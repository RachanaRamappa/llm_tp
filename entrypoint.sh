#!/bin/bash
set -e

echo "========================================"
echo "Neuro-Symbolic Task Planning + vLLM"
echo "Offline A100 Deployment"
echo "========================================"

# ==================================================================
# Helper: wait for vLLM server to be ready
# ==================================================================
wait_for_vllm() {
    local VLLM_HOST
    local VLLM_PORT
    VLLM_HOST=$(echo "${LLM_BASE_URL}" | sed -E 's|https?://([^:/]+).*|\1|')
    VLLM_PORT=$(echo "${LLM_BASE_URL}" | sed -E 's|https?://[^:]+:([0-9]+).*|\1|')

    for i in $(seq 1 120); do
        if curl -sf "http://${VLLM_HOST}:${VLLM_PORT}/v1/models" \
                -H "Authorization: Bearer ${LLM_API_KEY}" > /dev/null 2>&1; then
            echo "vLLM server is ready!"
            return 0
        fi
        echo "Waiting for vLLM server... ($i/120)"
        sleep 5
    done

    echo "[ERROR] vLLM server did not become ready in 10 minutes!"
    exit 1
}

COMMAND="${1:-serve}"

case "$COMMAND" in

    # ==================================================================
    # MODE: serve — Start vLLM server for Qwen3-32B
    # ==================================================================
    serve)
        echo "Starting vLLM server..."
        echo "Model: ${MODEL_PATH:-Qwen/Qwen3-32B}"
        echo "Port: 8000"

        python3.11 -m vllm.entrypoints.openai.api_server \
            --model "${MODEL_PATH:-Qwen/Qwen3-32B}" \
            --served-model-name "Qwen/Qwen3-32B" \
            --host 0.0.0.0 \
            --port 8000 \
            --dtype auto \
            --api-key "${LLM_API_KEY:-local-key}" \
            --max-model-len "${MAX_MODEL_LEN:-16384}" \
            --gpu-memory-utilization "${GPU_MEM_UTIL:-0.90}" \
            --trust-remote-code
        ;;

    # ==================================================================
    # MODE: mcts — Run MCTS-LLM planner
    # ==================================================================
    mcts)
        export LLM_BASE_URL="${LLM_BASE_URL:-http://vllm-server:8000/v1}"
        export LLM_API_KEY="${LLM_API_KEY:-local-key}"
        export LLM_MODEL="${MODEL_NAME:-Qwen/Qwen3-32B}"

        echo "Waiting for vLLM server at ${LLM_BASE_URL}..."
        wait_for_vllm

        DOMAINS="${DOMAIN:-barman blocksworld gripper}"

        for domain in $DOMAINS; do
            echo ""
            echo "============================================================"
            echo "  MCTS-LLM: Domain = $domain"
            echo "============================================================"

            cd /app

            python3.11 run_subgoal.py \
                --model "${LLM_MODEL}" \
                --backend vllm \
                --domain "$domain" \
                --subgoal_planner "mcts-llm" \
                --temperature 0.0 \
                --ns ${NS:-3 4 5} \
                --sizes ${SIZES:-2 3 4 5 6 7 8 9 10}
        done

        echo ""
        echo "========================================"
        echo "  MCTS-LLM COMPLETE (all domains)"
        echo "========================================"
        ;;

    # ==================================================================
    # MODE: symbolic — Run Symbolic-LLM planner
    # ==================================================================
    symbolic)
        export LLM_BASE_URL="${LLM_BASE_URL:-http://vllm-server:8000/v1}"
        export LLM_API_KEY="${LLM_API_KEY:-local-key}"
        export LLM_MODEL="${MODEL_NAME:-Qwen/Qwen3-32B}"

        echo "Waiting for vLLM server at ${LLM_BASE_URL}..."
        wait_for_vllm

        DOMAINS="${DOMAIN:-barman blocksworld gripper}"

        for domain in $DOMAINS; do
            echo ""
            echo "============================================================"
            echo "  Symbolic-LLM: Domain = $domain"
            echo "============================================================"

            cd /app

            python3.11 run_subgoal.py \
                --model "${LLM_MODEL}" \
                --backend vllm \
                --domain "$domain" \
                --subgoal_planner "symbolic-llm" \
                --temperature 0.0 \
                --planner "${FD_PLANNER:-seq-opt-fdss-1}" \
                --sizes ${SIZES:-2 3 4 5 6 7 8 9 10} \
                --path "${FD_PATH:-/opt/downward/fast-downward.py}"
        done

        echo ""
        echo "========================================"
        echo "  Symbolic-LLM COMPLETE (all domains)"
        echo "========================================"
        ;;

    # ==================================================================
    # MODE: fd-baseline — Run Fast Downward baseline (no LLM needed)
    # ==================================================================
    fd-baseline)
        DOMAINS="${DOMAIN:-barman blocksworld gripper}"

        for domain in $DOMAINS; do
            echo ""
            echo "============================================================"
            echo "  Fast Downward Baseline: Domain = $domain"
            echo "============================================================"

            cd /app

            python3.11 run_fd.py \
                --domain "$domain" \
                --planner "${FD_PLANNER:-seq-opt-fdss-1}" \
                --sizes ${SIZES:-2 3 4 5 6 7 8 9 10} \
                --path "${FD_PATH:-/opt/downward/fast-downward.py}"
        done

        echo ""
        echo "========================================"
        echo "  FD Baseline COMPLETE (all domains)"
        echo "========================================"
        ;;

    # ==================================================================
    # MODE: run-all — Run ALL planners on ALL domains
    # ==================================================================
    run-all)
        export LLM_BASE_URL="${LLM_BASE_URL:-http://vllm-server:8000/v1}"
        export LLM_API_KEY="${LLM_API_KEY:-local-key}"
        export LLM_MODEL="${MODEL_NAME:-Qwen/Qwen3-32B}"

        echo "Waiting for vLLM server at ${LLM_BASE_URL}..."
        wait_for_vllm

        DOMAINS="${DOMAIN:-barman blocksworld gripper}"

        for domain in $DOMAINS; do
            echo ""
            echo "########################################################"
            echo "  DOMAIN: $domain"
            echo "########################################################"

            cd /app

            # --- Fast Downward Baseline ---
            echo ""
            echo ">>> [1/3] Fast Downward Baseline: $domain"
            python3.11 run_fd.py \
                --domain "$domain" \
                --planner "${FD_PLANNER:-seq-opt-fdss-1}" \
                --sizes ${SIZES:-2 3 4 5 6 7 8 9 10} \
                --path "${FD_PATH:-/opt/downward/fast-downward.py}" \
                || echo "[WARN] FD Baseline failed for $domain, continuing..."

            # --- Symbolic-LLM ---
            echo ""
            echo ">>> [2/3] Symbolic-LLM: $domain"
            python3.11 run_subgoal.py \
                --model "${LLM_MODEL}" \
                --backend vllm \
                --domain "$domain" \
                --subgoal_planner "symbolic-llm" \
                --temperature 0.0 \
                --planner "${FD_PLANNER:-seq-opt-fdss-1}" \
                --sizes ${SIZES:-2 3 4 5 6 7 8 9 10} \
                --path "${FD_PATH:-/opt/downward/fast-downward.py}" \
                || echo "[WARN] Symbolic-LLM failed for $domain, continuing..."

            # --- MCTS-LLM ---
            echo ""
            echo ">>> [3/3] MCTS-LLM: $domain"
            python3.11 run_subgoal.py \
                --model "${LLM_MODEL}" \
                --backend vllm \
                --domain "$domain" \
                --subgoal_planner "mcts-llm" \
                --temperature 0.0 \
                --ns ${NS:-3 4 5} \
                --sizes ${SIZES:-2 3 4 5 6 7 8 9 10} \
                || echo "[WARN] MCTS-LLM failed for $domain, continuing..."
        done

        # --- Validate All Plans ---
        echo ""
        echo "########################################################"
        echo "  VALIDATING ALL PLANS"
        echo "########################################################"
        cd /app
        python3.11 validate_plans.py || echo "[WARN] Validation encountered errors"

        echo ""
        echo "========================================"
        echo "  ALL EXPERIMENTS COMPLETE"
        echo "========================================"
        echo "Results are in /app/experiments/"
        echo "========================================"
        ;;

    # ==================================================================
    # MODE: validate — Validate all generated plans using VAL
    # ==================================================================
    validate)
        cd /app
        python3.11 validate_plans.py
        ;;

    # ==================================================================
    # MODE: bash/sh — Interactive shell
    # ==================================================================
    bash|sh)
        exec /bin/bash "${@:2}"
        ;;

    python|python3|python3.11)
        exec python3.11 "${@:2}"
        ;;

    *)
        echo "Unknown command: $COMMAND"
        echo ""
        echo "Available commands:"
        echo "  serve        - Start vLLM model server"
        echo "  mcts         - Run MCTS-LLM planner on all domains"
        echo "  symbolic     - Run Symbolic-LLM planner on all domains"
        echo "  fd-baseline  - Run Fast Downward baseline (no LLM)"
        echo "  run-all      - Run all planners on all domains"
        echo "  validate     - Validate all generated plans"
        echo "  bash         - Open interactive shell"
        echo ""
        exec python3.11 "$COMMAND" "${@:2}"
        ;;
esac
