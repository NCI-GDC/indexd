#!/bin/bash
set -euox pipefail

export DOCKER_BUILDKIT=1

NAME="indexd"
PARAM=${1:-DO_NOT_PUSH};

BASE_CONTAINER_VERSION=1.2.0  # upgrade later

IMAGE_NAME="${DOCKER_RELEASE_REGISTRY:=quay.io}/ncigdc/${NAME}"
REGISTRY="${BASE_CONTAINER_REGISTRY:=quay.io}"

if [ -f 'VERSION.txt' ]; then
  VERSION=$(cat VERSION.txt)
else
  VERSION=$(python -m setuptools_scm)
fi

# setup active branch name, default to using git if build is happening on local
if [ ${TRAVIS_BRANCH+x} ]; then
  GIT_BRANCH=$TRAVIS_BRANCH;
elif [ ${GITLAB_CI+x} ]; then
  GIT_BRANCH=${CI_COMMIT_REF_NAME};
else
  GIT_BRANCH=$(git symbolic-ref --short -q HEAD);
fi

# replace slashes with underscore
GIT_BRANCH=${GIT_BRANCH/\//_}

# avoid installing git
COMMIT=$(git rev-parse HEAD)

echo "COMMIT=\"${COMMIT}\"" > indexd/index/version_data.py

BUILD_COMMAND=(build \
  --label org.opencontainers.image.version="${VERSION}" \
  --label org.opencontainers.image.created="$(date -Iseconds)" \
  --label org.opencontainers.image.revision="${COMMIT}" \
  --label org.opencontainers.ref.name="${NAME}:${GIT_BRANCH}" \
  --build-arg REGISTRY="${REGISTRY%\/ncigdc}" \
  --build-arg BASE_VERSION="${BASE_CONTAINER_VERSION:=1.2.0}" \
  --build-arg PIP_INDEX_URL \
  --build-arg REQUIREMENTS_GDC_LIBRARIES_FILE \
  --ssh default \
  -t "$IMAGE_NAME:$GIT_BRANCH" \
  -t "$IMAGE_NAME:$COMMIT"
)

echo "$COMMIT" > DOCKER_TAG.txt

touch "${REQUIREMENTS_GDC_LIBRARIES_FILE}"
cat "${REQUIREMENTS_GDC_LIBRARIES_FILE}"
docker "${BUILD_COMMAND[@]}" . --progress=plain
rm "${REQUIREMENTS_GDC_LIBRARIES_FILE}"


if [ "$PARAM" = "push" ]; then
  docker image ls "$IMAGE_NAME"
  docker push -a "$IMAGE_NAME"
fi
