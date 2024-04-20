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

RUN poetry run python -m grpc_tools.protoc -I ./identity_service/proto --python_out=app/identity_service_proto --grpc_python_out=app/identity_service_proto --pyi_out=app/identity_service_proto ./identity_service/proto/identity_service.proto ./identity_service/proto/auth.proto ./identity_service/proto/delete_user.proto ./identity_service/proto/get_access_token.proto ./identity_service/proto/get_user.proto ./identity_service/proto/update_user.proto && poetry run protol --create-package --in-place --python-out app/identity_service_proto protoc --proto-path=./identity_service/proto ./identity_service/proto/identity_service.proto ./identity_service/proto/auth.proto ./identity_service/proto/delete_user.proto ./identity_service/proto/get_access_token.proto ./identity_service/proto/get_user.proto ./identity_service/proto/update_user.proto
RUN poetry run python -m grpc_tools.protoc -I ./event_service/proto --python_out=app/event_service_proto --grpc_python_out=app/event_service_proto --pyi_out=app/event_service_proto ./event_service/proto/event_service.proto && poetry run protol --create-package --in-place --python-out app/event_service_proto protoc --proto-path=./event_service/proto ./event_service/proto/event_service.proto
RUN poetry run python -m grpc_tools.protoc -I ./invite_service/proto --python_out=app/invite_service_proto --grpc_python_out=app/invite_service_proto --pyi_out=app/invite_service_proto ./invite_service/proto/invite_service.proto && poetry run protol --create-package --in-place --python-out app/invite_service_proto protoc --proto-path=./invite_service/proto ./invite_service/proto/invite_service.proto

COPY . /app

EXPOSE 8084

CMD poetry run uvicorn main:app
