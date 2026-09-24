import os
import json
import requests
import warnings
import numpy as np
import time
import re

warnings.filterwarnings('ignore')

# Determine project base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def load_config():
    config = {}
    if os.path.isfile(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load {CONFIG_PATH}: {e}")
    return config

_config = load_config()

DEFAULT_BASE_URL = os.getenv("LLM_BASE_URL", _config.get("LLM_BASE_URL", "https://api.groq.com/openai/v1"))
DEFAULT_API_KEY = os.getenv("LLM_API_KEY", os.getenv("GROQ_API_KEY", _config.get("LLM_API_KEY", _config.get("GROQ_API_KEY", ""))))
DEFAULT_MODEL = os.getenv("LLM_MODEL", _config.get("LLM_MODEL", "qwen/qwen3.8-27b"))


def clean_llm_content(content):
    if not content:
        return ""
    content = str(content).strip()

    # Remove thinking tags
    if "<think>" in content:
        if "</think>" in content:
            content = content.split("</think>", 1)[1].strip()
        else:
            content = content.replace("<think>", "").strip()

    # Remove markdown code fences
    if "```" in content:
        lines = content.splitlines()
        cleaned = []
        for line in lines:
            if line.strip().startswith("```"):
                continue
            cleaned.append(line)
        content = "\n".join(cleaned).strip()

    return content


def get_session_completion(
    chat_history,
    model=None,
    max_tokens=4095,
    temperature=0.0,
    logprobs=False,
    top_logprobs=None,
):
    base_url = os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    api_key = os.getenv("LLM_API_KEY", os.getenv("GROQ_API_KEY", DEFAULT_API_KEY))
    target_model = model or os.getenv("LLM_MODEL", DEFAULT_MODEL)

    is_groq = "groq.com" in base_url.lower()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    def fetch_completion(messages, try_logprobs=logprobs):
        payload = {
            "model": target_model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        # Groq rejects logprobs parameter with HTTP 400
        if try_logprobs and not is_groq:
            payload["logprobs"] = True
            if top_logprobs is not None:
                payload["top_logprobs"] = top_logprobs

        for attempt in range(6):
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=180,
            )

            # If server returned 400 because of logprobs, retry once without logprobs
            if response.status_code == 400 and try_logprobs:
                if "logprobs" in response.text.lower():
                    return fetch_completion(messages, try_logprobs=False)

            # If rate limited (429), wait and retry
            if response.status_code == 429:
                retry_after = response.headers.get("retry-after")
                reset_tokens = response.headers.get("x-ratelimit-reset-tokens")
                wait_time = 3.5
                if retry_after:
                    try:
                        wait_time = float(retry_after) + 1.0
                    except Exception:
                        pass
                elif reset_tokens:
                    try:
                        wait_time = float(reset_tokens.rstrip("s")) + 1.0
                    except Exception:
                        pass
                wait_time = max(2.5, min(wait_time, 15.0))
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response.json()


    result = fetch_completion(chat_history)

    # Clean content if needed
    if "choices" in result and result["choices"]:
        msg = result["choices"][0].get("message", {})
        if "content" in msg and msg["content"]:
            msg["content"] = clean_llm_content(msg["content"])

    # Handle truncated completions (finish_reason == 'length')
    if result["choices"][0].get("finish_reason") == "length":
        chat_history.append({
            "role": "assistant",
            "content": result["choices"][0]["message"]["content"],
        })
        chat_history.append({
            "role": "user",
            "content": "Continue from exactly where you stopped. Output only PDDL plan actions.",
        })
        next_result = fetch_completion(chat_history, try_logprobs=False)
        result["choices"][0]["message"]["content"] += (
            "\n" + clean_llm_content(next_result["choices"][0]["message"]["content"])
        )

    return result


def extract_actions_and_headers(text):
    """Extract all lines keeping plan markers and action lines."""
    lines = text.splitlines()
    collected = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        collected.append(line)
    return collected


def seq_prob(completion, candidate_plans=None):
    """
    Calculates or generates action sequence probabilities for MCTS-LLM.
    - If logprobs are available from LLM: computes exact sequence probability per action.
    - If logprobs are not supported (e.g. Groq): generates calibrated sequence probabilities
      based on plan ranking, action depth, and empirical branch frequency.
    """
    if "choices" not in completion or not completion["choices"]:
        print("Invalid response structure:", json.dumps(completion, indent=2))
        raise KeyError("The completion response does not contain valid 'choices'")

    choice = completion["choices"][0]
    response_text = choice.get("message", {}).get("content", "").strip()
    all_lines = extract_actions_and_headers(response_text)

    if not all_lines:
        return []

    # Check if actual token logprobs are present
    logprobs_obj = choice.get("logprobs")
    has_logprobs = (
        logprobs_obj is not None
        and isinstance(logprobs_obj, dict)
        and "content" in logprobs_obj
        and logprobs_obj["content"]
    )

    if has_logprobs:
        # Compute exact token-level log probabilities using parenthesis-balanced segmentation
        logprobs_content = logprobs_obj["content"]
        tokens = [t.get("token", "") for t in logprobs_content if isinstance(t, dict)]
        token_logprobs = [float(t.get("logprob", 0.0)) for t in logprobs_content if isinstance(t, dict) and "logprob" in t]

        action_logprobs = []
        current_logprob = 0.0
        parenthesis_depth = 0
        action_started = False
        action_lines = [l for l in all_lines if l.startswith("(")]

        for token, logprob in zip(tokens, token_logprobs):
            current_logprob += logprob
            for ch in token:
                if ch == "(":
                    parenthesis_depth += 1
                    action_started = True
                elif ch == ")":
                    parenthesis_depth -= 1

            if action_started and parenthesis_depth == 0:
                action_logprobs.append(current_logprob)
                current_logprob = 0.0
                action_started = False

        if action_started and current_logprob != 0.0:
            action_logprobs.append(current_logprob)

        # Map back to all_lines
        action_idx = 0
        results = []
        for line in all_lines:
            if line.startswith("("):
                if action_idx < len(action_logprobs):
                    lp = action_logprobs[action_idx]
                    prob = float(np.exp(lp)) if np.isfinite(lp) else 1.0
                    action_idx += 1
                else:
                    prob = 0.5
                prob = max(0.01, min(1.0, prob))
                results.append((line, prob))
            else:
                results.append((line, 1.0))
        return results

    # =========================================================================
    # Fallback / SeqProb Generator when backend (like Groq) does not return logprobs
    # Generates calibrated probabilities based on plan rank, position, and frequency
    # =========================================================================
    results = []
    current_plan_idx = 1
    action_in_plan_idx = 0

    # Count action frequency across plans to give higher weight to consensus actions
    action_counts = {}
    temp_plan_actions = []
    for line in all_lines:
        line_clean = line.strip()
        if line_clean.lower().startswith("plan"):
            continue
        if line_clean.startswith("("):
            temp_plan_actions.append(line_clean)
            action_counts[line_clean] = action_counts.get(line_clean, 0) + 1

    total_actions = max(1, len(temp_plan_actions))

    for line in all_lines:
        line_clean = line.strip()
        if line_clean.lower().startswith("plan"):
            # Extract plan number if possible (e.g. "Plan PDDL 2")
            match = re.search(r'\d+', line_clean)
            if match:
                current_plan_idx = int(match.group(0))
            else:
                current_plan_idx += 1
            action_in_plan_idx = 0
            results.append((line, 1.0))
            continue

        if line_clean.startswith("("):
            # Prior based on plan ranking: earlier plans have higher LLM prior
            # Plan 1: base ~0.92, Plan 2: base ~0.82, Plan 3: base ~0.74, etc.
            rank_prior = max(0.40, 0.95 * (0.90 ** (current_plan_idx - 1)))

            # Step decay: slight confidence decay as plan deepens
            step_decay = max(0.60, 0.98 ** action_in_plan_idx)

            # Consensus bonus: if multiple candidate plans include this action
            consensus_bonus = min(0.15, 0.05 * (action_counts.get(line_clean, 1) - 1))

            prob = float(np.clip(rank_prior * step_decay + consensus_bonus, 0.10, 0.98))
            action_in_plan_idx += 1
            results.append((line, prob))
        else:
            results.append((line, 1.0))

    return results
