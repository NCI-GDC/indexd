#!/usr/bin/env bash
set -euox pipefail

PARAM=${1:-DO_NOT_PUSH};

SERVICE_NAME="indexd"
PIP_INDEX_URL=https://nexus.osdc.io/repository/pypi-all/simple
NEXUS_HOST=${PIP_INDEX_HOST:="nexus.osdc.io:172.23.11.116"}
IMAGE_NAME="${CONTAINER_REGISTRY:=dev-containers.osdc.io}/ncigdc/${SERVICE_NAME}"

# setup active branch name, default to using git if build is happening on local
if [ -z ${GIT_BRANCH+x} ]; then
  GIT_BRANCH=$(git symbolic-ref --short -q HEAD);
fi

# replace slashes with underscore
GIT_BRANCH=${GIT_BRANCH/\//_}
# Save the commit hash so the /status endpoint doesn't need Git.
COMMIT=$(git rev-parse HEAD)

# should install make use of published wheel?
if [ ${USE_PYPI_VERSION+x} ]; then
  VERSION=$(python -m setuptools_scm)
  INSTALL_CMD=${SERVICE_NAME}==${VERSION}
else
  INSTALL_CMD="--no-deps .";
fi

BUILD_COMMAND=(build \
  --build-arg SERVICE_NAME="${SERVICE_NAME}" \
  --build-arg COMMIT="${COMMIT}" \
  --build-arg BUILD_DATE="$(date -Iseconds)" \
  --build-arg PIP_INDEX_URL="${PIP_INDEX_URL}" \
  --build-arg APP_INSTALL_CMD="${INSTALL_CMD}" \
  --add-host "${NEXUS_HOST}" \
  -t "$IMAGE_NAME:$GIT_BRANCH" \
  -t "$IMAGE_NAME:$COMMIT" \
  -t "$IMAGE_NAME:${COMMIT:0:8}" \
  -t "$IMAGE_NAME:$GIT_BRANCH-${COMMIT:0:8}"
)

docker "${BUILD_COMMAND[@]}" . --progress=plain
if [ "$PARAM" = "push" ]; then
  docker push -a "$IMAGE_NAME"
fi
