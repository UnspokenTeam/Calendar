# Gateway

###### Gateway  для доступа к backend части Calendar

[![Build gateway](https://github.com/UnspokenTeam/Calendar/actions/workflows/build_gateway.yaml/badge.svg)](https://github.com/UnspokenTeam/Calendar/actions/workflows/build_gateway.yaml)

---

## Содержание

---
1. ### [**_Пример dotenv_**](#пример-dotenv)
2. ### [**_Установка_**](#установка)
    * [**_Перед установкой_**](#перед-установкой)
    * [**_Общие шаги_**](#общие-шаги)
    * [**_Docker_**](#docker)
    * [**_Local_**](#local)
3. ### [**_Документация_**](#документация)

## Пример dotenv

---

```env
; Хост для identity сервиса
IDENTITY_SERVICE_HOST="localhost"
; Порт для identity сервиса
IDENTITY_SERVICE_PORT="8080"
; Хост для event сервиса
EVENT_SERVICE_HOST="localhost"
; Порт для event сервиса
EVENT_SERVICE_PORT="8081"
; Хост для invite сервиса
INVITE_SERVICE_HOST="localhost"
; Порт для invite сервиса
INVITE_SERVICE_PORT="8082"
; Хост для notification сервиса
NOTIFICATION_SERVICE_HOST="localhost"
; Порт для notification сервиса
NOTIFICATION_SERVICE_PORT="8083"
; Url для подключения к локальному инстансу redis
REDIS_URL="redis://localhost:6543"
```

## Установка

---

### Перед установкой
1. Сделать ```docker pull``` для custom_postgres или подготовить собственный instance PostgreSQL
    ```bash
    docker pull ghcr.io/unspokenteam/custom_postgres:latest
    ```
2. Подготовить локальный инстанс redis ([Setup redis with docker](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/docker/))

### Общие шаги

1. Сделать ```docker pull``` для каждого сервиса или запусить их локально
    ```bash
    docker pull ghcr.io/unspokenteam/identity_service:latest
    docker pull ghcr.io/unspokenteam/event_service:latest
    docker pull ghcr.io/unspokenteam/invite_service:latest
    docker pull ghcr.io/unspokenteam/notification_service:latest
    ```
2. Следуя инструкции для каждого сервиса запустить контейнеры

### Docker
 
1. Склонировать gateway
    ```bash
    docker pull ghcr.io/unspokenteam/gateway:latest
    ```
2. В переменные вида **\*\_HOST** нужно прописать **host.docker.internal**
3. Запустить Gateway при помощи команды 
   ```bash
   docker run -d -p 8084:8084 --env-file $ENV_FILE_PATH ghcr.io/unspokenteam/gateway:latest
   ```

### Local
1. Перейти в папку gateway
2. Установить poetry для текущего проекта ([Poetry introduction](https://python-poetry.org/docs/))
3. Установить пакеты при помощи
   ```bash
   poetry install
   ```
4. Создать папку ```generated``` в папке ```app```
5. Сгенерировать прото файлы при помощи
   ```bash
   poetry run python -m grpc_tools.protoc -I ../shared/proto --python_out=app/generated --grpc_python_out=app/generated --pyi_out=app/generated ../shared/proto/event_service/*.proto ../shared/proto/invite_service/*.proto ../shared/proto/identity_service/*.proto ../shared/proto/user/*.proto
   poetry run protol --create-package --in-place --python-out app/generated protoc --proto-path=../shared/proto ../shared/proto/event_service/*.proto ../shared/proto/invite_service/*.proto ../shared/proto/identity_service/*.proto ../shared/proto/user/*.proto
   ```
6. Прописать переменные окружения в PyCharm или в dotenv файле (Если используется dotenv файл, то требуется в начало файла ```app/main.py``` вставить строчку ```dotenv.load_dotenv()``` предварительно импортировав пакет ```dotenv```)
7. Запустить проект при помощи
   ```bash
   poetry run uvicorn app.main:app
   ```

## Документация

---

Интерактивная документация будет запущена автоматически по пути ```http://localhost:8084/docs```