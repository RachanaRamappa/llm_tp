#!/bin/bash
set -e

echo "========================================"
echo "Neuro-Symbolic Task Planning + vLLM"
echo "========================================"

COMMAND="${1:-serve}"

case "$COMMAND" in
    serve)
        echo "Starting vLLM server for Qwen3-32B..."
        echo "Model: Qwen/Qwen3-32B"
        echo "Port: 8000"

        python3.11 -m vllm.entrypoints.openai.api_server \
            --model "${MODEL_PATH:-Qwen/Qwen3-32B}" \
            --served-model-name "Qwen/Qwen3-32B" \
            --host 0.0.0.0 \
            --port 8000 \
            --dtype auto \
            --api-key "${LLM_API_KEY:-local-key}" \
            --max-model-len 16384 \
            --trust-remote-code
        ;;

    mcts)
        export LLM_BASE_URL="${LLM_BASE_URL:-http://vllm-server:8000/v1}"
        export LLM_API_KEY="${LLM_API_KEY:-local-key}"
        export LLM_MODEL="${MODEL_NAME:-Qwen/Qwen3-32B}"

        echo "Waiting for vLLM server at ${LLM_BASE_URL}..."

        VLLM_HOST=$(echo "${LLM_BASE_URL}" | sed -E 's|https?://([^:/]+).*|\1|')
        VLLM_PORT=$(echo "${LLM_BASE_URL}" | sed -E 's|https?://[^:]+:([0-9]+).*|\1|')

        for i in $(seq 1 60); do
            if curl -sf "http://${VLLM_HOST}:${VLLM_PORT}/v1/models" -H "Authorization: Bearer ${LLM_API_KEY}" > /dev/null 2>&1; then
                echo "vLLM server is ready!"
                break
            fi
            echo "Waiting for vLLM server... ($i/60)"
            sleep 10
        done

        echo "Running MCTS LLM planner..."
        echo "Domain: ${DOMAIN:-barman}"
        echo "Model: ${LLM_MODEL}"
        echo "LLM Base URL: ${LLM_BASE_URL}"

        cd /app/scripts

        python3.11 run_subgoal.py \
            --model "${LLM_MODEL}" \
            --domain "${DOMAIN:-barman}" \
            --subgoal_planner "mcts-llm" \
            --temperature 0.0 \
            --ns ${NS:-3 4 5} \
            --sizes ${SIZES:-2 3 4 5}
        ;;

    symbolic)
        export LLM_BASE_URL="${LLM_BASE_URL:-http://vllm-server:8000/v1}"
        export LLM_API_KEY="${LLM_API_KEY:-local-key}"
        export LLM_MODEL="${MODEL_NAME:-Qwen/Qwen3-32B}"

        cd /app/scripts

        python3.11 run_subgoal.py \
            --model "${LLM_MODEL}" \
            --domain "${DOMAIN:-barman}" \
            --subgoal_planner "symbolic-llm" \
            --temperature 0.0 \
            --planner "${FD_PLANNER:-seq-opt-fdss-1}" \
            --sizes ${SIZES:-2 3 4 5} \
            --path "${FD_PATH:-/app/downward/fast-downward.py}"
        ;;

    bash|sh)
        exec /bin/bash "${@:2}"
        ;;

    python|python3.11)
        exec python3.11 "${@:2}"
        ;;

    *)
        echo "Unknown command: $COMMAND"
        echo "Available commands: serve, mcts, symbolic, bash, python"
        exec python3.11 "$COMMAND" "${@:2}"
        ;;
esac
