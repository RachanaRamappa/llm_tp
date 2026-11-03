# Fast and Accurate Task Planning using Neuro-Symbolic Language Models

[![Docker Image](https://img.shields.io/badge/Docker%20Package-ghcr.io%2Frachanaramappa%2Fllm__tp-blue?logo=docker)](https://github.com/RachanaRamappa/llm_tp/pkgs/container/llm_tp)
[![CI Build](https://github.com/RachanaRamappa/llm_tp/actions/workflows/docker.yml/badge.svg)](https://github.com/RachanaRamappa/llm_tp/actions/workflows/docker.yml)

Implementation of Neuro-Symbolic Task Planning combining Large Language Models (LLMs) with Symbolic Classical Planning (Fast Downward) and Plan Validation (VAL) across complex PDDL benchmarks.

---

## 📌 Project Summary & Completed Milestones

### 1. Neuro-Symbolic Planning Pipeline
- **Symbolic-LLM Planner (`symbolic-llm`)**: LLM decomposes high-level goals into multi-level subgoals. Each subgoal is solved sequentially using Fast Downward (`seq-opt-fdss-1`). Integrated with automated **Neuro-Symbolic Task Replanning** to recover from unreachable or failed states.
- **MCTS-LLM Planner (`mcts-llm`)**: Monte Carlo Tree Search exploring multiple candidate action trajectories ($n_s$), evaluated with sequence transition probabilities and symbolic applicability checks.
- **Fast Downward Baseline**: Pure classical PDDL planner baseline across all domain problem sizes.
- **Chain-of-Thought (CoT) Baseline**: Pure LLM reasoning baseline without symbolic verifiers.

### 2. Multi-Backend LLM Interface
- **vLLM (GPU / A100)**: High-throughput OpenAI-compatible server hosting local models (`Qwen/Qwen3-32B` / `Qwen2.5`).
- **Groq Cloud API**: High-speed cloud inference with automatic token-based sequence probability calibration and rate-limit handling.
- **Ollama**: Local lightweight inference on CPU / Mac Apple Silicon.
- **OpenAI**: Native support for GPT-4o / GPT-4 models.

### 3. PDDL Benchmark Domains
- **Barman**: Problem sizes 2 to 10 (cocktail mixing, shaker constraints, ingredient cleaning).
- **Blocksworld**: Problem sizes 3 to 10 (block stacking on tables, clear predicates).
- **Gripper**: Problem sizes 2 to 10 (robot multi-room object transport).

### 4. Plan Validation & Verification Engine
- Automated verification script (`validate_plans.py`) powered by the **VAL** plan validation tool.
- Verifies plan correctness, step applicability, and goal achievement, generating metric matrices for plan length, execution time, and success rate.

### 5. Production Docker Container & CI/CD
- Built on official `vllm/vllm-openai:v0.6.3` with CUDA 12.4 + PyTorch pre-configured.
- Fast Downward and VAL compiled from source directly inside the container.
- Automated GitHub Actions workflow publishing to **GitHub Container Registry (`ghcr.io`)**.

---

## 🚀 Quick Start with Docker (Recommended)

### 1. Pull the Pre-Built Docker Image
```bash
docker pull ghcr.io/rachanaramappa/llm_tp:latest
```

### 2. Run with Docker Commands

#### A. Start vLLM Model Server (on GPU / A100)
```bash
docker run --gpus all -d \
  --name vllm-server \
  -p 8000:8000 \
  --shm-size 16g \
  -v /path/to/model_weights:/model_cache:ro \
  -e MODEL_PATH=/model_cache/Qwen3-32B \
  ghcr.io/rachanaramappa/llm_tp:latest serve
```

#### B. Run All Experiments (FD + Symbolic-LLM + MCTS-LLM on All Domains)
```bash
docker run --rm --gpus all --network host \
  -v ./results:/app/experiments \
  -e LLM_BASE_URL=http://localhost:8000/v1 \
  ghcr.io/rachanaramappa/llm_tp:latest run-all
```

#### C. Run Specific Planners
```bash
# Run Symbolic-LLM
docker run --rm --network host \
  -v ./results:/app/experiments \
  -e LLM_BASE_URL=http://localhost:8000/v1 \
  ghcr.io/rachanaramappa/llm_tp:latest symbolic

# Run MCTS-LLM
docker run --rm --network host \
  -v ./results:/app/experiments \
  -e LLM_BASE_URL=http://localhost:8000/v1 \
  ghcr.io/rachanaramappa/llm_tp:latest mcts

# Run Fast Downward Baseline
docker run --rm \
  -v ./results:/app/experiments \
  ghcr.io/rachanaramappa/llm_tp:latest fd-baseline

# Validate All Generated Plans
docker run --rm --network host \
  -v ./results:/app/experiments \
  ghcr.io/rachanaramappa/llm_tp:latest validate
```

#### D. Interactive Container Shell
```bash
docker run --rm -it --network host \
  -v ./results:/app/experiments \
  ghcr.io/rachanaramappa/llm_tp:latest bash
```

---

## 🐳 Running via Docker Compose

```bash
# 1. Start the vLLM server only
docker compose up vllm-server

# 2. Run all experiments in a separate container connected to vLLM
docker compose run planner run-all

# 3. Run individual planners
docker compose run planner symbolic
docker compose run planner mcts
docker compose run planner validate

# 4. Interactive shell inside the planner container
docker compose run planner bash
```

---

## 💻 Local Conda Setup & Execution (Without Docker)

### 1. Environment Setup
```bash
# macOS
conda env create -f environment_mac.yml
conda activate llm_tp

# Linux
conda env create -f environment.yml
conda activate llm_tp
```

### 2. Configure Fast Downward & LLM Keys
```bash
# Export path to Fast Downward planner
export FD_PATH="$(pwd)/downward/fast-downward.py"
```

Configure `config.json`:
```json
{
  "LLM_BASE_URL": "https://api.groq.com/openai/v1",
  "LLM_API_KEY": "your_api_key_here",
  "LLM_MODEL": "qwen/qwen3.8-27b"
}
```

### 3. Run Experiments Locally

#### Symbolic-LLM Planner
```bash
python scripts/run_subgoal.py \
    --model qwen/qwen3.8-27b \
    --domain barman \
    --subgoal_planner symbolic-llm \
    --temperature 0.0 \
    --planner seq-opt-fdss-1 \
    --sizes 2 3 4 5 6 7 8 9 10 \
    --path "$FD_PATH"
```

#### MCTS-LLM Planner
```bash
python scripts/run_subgoal.py \
    --model qwen/qwen3.8-27b \
    --domain barman \
    --subgoal_planner mcts-llm \
    --temperature 0.0 \
    --ns 1 2 3 \
    --sizes 2 3 4 5 6 7 8 9 10
```

#### Fast Downward Baseline
```bash
python scripts/run_fd.py \
    --domain barman \
    --planner seq-opt-fdss-1 \
    --sizes 2 3 4 5 6 7 8 9 10 \
    --path "$FD_PATH"
```

#### Chain-of-Thought (CoT) Baseline
```bash
python scripts/run_llm.py \
    --model qwen/qwen3.8-27b \
    --domain barman \
    --temperature 0.0 \
    --sizes 2 3 4 5 6 7 8 9 10
```

#### Validate Generated Plans
```bash
python scripts/validate_plans.py \
    --domain barman \
    --problem_file experiments/barman/problem/barman2_1.pddl \
    --plan_file experiments/barman/plan/symbolic-llm/barman2_1.pddl
```

---

## 📂 Repository Layout

```
.
├── Dockerfile                  # Production GPU container definition (vLLM + FD + VAL)
├── docker-compose.yml          # Multi-service composition for vLLM & Planner
├── entrypoint.sh               # Unified container execution modes
├── push_to_ghcr.sh             # Helper script to build & push to GitHub Container Registry
├── export_for_server.sh        # Offline package export bundle for isolated servers
├── config.json                 # Active LLM endpoint and model configuration
├── domains/                    # PDDL domain definitions
│   ├── domain_barman.pddl
│   ├── domain_blocksworld.pddl
│   └── domain_gripper.pddl
├── experiments/                # Benchmark problems, generated plans, and results
│   ├── barman/
│   ├── blocksworld/
│   └── gripper/
├── scripts/                    # Core planning algorithms and execution scripts
│   ├── run_subgoal.py          # Runner for Symbolic-LLM & MCTS-LLM
│   ├── run_fd.py               # Fast Downward classical baseline runner
│   ├── run_llm.py              # Chain-of-Thought pure LLM runner
│   ├── subgoal.py              # Subgoal generation & task decomposition logic
│   ├── symbolic.py             # Interface to Fast Downward planner
│   ├── mcts.py                 # Monte Carlo Tree Search planning engine
│   └── validate_plans.py       # VAL plan validation and result aggregation
└── utils/                      # LLM utilities and prompt engineering
    ├── llm_functions.py        # Multi-backend LLM client, retries, and logprobs
    └── prompts.py              # In-context few-shot PDDL prompts
```

---

## 📑 Command Reference Table

| Goal | Command |
|---|---|
| **Pull Pre-built Docker Image** | `docker pull ghcr.io/rachanaramappa/llm_tp:latest` |
| **Start vLLM Server (Docker)** | `docker run --gpus all -d -p 8000:8000 ghcr.io/rachanaramappa/llm_tp:latest serve` |
| **Run All Benchmarks (Docker)** | `docker run --rm --network host ghcr.io/rachanaramappa/llm_tp:latest run-all` |
| **Run Symbolic-LLM (Docker)** | `docker run --rm --network host ghcr.io/rachanaramappa/llm_tp:latest symbolic` |
| **Run MCTS-LLM (Docker)** | `docker run --rm --network host ghcr.io/rachanaramappa/llm_tp:latest mcts` |
| **Run Validation (Docker)** | `docker run --rm --network host ghcr.io/rachanaramappa/llm_tp:latest validate` |
| **Run Compose Pipeline** | `docker compose up vllm-server` & `docker compose run planner run-all` |
| **Local Symbolic-LLM (Conda)** | `python scripts/run_subgoal.py --domain barman --subgoal_planner symbolic-llm --path "$FD_PATH"` |
| **Local MCTS-LLM (Conda)** | `python scripts/run_subgoal.py --domain barman --subgoal_planner mcts-llm --ns 1 2 3` |
| **Local FD Baseline (Conda)** | `python scripts/run_fd.py --domain barman --planner seq-opt-fdss-1 --path "$FD_PATH"` |
| **Local Plan Validation (Conda)**| `python scripts/validate_plans.py --domain barman` |