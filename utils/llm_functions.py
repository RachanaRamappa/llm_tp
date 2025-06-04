from openai import OpenAI
import os
import json
import requests
import warnings
import numpy as np
import asyncio
import aiohttp

warnings.filterwarnings('ignore')

def get_session_completion(chat_history, model="gpt-4o", max_tokens=4095,
                           temperature=0.7, logprobs=True, top_logprobs=None):
    with open("../config.json", "r") as f:
        config = json.load(f)
    api_key = config["OPENAI_API_KEY"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    def fetch_completion(messages):
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers,
                             json={
                                 "model": model,
                                 "messages": messages,
                                 "max_tokens": max_tokens,
                                 "temperature": temperature,
                                 "logprobs": logprobs,
                                 "top_logprobs": top_logprobs,
                             })

        return resp.json()

    result = fetch_completion(chat_history)

    if result['choices'][0]['finish_reason'] == 'length':
        chat_history.append({
            "role": "assistant",
            "content": result["choices"][0]['message']["content"]
        })
        chat_history.append({
            "role": "user",
            "content": f'''Continue.'''
        })
        next_result = fetch_completion(chat_history)

        result["choices"][0]['message']["content"] += "\n"
        result["choices"][0]['logprobs']["content"].append({'token': '\n', 'logprob': -3.0e-05, 'bytes': [10], 'top_logprobs': []})
        result["choices"][0]['message']["content"] += next_result["choices"][0]['message']["content"]
        result["choices"][0]['logprobs']["content"] += next_result["choices"][0]['logprobs']["content"]

    return result


def seq_prob(completion):
    if 'choices' not in completion:
        print("Invalid response structure:", json.dumps(completion, indent=2))
        raise KeyError("The completion response does not contain 'choices' key")
    response_text = completion["choices"][0]['message']["content"].strip()
    logprobs_content = completion["choices"][0]['logprobs']['content']
    token_logprobs = [token['logprob'] for token in logprobs_content]
    tokens = [token['token'] for token in logprobs_content]

    action_logprobs = []
    current_action_logprob = 0
    action_lines = []

    # Split response text into lines
    lines = response_text.split('\n')

    # Filter out comment lines and collect non-comment lines
    for line in lines:
        line = line.strip()
        if not line or line.startswith(';'):
            continue
        action_lines.append(line)

    # Process tokens to calculate action log probabilities
    action_idx = 0
    for token, logprob in zip(tokens, token_logprobs):
        if token.endswith(',') or token.endswith('\n'):
            current_action_logprob += logprob
            if action_idx < len(action_lines):
                action_logprobs.append(current_action_logprob)
                current_action_logprob = 0
                action_idx += 1
        else:
            current_action_logprob += logprob
    if current_action_logprob != 0 and action_idx < len(action_lines):
        action_logprobs.append(current_action_logprob)

    action_probabilities = [np.exp(logprob) for logprob in action_logprobs]

    # Ensure we do not exceed the number of actions found
    if len(action_probabilities) > len(action_lines):
        action_probabilities = action_probabilities[:len(action_lines)]

    actions_with_probabilities = list(zip(action_lines, action_probabilities))

    return actions_with_probabilities
