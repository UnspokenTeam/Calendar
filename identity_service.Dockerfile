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

WORKDIR /app/identity_service

COPY identity_service/poetry.lock ./identity_service/pyproject.toml ./

RUN poetry install --no-interaction --no-cache --without dev

RUN mkdir generated

COPY identity_service ./

RUN poetry run python -m grpc_tools.protoc -I ../shared/proto --python_out=generated --grpc_python_out=generated --pyi_out=generated ../shared/proto/identity_service/*.proto ../shared/proto/user/*.proto
RUN poetry run protol --create-package --in-place --python-out generated protoc --proto-path=../shared/proto ../shared/proto/identity_service/*.proto ../shared/proto/user/*.proto

RUN poetry run prisma generate

EXPOSE 8080

CMD poetry run prisma db push && poetry run python main.py
