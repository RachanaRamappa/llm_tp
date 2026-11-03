#!/bin/bash
# ==============================================================================
# Helper to build and push Docker image to GitHub Container Registry (ghcr.io)
# ==============================================================================
# Prerequisites:
#   A GitHub Personal Access Token (classic) with `write:packages` permission.
#   Create one at: https://github.com/settings/tokens
#
# Usage:
#   export CR_PAT="ghp_your_github_token"
#   ./push_to_ghcr.sh
# ==============================================================================

set -e

IMAGE_NAME="ghcr.io/rachanaramappa/llm_tp:latest"

echo "========================================================"
echo "  Publishing vLLM + Task Planner to GitHub Container Registry"
echo "  Target: $IMAGE_NAME"
echo "========================================================"

if [ -n "$CR_PAT" ]; then
    echo "[1/3] Logging in to ghcr.io using \$CR_PAT..."
    echo "$CR_PAT" | docker login ghcr.io -u RachanaRamappa --password-stdin
else
    echo "[1/3] Checking ghcr.io login status..."
    echo "If not logged in, run: export CR_PAT='your_token' or 'docker login ghcr.io -u RachanaRamappa'"
fi

echo ""
echo "[2/3] Building Docker image for linux/amd64 (A100 / GPU server)..."
docker buildx build --platform linux/amd64 -t "$IMAGE_NAME" . --load

echo ""
echo "[3/3] Pushing to GitHub Container Registry..."
docker push "$IMAGE_NAME"

echo ""
echo "========================================================"
echo "  SUCCESSFULLY PUBLISHED!"
echo "  Docker Link for Guide:"
echo "    https://github.com/RachanaRamappa/llm_tp/pkgs/container/llm_tp"
echo "  Pull Command for Guide:"
echo "    docker pull $IMAGE_NAME"
echo "========================================================"
