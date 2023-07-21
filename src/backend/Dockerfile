ARG BASE_IMAGE_TAG="3.11-slim"

FROM docker.io/amd64/python:${BASE_IMAGE_TAG}
ARG IMAGE_VERSION
ARG TZ='America/Montreal'
ENV TZ="${TZ}"
ENV APP_VERSION="${IMAGE_VERSION}"
ENV OCI_USER='runtimeuser'
ENV OCI_USER_ID='1001'

# https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.vendor="Testruction" \
      org.opencontainers.image.authors='Florian JUDITH <florian.judith.b@gmail.com>' \
      org.opencontainers.image.version=${IMAGE_VERSION} \
	  org.opencontainers.image.title="Banckend Service Demo" \
	  org.opencontainers.image.description="MVC based FastAPI backend connected to relational database using SqlAlchemy" \
      org.opencontainers.image.base.name="docker.io/amd64/python:${BASE_IMAGE_TAG}" \
      org.opencontainers.image.source="https://github.com/testruction/fastapi-sqlalchemy-cockroachdb"

USER root

# Create the internal user
RUN groupadd --gid="${OCI_USER_ID}" "${OCI_USER}" \
    && useradd --uid="${OCI_USER_ID}" --gid=${OCI_USER_ID} --system "${OCI_USER}"

# Copy app source code
COPY ./ /usr/local/app/
WORKDIR /usr/local/app/

# Python Build
RUN python3 -m pip install --upgrade pip \
    && pip install -e .[tests,dev] \
    && pip uninstall -y webdemo-backendservice

# Startup admission control
COPY ./entrypoint.sh /entrypoint.sh
RUN chown -R ${OCI_USER}:${OCI_USER} \
        /entrypoint.sh \
        /usr/local/app/ \
    && chmod -R a+x \
        /entrypoint.sh \
        /usr/local/app/

EXPOSE 8000

# Activation de l'utilisateur intégré
USER ${OCI_USER}

WORKDIR /usr/local/app/src
ENTRYPOINT [ "/entrypoint.sh" ]
# CMD ["uvicorn", "--host=0.0.0.0", "--port=8000", "asgi:app"]
CMD ["hypercorn", "--bind=0.0.0.0:8000", "asgi:app"]
