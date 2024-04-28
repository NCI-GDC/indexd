ARG BASE_VERSION=chore_add-service-install
ARG REGISTRY=dev-containers.osdc.io
ARG SERVICE_NAME=indexd
ARG PYTHON_VERSION=python3.7

FROM ${REGISTRY}/ncigdc/${PYTHON_VERSION}-builder:${BASE_VERSION} AS build
ARG SERVICE_NAME
ARG PIP_INDEX_URL
ARG PYTHON_VERSION
ARG USE_PYPI_VERSION="no"

WORKDIR /${SERVICE_NAME}
COPY . .
RUN bash /service-install.sh

FROM ${REGISTRY}/ncigdc/${PYTHON_VERSION}-httpd:${BASE_VERSION}
ARG NAME
ARG PYTHON_VERSION
ARG SERVICE_NAME
ARG GIT_BRANCH
ARG COMMIT
ARG BUILD_DATE

LABEL org.opencontainers.image.title="${SERVICE_NAME}" \
      org.opencontainers.image.description="${SERVICE_NAME} container image" \
      org.opencontainers.image.source="https://github.com/NCI-GDC/${SERVICE_NAME}" \
      org.opencontainers.image.vendor="NCI GDC" \
      org.opencontainers.image.ref.name="${SERVICE_NAME}:${GIT_BRANCH}" \
      org.opencontainers.image.revision="${COMMIT}" \
      org.opencontainers.image.created="${BUILD_DATE}"

RUN dnf install -y libpq-15.0

RUN mkdir -p /var/www/${SERVICE_NAME}/ \
  && chmod 777 /var/www/${SERVICE_NAME}

COPY wsgi.py /var/www/${SERVICE_NAME}/
COPY --from=build /venv/lib/${PYTHON_VERSION}/site-packages /venv/lib/${PYTHON_VERSION}/site-packages

# Make indexd CLI utilities available for, e.g., DB schema migration.
COPY --from=build /venv/bin/indexd /venv/bin
COPY --from=build /venv/bin/index_admin.py /venv/bin
COPY --from=build /venv/bin/migrate_index.py /venv/bin


WORKDIR /var/www/${SERVICE_NAME}
