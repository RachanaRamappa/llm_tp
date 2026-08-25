import json
import requests
import warnings
import numpy as np

warnings.filterwarnings("ignore")


# ============================================================
# vLLM Configuration
# ============================================================

VLLM_URL = "http://localhost:8000"
VLLM_CHAT_URL = f"{VLLM_URL}/v1/chat/completions"
VLLM_MODELS_URL = f"{VLLM_URL}/v1/models"

DEFAULT_MODEL = "Qwen/Qwen3-0.6B"

# Timeout for LLM requests
REQUEST_TIMEOUT = 300


# ============================================================
# Check whether vLLM server is running
# ============================================================

def check_vllm_server():

    try:

        response = requests.get(
            VLLM_MODELS_URL,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        models = [
            item.get("id")
            for item in data.get("data", [])
        ]

        print("\n===== vLLM SERVER =====")
        print("Status: RUNNING")
        print("Models:")

        if models:

            for model in models:
                print(" -", model)

        else:

            print(" - No models reported")

        print("=======================\n")

        return True

    except requests.exceptions.RequestException as e:

        print("\n===== vLLM SERVER =====")
        print("Status: NOT RUNNING")
        print("Error:", e)
        print("=======================\n")

        return False

    except Exception as e:

        print("\n===== vLLM SERVER =====")
        print("Status: NOT RUNNING")
        print("Error:", e)
        print("=======================\n")

        return False


# ============================================================
# Check whether requested model exists
# ============================================================

def check_model_available(model):

    try:

        response = requests.get(
            VLLM_MODELS_URL,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        models = [
            item.get("id")
            for item in data.get("data", [])
        ]

        if model not in models:

            print("\nWARNING:")
            print("Requested model:", model)
            print("Available models:", models)
            print()

            return False

        return True

    except Exception:

        return False


# ============================================================
# Clean Qwen / LLM output
# ============================================================

def clean_llm_content(content):

    if content is None:
        return ""

    content = str(content).strip()

    # --------------------------------------------------------
    # Remove Qwen thinking blocks
    # --------------------------------------------------------

    if "<think>" in content:

        if "</think>" in content:

            content = content.split(
                "</think>",
                1
            )[1].strip()

        else:

            content = content.replace(
                "<think>",
                ""
            ).strip()

    # --------------------------------------------------------
    # Remove markdown code fences
    # --------------------------------------------------------

    if content.startswith("```"):

        lines = content.splitlines()

        cleaned_lines = []

        for line in lines:

            line = line.strip()

            if line.startswith("```"):
                continue

            cleaned_lines.append(line)

        content = "\n".join(
            cleaned_lines
        ).strip()

    # --------------------------------------------------------
    # Remove common unwanted prefixes
    # --------------------------------------------------------

    prefixes = [

        "Plan PDDL:",
        "plan PDDL:",
        "PLAN PDDL:",
        "Subgoal:",
        "subgoal:",
        "Goal:",
        "goal:"
    ]

    for prefix in prefixes:

        if content.startswith(prefix):

            content = content[
                len(prefix):
            ].strip()

            break

    return content.strip()


# ============================================================
# Get vLLM completion
# ============================================================

def get_session_completion(
    chat_history,
    model=DEFAULT_MODEL,
    max_tokens=500,
    temperature=0.0,
    logprobs=False,
    top_logprobs=None
):

    # --------------------------------------------------------
    # Check server
    # --------------------------------------------------------
    print("get completion")
    if not check_vllm_server():

        raise RuntimeError(
            "vLLM server is not running.\n\n"
            "Start it using:\n\n"
            "vllm serve Qwen/Qwen3-0.6B "
            "--max-model-len 2048 "
            "--default-chat-template-kwargs "
            "'{\"enable_thinking\": false}'"
        )

    # --------------------------------------------------------
    # Check model
    # --------------------------------------------------------

    if not check_model_available(model):

        raise RuntimeError(
            f"Model '{model}' is not available "
            "on the vLLM server."
        )

    # --------------------------------------------------------
    # Validate chat history
    # --------------------------------------------------------

    if not isinstance(chat_history, list):

        raise TypeError(
            "chat_history must be a list of "
            "message dictionaries."
        )

    for message in chat_history:

        if not isinstance(message, dict):

            raise TypeError(
                "Every chat_history item must "
                "be a dictionary."
            )

        if "role" not in message:

            raise ValueError(
                "Each message must contain 'role'."
            )

        if "content" not in message:

            raise ValueError(
                "Each message must contain 'content'."
            )

    # --------------------------------------------------------
    # Build request
    #
    # IMPORTANT:
    #
    # chat_template_kwargs is placed inside extra_body.
    #
    # This matches the OpenAI/vLLM interface used by the
    # working curl test.
    # --------------------------------------------------------

    payload = {

        "model": model,

        "messages": chat_history,

        "temperature": float(
            temperature
        ),

        "max_tokens": int(
            max_tokens
        ),

        "extra_body": {

            "chat_template_kwargs": {

                "enable_thinking": False

            }

        }

    }

    # --------------------------------------------------------
    # Optional logprobs
    # --------------------------------------------------------

    if logprobs:

        payload["logprobs"] = True

        if top_logprobs is not None:

            payload["top_logprobs"] = int(
                top_logprobs
            )

    # --------------------------------------------------------
    # Debug request
    # --------------------------------------------------------

    print("\n===== vLLM REQUEST =====")
    print("Model:", model)
    print("Max tokens:", max_tokens)
    print("Temperature:", temperature)
    print("Thinking:", False)
    print("Logprobs:", logprobs)
    print("========================\n")

    # --------------------------------------------------------
    # Send request
    # --------------------------------------------------------

    try:

        response = requests.post(
            VLLM_CHAT_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )

    except requests.exceptions.ConnectionError as e:

        raise RuntimeError(
            "Could not connect to vLLM server at "
            f"{VLLM_CHAT_URL}.\n"
            "Make sure vLLM is running."
        ) from e

    except requests.exceptions.Timeout as e:

        raise RuntimeError(
            "vLLM request timed out."
        ) from e

    # --------------------------------------------------------
    # Handle HTTP errors with useful information
    # --------------------------------------------------------

    if not response.ok:

        print("\n===== vLLM ERROR =====")
        print("HTTP status:", response.status_code)
        print("Response:")

        try:

            print(
                json.dumps(
                    response.json(),
                    indent=2
                )
            )

        except Exception:

            print(
                response.text
            )

        print("======================\n")

        response.raise_for_status()

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    try:

        data = response.json()

    except Exception as e:

        print("\n===== INVALID JSON =====")
        print(response.text)
        print("========================\n")

        raise RuntimeError(
            "vLLM returned invalid JSON."
        ) from e

    # --------------------------------------------------------
    # Validate response
    # --------------------------------------------------------

    if "choices" not in data:

        print(
            "\n===== INVALID vLLM RESPONSE ====="
        )

        print(
            json.dumps(
                data,
                indent=2
            )
        )

        print(
            "=================================\n"
        )

        raise RuntimeError(
            "vLLM response does not contain "
            "'choices'."
        )

    if not data["choices"]:

        raise RuntimeError(
            "vLLM returned an empty choices list."
        )

    # --------------------------------------------------------
    # Get first choice
    # --------------------------------------------------------

    choice = data["choices"][0]

    message = choice.get(
        "message",
        {}
    )

    if not isinstance(message, dict):

        message = {}

    # --------------------------------------------------------
    # Extract content
    # --------------------------------------------------------

    content = message.get(
        "content",
        ""
    )

    content = clean_llm_content(
        content
    )

    # --------------------------------------------------------
    # Extract reasoning if present
    #
    # We do NOT expose reasoning to the rest of the project.
    # Qwen3 thinking is disabled anyway.
    # --------------------------------------------------------

    reasoning = message.get(
        "reasoning"
    )

    # --------------------------------------------------------
    # Extract logprobs
    # --------------------------------------------------------

    response_logprobs = choice.get(
        "logprobs"
    )

    # --------------------------------------------------------
    # Debug response
    # --------------------------------------------------------

    print(
        "===== vLLM RESPONSE ====="
    )

    print(
        "LLM CONTENT:"
    )

    print(
        repr(content)
    )

    if reasoning:

        print(
            "Reasoning returned:",
            repr(reasoning)
        )

    print(
        "Finish reason:",
        choice.get(
            "finish_reason"
        )
    )

    if "usage" in data:

        usage = data["usage"]

        print(
            "Prompt tokens:",
            usage.get(
                "prompt_tokens"
            )
        )

        print(
            "Completion tokens:",
            usage.get(
                "completion_tokens"
            )
        )

        print(
            "Total tokens:",
            usage.get(
                "total_tokens"
            )
        )

    print(
        "========================\n"
    )

    # --------------------------------------------------------
    # Return structure expected by project
    # --------------------------------------------------------

    result = {

        "choices": [

            {

                "message": {

                    "role": "assistant",

                    "content": content

                },

                "finish_reason":
                    choice.get(
                        "finish_reason",
                        "stop"
                    ),

                "logprobs":
                    response_logprobs

            }

        ],

        "model":
            data.get(
                "model",
                model
            ),

        "usage":
            data.get(
                "usage",
                {}
            )

    }

    return result


# ============================================================
# Extract PDDL action lines
# ============================================================

def extract_pddl_actions(text):

    if not text:

        return []

    actions = []

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # ----------------------------------------------------
        # Ignore comments
        # ----------------------------------------------------

        if line.startswith(";"):
            continue

        # ----------------------------------------------------
        # Ignore markdown
        # ----------------------------------------------------

        if line.startswith("```"):
            continue

        if line.startswith("#"):
            continue

        # ----------------------------------------------------
        # PDDL action
        # ----------------------------------------------------

        if (
            line.startswith("(")
            and line.endswith(")")
        ):

            actions.append(
                line
            )

    return actions


# ============================================================
# Calculate action probabilities
# ============================================================

def seq_prob(completion):

    # --------------------------------------------------------
    # Validate response
    # --------------------------------------------------------

    if not isinstance(
        completion,
        dict
    ):

        raise TypeError(
            "completion must be a dictionary."
        )

    if "choices" not in completion:

        print(
            "Invalid response structure:"
        )

        print(
            json.dumps(
                completion,
                indent=2
            )
        )

        raise KeyError(
            "The completion response does not "
            "contain 'choices'."
        )

    if not completion["choices"]:

        return []

    # --------------------------------------------------------
    # Get response text
    # --------------------------------------------------------

    response_text = (

        completion["choices"][0]
        .get("message", {})
        .get("content", "")

    )

    response_text = clean_llm_content(
        response_text
    )

    # --------------------------------------------------------
    # Extract PDDL actions
    # --------------------------------------------------------

    action_lines = extract_pddl_actions(
        response_text
    )

    # --------------------------------------------------------
    # No actions
    # --------------------------------------------------------

    if not action_lines:

        return []

    # --------------------------------------------------------
    # Get logprobs
    # --------------------------------------------------------

    logprobs = (

        completion["choices"][0]
        .get("logprobs")

    )

    # --------------------------------------------------------
    # No logprobs
    #
    # Return default probability 1.0.
    # --------------------------------------------------------

    if not logprobs:

        return [
            (
                action,
                1.0
            )

            for action in action_lines
        ]

    # --------------------------------------------------------
    # vLLM logprobs structure
    # --------------------------------------------------------

    logprobs_content = logprobs.get(
        "content"
    )

    if not logprobs_content:

        return [
            (
                action,
                1.0
            )

            for action in action_lines
        ]

    # --------------------------------------------------------
    # Extract token log probabilities
    # --------------------------------------------------------

    token_logprobs = []

    tokens = []

    for token_data in logprobs_content:

        if not isinstance(
            token_data,
            dict
        ):

            continue

        token = token_data.get(
            "token",
            ""
        )

        logprob = token_data.get(
            "logprob"
        )

        if logprob is None:

            continue

        tokens.append(
            token
        )

        token_logprobs.append(
            float(logprob)
        )

    # --------------------------------------------------------
    # If token logprobs unavailable
    # --------------------------------------------------------

    if not token_logprobs:

        return [
            (
                action,
                1.0
            )

            for action in action_lines
        ]

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Do not attempt to calculate action probabilities by
    # blindly checking token.endswith(",") or token.endswith
    # newline. PDDL tokenization does not guarantee this.
    #
    # Instead, approximate probabilities based on balanced
    # parentheses.
    # --------------------------------------------------------

    action_logprobs = []

    current_logprob = 0.0

    parenthesis_depth = 0

    action_started = False

    completed_actions = 0

    for token, logprob in zip(
        tokens,
        token_logprobs
    ):

        current_logprob += logprob

        # ----------------------------------------------------
        # Count parentheses
        # ----------------------------------------------------

        for character in token:

            if character == "(":

                parenthesis_depth += 1
                action_started = True

            elif character == ")":

                parenthesis_depth -= 1

        # ----------------------------------------------------
        # One complete PDDL action
        # ----------------------------------------------------

        if (
            action_started
            and parenthesis_depth == 0
        ):

            if (
                completed_actions
                < len(action_lines)
            ):

                action_logprobs.append(
                    current_logprob
                )

                completed_actions += 1

            current_logprob = 0.0
            action_started = False

    # --------------------------------------------------------
    # Handle incomplete final action
    # --------------------------------------------------------

    if (
        action_started
        and completed_actions
        < len(action_lines)
    ):

        action_logprobs.append(
            current_logprob
        )

    # --------------------------------------------------------
    # Convert log probabilities
    #
    # exp(logprob) gives probability of the token sequence.
    # --------------------------------------------------------

    action_probabilities = []

    for logprob in action_logprobs:

        try:

            probability = float(
                np.exp(logprob)
            )

        except Exception:

            probability = 1.0

        # ----------------------------------------------------
        # Numerical safety
        # ----------------------------------------------------

        if not np.isfinite(
            probability
        ):

            probability = 1.0

        probability = max(
            0.0,
            min(
                1.0,
                probability
            )
        )

        action_probabilities.append(
            probability
        )

    # --------------------------------------------------------
    # Safety:
    # Make number of probabilities equal to number of actions
    # --------------------------------------------------------

    if (
        len(action_probabilities)
        > len(action_lines)
    ):

        action_probabilities = (
            action_probabilities[
                :len(action_lines)
            ]
        )

    while (
        len(action_probabilities)
        < len(action_lines)
    ):

        action_probabilities.append(
            1.0
        )

    # --------------------------------------------------------
    # Return:
    #
    # [
    #   ("(action ...)", probability),
    #   ...
    # ]
    # --------------------------------------------------------

    return list(
        zip(
            action_lines,
            action_probabilities
        )
    )