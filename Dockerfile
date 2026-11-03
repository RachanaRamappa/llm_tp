# ==============================================================================
# Neuro-Symbolic Task Planning — Offline A100 / GPU Docker Image with vLLM
# ==============================================================================
# This image contains:
#   1. vLLM server (pre-installed official vLLM + PyTorch + CUDA stack)
#   2. Fast Downward (symbolic PDDL planner, built from source)
#   3. VAL (PDDL plan validator, built from source)
#   4. All project code (PDDL domains, problems, prompts, and runners)
#
# Base image: Official vLLM OpenAI image (CUDA 12 + PyTorch + vLLM ready to go)
# ==============================================================================

FROM vllm/vllm-openai:v0.6.3

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    VLLM_WORKER_MULTIPROC_METHOD=spawn

USER root

# ---------- System packages for Fast Downward & VAL ----------
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
    graphviz \
    libopenblas-dev \
    liblapack-dev \
    libgmp-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# ======================================================================
# STAGE 1: Build Fast Downward (symbolic PDDL planner)
# ======================================================================
RUN git clone --depth 1 https://github.com/aibasel/downward.git /opt/downward && \
    cd /opt/downward && \
    python3 build.py

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

# Make VAL and Fast Downward accessible on PATH
ENV PATH="/opt/VAL/bin:/opt/downward:${PATH}" \
    FD_PATH="/opt/downward/fast-downward.py"

# ======================================================================
# STAGE 3: Install Project-Specific Python dependencies
# ======================================================================
WORKDIR /app

RUN pip install --no-cache-dir \
    pddlpy==0.4.4 \
    antlr4-python3-runtime==4.13.1 \
    python-graphviz==0.20.3 \
    networkx==3.1

# ======================================================================
# STAGE 4: Copy project code
# ======================================================================
RUN mkdir -p /app/scripts /app/domains /app/utils \
             /app/experiments /model_cache /app/results

COPY . /app/

# Ensure __init__.py exists for Python package imports
RUN touch /app/scripts/__init__.py /app/utils/__init__.py

# Make entrypoint executable
RUN if [ -f /app/entrypoint.sh ]; then \
        mkdir -p /app/bin && cp /app/entrypoint.sh /app/bin/entrypoint.sh && chmod +x /app/bin/entrypoint.sh; \
    fi

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
