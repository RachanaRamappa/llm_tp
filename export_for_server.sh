#!/bin/bash
# ==============================================================================
# Export Docker image + model weights for transfer to offline A100 server
# ==============================================================================
# Run this AFTER:
#   1. Building the Docker image (docker buildx build ...)
#   2. Downloading the model (./download_model.sh)
#
# This creates two files ready for transfer:
#   - llm-task-planner-image.tar.gz  (~10-15 GB compressed Docker image)
#   - model_cache/                    (~65 GB model weights — copy as-is)
#
# Usage:
#   chmod +x export_for_server.sh
#   ./export_for_server.sh
# ==============================================================================

set -e

IMAGE_NAME="llm-task-planner:latest"
EXPORT_DIR="./export"
IMAGE_TAR="$EXPORT_DIR/llm-task-planner-image.tar.gz"

echo "========================================"
echo "  Export for Offline A100 Server"
echo "========================================"

# --- Step 1: Check Docker image exists ---
echo ""
echo "[1/4] Checking Docker image..."
if docker image inspect "$IMAGE_NAME" > /dev/null 2>&1; then
    IMAGE_SIZE=$(docker image inspect "$IMAGE_NAME" --format='{{.Size}}' | awk '{printf "%.1f GB\n", $1/1024/1024/1024}')
    echo "  ✓ Image found: $IMAGE_NAME ($IMAGE_SIZE)"
else
    echo "  ✗ Image '$IMAGE_NAME' not found!"
    echo "  Build it first:"
    echo "    docker buildx build --platform linux/amd64 -t $IMAGE_NAME ."
    exit 1
fi

# --- Step 2: Check model weights ---
echo ""
echo "[2/4] Checking model weights..."
if [ -d "./model_cache/Qwen3-32B" ]; then
    MODEL_SIZE=$(du -sh ./model_cache/Qwen3-32B | cut -f1)
    echo "  ✓ Model weights found: ./model_cache/Qwen3-32B ($MODEL_SIZE)"
else
    echo "  ✗ Model weights not found at ./model_cache/Qwen3-32B"
    echo "  Download first: ./download_model.sh"
    exit 1
fi

# --- Step 3: Save Docker image ---
echo ""
echo "[3/4] Saving Docker image to $IMAGE_TAR ..."
echo "  This will take several minutes..."
mkdir -p "$EXPORT_DIR"
docker save "$IMAGE_NAME" | gzip > "$IMAGE_TAR"
SAVED_SIZE=$(du -sh "$IMAGE_TAR" | cut -f1)
echo "  ✓ Image saved: $IMAGE_TAR ($SAVED_SIZE)"

# --- Step 4: Create server setup script ---
echo ""
echo "[4/4] Creating server setup script..."
cat > "$EXPORT_DIR/server_run.sh" << 'SERVER_SCRIPT'
#!/bin/bash
# ==============================================================================
# Run on the A100 server (no internet needed)
# ==============================================================================
# Transfer these files to the server:
#   1. llm-task-planner-image.tar.gz  (this directory)
#   2. model_cache/Qwen3-32B/         (model weights)
#
# Then run this script:
#   chmod +x server_run.sh
#   ./server_run.sh
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================"
echo "  A100 Server Setup (Offline)"
echo "========================================"

# --- Load Docker image ---
echo ""
echo "[1/3] Loading Docker image..."
if docker image inspect "llm-task-planner:latest" > /dev/null 2>&1; then
    echo "  Image already loaded, skipping..."
else
    echo "  Loading from llm-task-planner-image.tar.gz ..."
    docker load < "$SCRIPT_DIR/llm-task-planner-image.tar.gz"
    echo "  ✓ Image loaded"
fi

# --- Verify model weights ---
echo ""
echo "[2/3] Checking model weights..."
MODEL_DIR="${SCRIPT_DIR}/../model_cache/Qwen3-32B"
if [ ! -d "$MODEL_DIR" ]; then
    MODEL_DIR="${SCRIPT_DIR}/model_cache/Qwen3-32B"
fi
if [ ! -d "$MODEL_DIR" ]; then
    echo "  ✗ Model weights not found!"
    echo "  Expected at: $MODEL_DIR"
    echo "  Make sure you transferred the model_cache/Qwen3-32B directory"
    exit 1
fi
echo "  ✓ Model weights at: $MODEL_DIR"

# --- Create results directory ---
mkdir -p "$SCRIPT_DIR/results"

echo ""
echo "[3/3] Ready to run!"
echo ""
echo "========================================"
echo "  COMMANDS"
echo "========================================"
echo ""
echo "# Start vLLM server (run this first, keep it running):"
echo "docker run --rm -d --gpus all --name vllm-server \\"
echo "  -v $MODEL_DIR:/model_cache/Qwen3-32B:ro \\"
echo "  -e MODEL_PATH=/model_cache/Qwen3-32B \\"
echo "  -p 8000:8000 --shm-size 16g \\"
echo "  llm-task-planner:latest serve"
echo ""
echo "# Wait ~2 min for server to load, then check:"
echo "curl http://localhost:8000/v1/models -H 'Authorization: Bearer local-key'"
echo ""
echo "# Run ALL experiments (FD + Symbolic-LLM + MCTS-LLM on all 3 domains):"
echo "docker run --rm --gpus all --network host \\"
echo "  -v $SCRIPT_DIR/results:/app/experiments \\"
echo "  -e LLM_BASE_URL=http://localhost:8000/v1 \\"
echo "  llm-task-planner:latest run-all"
echo ""
echo "# Or run specific planners:"
echo "docker run --rm --network host \\"
echo "  -v $SCRIPT_DIR/results:/app/experiments \\"
echo "  -e LLM_BASE_URL=http://localhost:8000/v1 \\"
echo "  llm-task-planner:latest mcts"
echo ""
echo "# Interactive shell:"
echo "docker run --rm -it --network host \\"
echo "  -v $SCRIPT_DIR/results:/app/experiments \\"
echo "  -e LLM_BASE_URL=http://localhost:8000/v1 \\"
echo "  llm-task-planner:latest bash"
echo ""
echo "# Validate all plans:"
echo "docker run --rm --network host \\"
echo "  -v $SCRIPT_DIR/results:/app/experiments \\"
echo "  llm-task-planner:latest validate"
echo ""
echo "========================================"
SERVER_SCRIPT

chmod +x "$EXPORT_DIR/server_run.sh"
echo "  ✓ Created $EXPORT_DIR/server_run.sh"

echo ""
echo "========================================"
echo "  EXPORT COMPLETE"
echo "========================================"
echo ""
echo "Files to transfer to the A100 server:"
echo "  1. $IMAGE_TAR"
echo "  2. ./model_cache/Qwen3-32B/  (entire directory)"
echo ""
echo "Transfer method options:"
echo "  • USB drive / external SSD"
echo "  • scp / rsync (if you have temporary network access)"
echo "  • Shared network storage"
echo ""
echo "On the server, run:"
echo "  ./export/server_run.sh"
echo "========================================"
