# Multi-stage build for Neuro-Symbolic Task Planning with vLLM + Qwen3-32B
# IMPORTANT: Built for linux/amd64 (matches the A100 server's architecture).
# Model weights are NOT baked into this image (too large for laptop builds).
# They are downloaded separately and mounted as a volume at runtime.
FROM --platform=linux/amd64 nvidia/cuda:12.4.1-devel-ubuntu22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/model_cache/huggingface \
    VLLM_WORKER_MULTIPROC_METHOD=spawn

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
    wget \
    python3.11 \
    python3.11-dev \
    python3-pip \
    libopenblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

RUN python3.11 -m pip install --upgrade pip setuptools wheel

WORKDIR /app

COPY requirements-docker.txt /tmp/requirements-docker.txt
RUN python3.11 -m pip install -r /tmp/requirements-docker.txt

RUN mkdir -p /app/scripts /app/domains /app/prompts /app/utils /app/experiments /model_cache

COPY . /app/

RUN mkdir -p /app/bin
COPY entrypoint.sh /app/bin/entrypoint.sh
RUN chmod +x /app/bin/entrypoint.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/bin/entrypoint.sh"]
CMD ["serve"]
