FROM python:3.11 as python-base

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
RUN poetry run python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. --pyi_out=. ./proto/event_service.proto

EXPOSE 8080
CMD [ "poetry", "run", "python", "main.py" ]