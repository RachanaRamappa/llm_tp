# ==============================================================================
# Neuro-Symbolic Task Planning — Offline A100 Docker Image
# ==============================================================================
# This image contains:
#   1. vLLM server (serves Qwen3-32B for LLM inference)
#   2. Fast Downward (symbolic PDDL planner, built from source)
#   3. VAL (PDDL plan validator, built from source)
#   4. All project code + Python dependencies
#
# Model weights are NOT inside the image — mount them at /model_cache
# Build:   docker buildx build --platform linux/amd64 -t llm-task-planner:latest .
# ==============================================================================

FROM --platform=linux/amd64 nvidia/cuda:12.4.1-devel-ubuntu22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    VLLM_WORKER_MULTIPROC_METHOD=spawn

# ---------- System packages ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    cmake \
    curl \
    flex \
    bison \
    g++ \
    git \
    wget \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    libopenblas-dev \
    liblapack-dev \
    libgmp-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Make python3.11 the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

RUN python3.11 -m pip install --upgrade pip setuptools wheel

# ======================================================================
# STAGE 1: Build Fast Downward (symbolic PDDL planner)
# ======================================================================
RUN git clone --depth 1 https://github.com/aibasel/downward.git /opt/downward && \
    cd /opt/downward && \
    python3.11 build.py

# ======================================================================
# STAGE 2: Build VAL (PDDL plan validator)
# ======================================================================
RUN git clone --depth 1 https://github.com/KCL-Planning/VAL.git /tmp/VAL && \
    cd /tmp/VAL && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=/opt/VAL && \
    make -j$(nproc) && \
    make install && \
    rm -rf /tmp/VAL

# Make VAL accessible on PATH
ENV PATH="/opt/VAL/bin:/opt/downward:${PATH}"

# ======================================================================
# STAGE 3: Install Python dependencies
# ======================================================================
WORKDIR /app

COPY requirements-docker.txt /tmp/requirements-docker.txt
RUN python3.11 -m pip install -r /tmp/requirements-docker.txt && \
    rm /tmp/requirements-docker.txt

# ======================================================================
# STAGE 4: Copy project code
# ======================================================================
# Create directory structure
RUN mkdir -p /app/scripts /app/domains /app/prompts /app/utils \
             /app/experiments /model_cache /app/results

# Copy everything
COPY . /app/

# Ensure __init__.py exists for Python package imports
RUN touch /app/scripts/__init__.py /app/utils/__init__.py

# Make entrypoint executable
COPY entrypoint.sh /app/bin/entrypoint.sh
RUN mkdir -p /app/bin && chmod +x /app/bin/entrypoint.sh

# ======================================================================
# STAGE 5: Configure environment
# ======================================================================
ENV HF_HOME=/model_cache/huggingface \
    TRANSFORMERS_CACHE=/model_cache/huggingface \
    TORCH_HOME=/model_cache/torch \
    FD_PATH=/opt/downward/fast-downward.py \
    VLLM_WORKER_MULTIPROC_METHOD=spawn

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/bin/entrypoint.sh"]
CMD ["serve"]
