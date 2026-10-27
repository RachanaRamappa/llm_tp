#!/bin/bash
# ==============================================================================
# Download Qwen3-32B model weights for offline vLLM deployment
# ==============================================================================
# Run this on a machine WITH internet before transferring to the A100 server.
#
# Usage:
#   chmod +x download_model.sh
#   ./download_model.sh
#
# This downloads the full Qwen3-32B model (~65GB) to ./model_cache/Qwen3-32B
# ==============================================================================

set -e

MODEL_ID="${1:-Qwen/Qwen3-32B}"
DOWNLOAD_DIR="./model_cache/Qwen3-32B"

echo "========================================"
echo "  Model Download for Offline Deployment"
echo "========================================"
echo "Model    : $MODEL_ID"
echo "Save to  : $DOWNLOAD_DIR"
echo "========================================"
echo ""

# Install huggingface_hub if not available
if ! python3 -c "import huggingface_hub" 2>/dev/null; then
    echo "Installing huggingface_hub..."
    pip install huggingface_hub[cli]
fi

# Create download directory
mkdir -p "$DOWNLOAD_DIR"

echo "Downloading model weights..."
echo "This may take a while (~65GB for Qwen3-32B)..."
echo ""

# Download using huggingface-cli (resumes if interrupted)
huggingface-cli download "$MODEL_ID" \
    --local-dir "$DOWNLOAD_DIR" \
    --local-dir-use-symlinks False

echo ""
echo "========================================"
echo "  Download Complete!"
echo "========================================"
echo "Model saved to: $DOWNLOAD_DIR"
echo ""
echo "Contents:"
ls -lh "$DOWNLOAD_DIR"
echo ""
echo "Total size:"
du -sh "$DOWNLOAD_DIR"
echo ""
echo "Next step: Run ./export_for_server.sh to package everything"
echo "========================================"
