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

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./

RUN poetry install --no-interaction --no-cache --without dev

COPY . /app
RUN mkdir generated
RUN echo "from . import *" | cat >> ./generated/__init__.py
RUN poetry run python -m grpc_tools.protoc -I proto --python_out=generated --grpc_python_out=generated --pyi_out=generated ./proto/identity_service.proto ./proto/auth.proto ./proto/delete_user.proto ./proto/get_access_token.proto ./proto/get_user.proto ./proto/update_user.proto
RUN poetry run 2to3 ./generated  -w -n
RUN poetry run prisma generate

EXPOSE 8080
CMD poetry run prisma db push && poetry run python main.py
