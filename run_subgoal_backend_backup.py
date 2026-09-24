import os
import json
import numpy as np
from openai import OpenAI


# ============================================================
# DUAL LLM BACKEND CONFIGURATION
#
# Symbolic-LLM:
#     Ollama -> qwen3:8b
#
# MCTS-LLM:
#     vLLM -> Qwen/Qwen3-32B
#
# Both expose OpenAI-compatible APIs.
# ============================================================


# ------------------------------------------------------------
# Ollama configuration
# ------------------------------------------------------------

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434/v1"
)

OLLAMA_API_KEY = os.getenv(
    "OLLAMA_API_KEY",
    "ollama"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:8b"
)


# ------------------------------------------------------------
# vLLM configuration
# ------------------------------------------------------------

VLLM_BASE_URL = os.getenv(
    "VLLM_BASE_URL",
    "http://localhost:8000/v1"
)

VLLM_API_KEY = os.getenv(
    "VLLM_API_KEY",
    "local-key"
)

VLLM_MODEL = os.getenv(
    "VLLM_MODEL",
    "Qwen/Qwen3-32B"
)


# ============================================================
# Backend detection
# ============================================================

def detect_backend(model):
    """
    Decide which backend should be used.

    Explicit prefixes are supported:

        ollama:qwen3:8b
        vllm:Qwen/Qwen3-32B

    If no prefix is provided, the model name is used:

        qwen3:8b          -> Ollama
        Qwen/Qwen3-32B    -> vLLM
    """

    if not model:
        return "ollama"

    model_lower = model.lower()

    # Explicit backend selection
    if model_lower.startswith("ollama:"):
        return "ollama"

    if model_lower.startswith("vllm:"):
        return "vllm"

    # Automatic selection
    if model_lower == "qwen3:8b":
        return "ollama"

    if "qwen3-32b" in model_lower:
        return "vllm"

    if "qwen/qwen3" in model_lower:
        return "vllm"

    # Default
    return os.getenv("LLM_BACKEND", "ollama").lower()


# ============================================================
# Remove explicit backend prefix
# ============================================================

def clean_model_name(model, backend):
    """
    Convert:

        ollama:qwen3:8b
        vllm:Qwen/Qwen3-32B

    into the actual model name expected by the server.
    """

    if not model:
        return (
            OLLAMA_MODEL
            if backend == "ollama"
            else VLLM_MODEL
        )

    if model.lower().startswith("ollama:"):
        return model[len("ollama:"):]

    if model.lower().startswith("vllm:"):
        return model[len("vllm:"):]

    return model


# ============================================================
# Create OpenAI-compatible client
# ============================================================

def create_client(model):
    """
    Create the correct OpenAI-compatible client.

    Ollama:
        http://localhost:11434/v1

    vLLM:
        http://localhost:8000/v1
    """

    backend = detect_backend(model)

    actual_model = clean_model_name(model, backend)

    if backend == "vllm":

        print(
            f"[LLM BACKEND] vLLM | "
            f"URL={VLLM_BASE_URL} | "
            f"MODEL={actual_model}"
        )

        client = OpenAI(
            base_url=VLLM_BASE_URL,
            api_key=VLLM_API_KEY
        )

    else:

        print(
            f"[LLM BACKEND] Ollama | "
            f"URL={OLLAMA_BASE_URL} | "
            f"MODEL={actual_model}"
        )

        client = OpenAI(
            base_url=OLLAMA_BASE_URL,
            api_key=OLLAMA_API_KEY
        )

    return client, backend, actual_model


# ============================================================
# Build backend-specific extra parameters
# ============================================================

def get_extra_body(backend):
    """
    Qwen3 thinking configuration.

    Ollama:
        extra_body={"think": False}

    vLLM:
        disable Qwen3 thinking through chat_template_kwargs.
    """

    if backend == "vllm":

        return {
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        }

    else:

        return {
            "think": False
        }


# ============================================================
# Single completion request
# ============================================================

def _request_completion(
    client,
    backend,
    model,
    messages,
    max_tokens,
    temperature,
    logprobs,
    top_logprobs
):

    kwargs = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    # --------------------------------------------------------
    # Log probabilities
    #
    # Required by MCTS-LLM.
    # --------------------------------------------------------

    if logprobs:
        kwargs["logprobs"] = True

        if top_logprobs is not None:
            kwargs["top_logprobs"] = top_logprobs
    else:
        kwargs["logprobs"] = False

    # --------------------------------------------------------
    # Backend-specific Qwen3 settings
    # --------------------------------------------------------

    extra_body = get_extra_body(backend)

    if extra_body:
        kwargs["extra_body"] = extra_body

    response = client.chat.completions.create(**kwargs)

    return response.model_dump()


