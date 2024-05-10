FROM python:3.11-slim as python-base

ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

ENV POETRY_CACHE_DIR=/opt/.cache

FROM python-base as poetry-base

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM python-base as example-app

RUN apt-get update && apt-get install -y protobuf-compiler

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY shared ./shared

WORKDIR /app/invite_service

COPY invite_service/poetry.lock ./invite_service/pyproject.toml ./

RUN poetry install --no-interaction --no-cache --without dev

COPY invite_service ./

RUN mkdir ./src/generated

RUN poetry run python -m grpc_tools.protoc -I ../shared/proto --python_out=./src/generated --grpc_python_out=./src/generated --pyi_out=./src/generated ../shared/proto/user/*.proto ../shared/proto/invite_service/*.proto
RUN poetry run protol --create-package --in-place --python-out ./src/generated protoc  --experimental_allow_proto3_optional --proto-path=../shared/proto ../shared/proto/invite_service/*.proto ../shared/proto/user/*.proto

RUN poetry run prisma generate

EXPOSE 8082

CMD poetry run python -m src.main
