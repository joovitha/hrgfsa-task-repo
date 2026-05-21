#!/bin/bash
set -e

DOCKERHUB_USERNAME="${DOCKERHUB_USERNAME:?DOCKERHUB_USERNAME is required}"
DOCKERHUB_TOKEN="${DOCKERHUB_TOKEN:?DOCKERHUB_TOKEN is required}"
IMAGE_NAME="${IMAGE_NAME:-devops-app}"
IMAGE_TAG="${IMAGE_TAG:-latest1}"
IMAGE="docker.io/$DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG"

echo "$DOCKERHUB_TOKEN" | docker login --username "$DOCKERHUB_USERNAME" --password-stdin
docker build -t "$IMAGE" ./app
docker push "$IMAGE"

echo "Built and pushed $IMAGE"
if [ -n "${IMAGE_OUTPUT_FILE:-}" ]; then
echo "IMAGE=$IMAGE" > "$IMAGE_OUTPUT_FILE"
fi