# ============================================================
# Main LLM completion function
# ============================================================

def get_session_completion(
    chat_history,
    model=None,
    max_tokens=2048,
    temperature=0.0,
    logprobs=False,
    top_logprobs=None
):

    # --------------------------------------------------------
    # Select model
    # --------------------------------------------------------

    if model is None:
        model = os.getenv(
            "LLM_MODEL",
            OLLAMA_MODEL
        )

    # --------------------------------------------------------
    # Create appropriate backend
    # --------------------------------------------------------

    client, backend, actual_model = create_client(model)

    print("=" * 60)
    print("LLM REQUEST")
    print(f"Backend       : {backend}")
    print(f"Model         : {actual_model}")
    print(f"Temperature   : {temperature}")
    print(f"Max tokens    : {max_tokens}")
    print(f"Logprobs      : {logprobs}")
    print("=" * 60)

    # --------------------------------------------------------
    # First request
    # --------------------------------------------------------

    result = _request_completion(
        client=client,
        backend=backend,
        model=actual_model,
        messages=chat_history,
        max_tokens=max_tokens,
        temperature=temperature,
        logprobs=logprobs,
        top_logprobs=top_logprobs
    )

    # --------------------------------------------------------
    # Basic response validation
    # --------------------------------------------------------

    if not result:
        raise RuntimeError(
            "LLM returned an empty response."
        )

    if "choices" not in result:
        print(
            "Invalid LLM response:"
        )
        print(
            json.dumps(
                result,
                indent=2
            )
        )

        raise KeyError(
            "LLM response does not contain 'choices'."
        )

    if not result["choices"]:
        raise RuntimeError(
            "LLM response contains an empty choices list."
        )

    choice = result["choices"][0]

    message = choice.get(
        "message",
        {}
    )

    content = message.get(
        "content",
        ""
    )

    reasoning = message.get(
        "reasoning",
        ""
    )

    finish_reason = choice.get(
        "finish_reason"
    )

    print(
        "LLM CONTENT:",
        repr(content)
    )

    print(
        "LLM FINISH:",
        finish_reason
    )

    if reasoning:
        print(
            "LLM REASONING RECEIVED:",
            repr(reasoning[:200])
        )

    # --------------------------------------------------------
    # Important:
    #
    # If the model stops because of max_tokens, continue.
    # --------------------------------------------------------

    if finish_reason == "length":

        print(
            "LLM reached token limit."
        )

        assistant_content = message.get(
            "content",
            ""
        )

        # Add first response to conversation
        chat_history.append(
            {
                "role": "assistant",
                "content": assistant_content
            }
        )

        # Ask for continuation
        chat_history.append(
            {
                "role": "user",
                "content":
                    "Continue from exactly where you stopped. "
                    "Output only PDDL plan actions."
            }
        )

        # ----------------------------------------------------
        # Second request
        # ----------------------------------------------------

        next_result = _request_completion(
            client=client,
            backend=backend,
            model=actual_model,
            messages=chat_history,
            max_tokens=max_tokens,
            temperature=temperature,
            logprobs=logprobs,
            top_logprobs=top_logprobs
        )

        if (
            "choices" not in next_result
            or not next_result["choices"]
        ):
            raise RuntimeError(
                "Continuation request returned invalid response."
            )

        next_choice = next_result["choices"][0]

        next_message = next_choice.get(
            "message",
            {}
        )

        next_content = next_message.get(
            "content",
            ""
        )

        print(
            "LLM CONTINUATION:",
            repr(next_content)
        )

        # ----------------------------------------------------
        # Combine textual content
        # ----------------------------------------------------

        result["choices"][0]["message"]["content"] = (
            assistant_content
            + "\n"
            + next_content
        )

        # ----------------------------------------------------
        # Combine logprobs if available
        #
        # MCTS needs this.
        # ----------------------------------------------------

        if logprobs:

            first_logprobs = (
                result["choices"][0].get(
                    "logprobs"
                )
            )

            next_logprobs = (
                next_choice.get(
                    "logprobs"
                )
            )

            if (
                first_logprobs
                and next_logprobs
            ):

                first_content = (
                    first_logprobs.get(
                        "content"
                    )
                )

                next_content_logprobs = (
                    next_logprobs.get(
                        "content"
                    )
                )

                if (
                    first_content is not None
                    and next_content_logprobs is not None
                ):

                    first_content.extend(
                        next_content_logprobs
                    )

        return result

    return result


# ============================================================
# Extract PDDL action lines
# ============================================================

def extract_pddl_actions(text):

    if not text:
        return []

    actions = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Ignore comments
        if line.startswith(";"):
            continue

        # Ignore Markdown fences
        if line.startswith("```"):
            continue

        # Only keep PDDL-like action lines
        if line.startswith("(") and line.endswith(")"):

            actions.append(line)

    return actions


