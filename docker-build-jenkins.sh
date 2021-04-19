#!/usr/bin/env bash
set -euo pipefail
export DOCKER_BUILDKIT=1

# Build and push docker image.
docker build --ssh default -t ${REGISTRY}/${REPO}:${GIT_TAG} . --build-arg http_proxy=https://cloud-proxy:3128 --build-arg https_proxy=https://cloud-proxy:3128
docker push ${REGISTRY}/${REPO}:${GIT_TAG}

# Clean up docker image after pushing
docker rmi ${REGISTRY}/${REPO}:${GIT_TAG}

# Do a soft prune
docker system prune -f --volumes
