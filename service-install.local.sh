#!/usr/bin/env bash
set -euox pipefail

# should install make use of published wheel?
if [ "${USE_PYPI_VERSION}" = "yes" ]; then
  pip install versionista=="${VERSIONISTA_VERSION:="1.0.1dev4"}"
  VERSION=$(python -m setuptools_scm)
  INSTALL_CMD=${SERVICE_NAME}==${VERSION}
else
  INSTALL_CMD="--no-deps ."
fi

pip install --no-deps -r requirements.txt --index-url="$PIP_INDEX_URL"
pip install --index-url="$PIP_INDEX_URL" "${INSTALL_CMD}"