# ============================================================
# Calculate sequence probabilities
# ============================================================

def seq_prob(completion):

    # --------------------------------------------------------
    # Validate response
    # --------------------------------------------------------

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
            "The completion response does not contain "
            "'choices' key"
        )

    if not completion["choices"]:

        raise RuntimeError(
            "Completion contains no choices."
        )

    choice = completion["choices"][0]

    # --------------------------------------------------------
    # Get generated text
    # --------------------------------------------------------

    response_text = (
        choice
        .get("message", {})
        .get("content", "")
        .strip()
    )

    # --------------------------------------------------------
    # Get log probabilities
    #
    # This is essential for MCTS-LLM.
    # --------------------------------------------------------

    logprobs_object = choice.get(
        "logprobs"
    )

    if not logprobs_object:

        raise RuntimeError(
            "No logprobs returned by the LLM backend. "
            "MCTS-LLM requires token log probabilities."
        )

    logprobs_content = (
        logprobs_object.get(
            "content"
        )
    )

    if not logprobs_content:

        raise RuntimeError(
            "logprobs.content is empty. "
            "The selected backend/model does not "
            "provide token log probabilities."
        )

    # --------------------------------------------------------
    # Extract tokens and log probabilities
    # --------------------------------------------------------

    tokens = []

    token_logprobs = []

    for token_info in logprobs_content:

        token = token_info.get(
            "token",
            ""
        )

        logprob = token_info.get(
            "logprob"
        )

        if logprob is None:
            continue

        tokens.append(token)
        token_logprobs.append(logprob)

    # --------------------------------------------------------
    # Extract valid action lines
    # --------------------------------------------------------

    action_lines = []

    for line in response_text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith(";"):
            continue

        if line.startswith("```"):
            continue

        if line.startswith("("):

            action_lines.append(line)

    if not action_lines:

        print(
            "WARNING: No PDDL actions found in response."
        )

        return []

    # --------------------------------------------------------
    # Calculate log probability for each action
    # --------------------------------------------------------

    action_logprobs = []

    current_action_logprob = 0.0

    action_idx = 0

    for token, logprob in zip(
        tokens,
        token_logprobs
    ):

        current_action_logprob += logprob

        # ----------------------------------------------------
        # Detect action boundary
        #
        # Most OpenAI-compatible tokenizers preserve
        # newline information either as "\n" or as part
        # of the next token.
        # ----------------------------------------------------

        if "\n" in token:

            if action_idx < len(action_lines):

                action_logprobs.append(
                    current_action_logprob
                )

                current_action_logprob = 0.0

                action_idx += 1

    # --------------------------------------------------------
    # Last action
    # --------------------------------------------------------

    if (
        action_idx < len(action_lines)
        and current_action_logprob != 0
    ):

        action_logprobs.append(
            current_action_logprob
        )

    # --------------------------------------------------------
    # If token/newline alignment is imperfect,
    # create a safe fallback.
    #
    # This prevents MCTS from crashing simply because
    # the tokenizer did not return newline as an individual
    # token.
    # --------------------------------------------------------

    if len(action_logprobs) != len(action_lines):

        print(
            "WARNING: Token/action alignment mismatch."
        )

        print(
            "Actions:",
            len(action_lines)
        )

        print(
            "Probabilities:",
            len(action_logprobs)
        )

        # ----------------------------------------------------
        # Conservative fallback:
        # distribute token log probability according to
        # action count.
        # ----------------------------------------------------

        if len(action_logprobs) == 0:

            total_logprob = sum(
                token_logprobs
            )

            average_logprob = (
                total_logprob
                / max(
                    len(action_lines),
                    1
                )
            )

            action_logprobs = [
                average_logprob
                for _ in action_lines
            ]

        elif len(action_logprobs) < len(action_lines):

            last_value = action_logprobs[-1]

            while len(action_logprobs) < len(action_lines):

                action_logprobs.append(
                    last_value
                )

        else:

            action_logprobs = (
                action_logprobs[
                    :len(action_lines)
                ]
            )

    # --------------------------------------------------------
    # Convert log probabilities to probabilities
    # --------------------------------------------------------

    action_probabilities = [
        float(np.exp(logprob))
        for logprob in action_logprobs
    ]

    # --------------------------------------------------------
    # Return:
    #
    # [
    #     ("(action a b)", probability),
    #     ("(action c d)", probability)
    # ]
    # --------------------------------------------------------

    actions_with_probabilities = list(
        zip(
            action_lines,
            action_probabilities
        )
    )

    return actions_with_probabilities