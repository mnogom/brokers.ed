# Universal Dockerfile. To use it, set ARG BUILD_SOURCE=<path-to-source-code>

ARG IMAGE_NAME=python
ARG IMAGE_VERSION=3.12-alpine3.20

ARG BUILD_SOURCE

ARG POETRY_HOME=/etc/poetry
ARG POETRY_PATH=$POETRY_HOME/bin
ARG HOME_PATH=/root
ARG PROJECT_PATH=$HOME_PATH/app
ARG DIST_PATH=$PROJECT_PATH/dist

FROM $IMAGE_NAME:$IMAGE_VERSION AS build
ARG POETRY_HOME
ARG POETRY_PATH
ARG PROJECT_PATH
ARG DIST_PATH
ARG BUILD_SOURCE

LABEL maintainer="Konstantin Freidlin"
LABEL description="ZMQ Req/Rep :: Build"
LABEL version="0.1.0"

WORKDIR $PROJECT_PATH

ENV PATH="$PATH:$POETRY_PATH"

RUN apk update && apk add curl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=$POETRY_HOME python3 -

COPY ./$BUILD_SOURCE/pyproject.toml ./$BUILD_SOURCE/poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-cache --no-root

COPY ./$BUILD_SOURCE/README.md ./
COPY ./$BUILD_SOURCE/src/ ./src/
RUN poetry build --directory $DIST_PATH

CMD [ "/bin/sh" ]

FROM $IMAGE_NAME:$IMAGE_VERSION

LABEL maintainer="Konstantin Freidlin"
LABEL description="ZMQ Req/Rep"
LABEL version="0.1.0"

ARG DIST_PATH
ARG BUILD_SOURCE

COPY --from=build $DIST_PATH /usr/src/
RUN pip3 install --no-cache-dir /usr/src/*.whl
COPY ./$BUILD_SOURCE/entrypoint.sh /

ENTRYPOINT [ "/entrypoint.sh" ]
