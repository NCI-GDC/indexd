#!/bin/bash
set -eo pipefail

PARAM=${1:-push};

IMAGE_NAME="${DOCKER_RELEASE_REGISTRY:=quay.io}/ncigdc/indexd"

# avoid installing git
COMMIT=$(git rev-parse HEAD) && echo "COMMIT=\"${COMMIT}\"" >indexd/index/version_data.py

# setup active branch name, default to using git if build is happening on local
if [ ${TRAVIS_BRANCH+x} ]; then
  GIT_BRANCH=$TRAVIS_BRANCH;
elif [ ${GITLAB_CI+x} ]; then
  GIT_BRANCH=${CI_COMMIT_REF_SLUG}-${CI_COMMIT_SHORT_SHA};
else
  GIT_BRANCH=$(git symbolic-ref --short -q HEAD);
fi

# replace slashes with underscore
GIT_BRANCH=${GIT_BRANCH/\//_}

VERSION=$(cat VERSION)
echo "$VERSION"

BUILD_COMMAND=(build \
  --label org.opencontainers.image.version="${VERSION}" \
  --label org.opencontainers.image.created="$(date -Iseconds)" \
  --label org.opencontainers.image.revision="${CI_COMMIT_SHORT_SHA}" \
  --label org.opencontainers.ref.name="indexd:${GIT_BRANCH}" \
  --ssh default -t "$IMAGE_NAME:$GIT_BRANCH")

if [ "$PARAM" = "push" ]; then
  docker push "$IMAGE_NAME:$GIT_BRANCH"
fi

if [ ! -z "$GITLAB_CI"  ]; then
  LEGACY_BRANCH_NAME=${CI_COMMIT_BRANCH/\//_}
  docker tag "$IMAGE_NAME:$GIT_BRANCH" "$IMAGE_NAME:$LEGACY_BRANCH_NAME"
  docker push "$IMAGE_NAME:$LEGACY_BRANCH_NAME"
fi
