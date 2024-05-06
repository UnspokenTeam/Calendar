___
# Identity service
[![Build identity service](https://github.com/UnspokenTeam/Calendar/actions/workflows/build_identity_service.yaml/badge.svg)](https://github.com/UnspokenTeam/Calendar/actions/workflows/build_identity_service.yaml)
___
**Установка и описание**
___
1. **Образец .env файла**
	```env
    ; Ключ для генерации Access token
    ACCESS_SECRET="ACCESS_SECRET"
    ; Ключ для генерации Refresh token
    REFRESH_SECRET="REFRESH_SECRET"
    ; Адрес базы данных
	DATABASE_URL="DATABASE_URL"
    ; Вид окружения
	ENVIRONMENT="ENVIRONMENT"
    ; Время истечения срока валидности Refresh token в днях
    REFRESH_TOKEN_EXPIRATION=30
    ; Время истечения срока валидности Access token в минутах
    ACCESS_TOKEN_EXPIRATION=15
	```
___
2. **Установка**:
___  
**Перед установкой**:

1. Сделать ```docker pull``` для custom_postgres или подготовить собственный instance PostgreSQL
```bash
docker pull ghcr.io/unspokenteam/custom_postgres:latest
```
2. Подготовить локальный инстанс redis ([Setup redis with docker](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/docker/))
___  
   - Далее доступно несколько способов установки:

     1. **Через docker**
        - Установка осуществляется через **docker**, для установки пакета микросервиса введите и выполните команду:
         ```bash
         docker pull ghcr.io/unspokenteam/identity_service:latest
          ```
        - Создайте .env файл, укажите его путь в команде и выполните её:
         ```bash
         docker run -d -p 8080=8080 —env-file $PATH_TO_ENV ghcr.io/unspokenteam/identity_service:latest
          ```

     2. **Через poetry**
         - Также возможен локальный запуск при помощи утилиты poetry **без использования docker'a**. Для этого введите и выполните команду:
         ```bash
         poetry install
         ```
         - Сгенерируйте proto файлы, выполнив команду:
         ```bash
         poetry run python -m grpc_tools.protoc -I ../shared/proto --python_out=generated --grpc_python_out=generated --pyi_out=generated ../shared/proto/user/*.proto ../shared/proto/identity_service/*.proto && poetry run protol --create-package --in-place --python-out generated protoc --proto-path=../shared/proto ../shared/proto/identity_service/*.proto ../shared/proto/user/*.proto
         ```
         - Сгенерируйте prisma клиент, выполнив команду:
         ```bash
         poetry run prisma generate
         ```
         - Создайте .env файл в папке микросервиса. Добавьте вызов load_dotenv из модуля dotenv в методе serve в файле main.py и выполните команду:
         ```bash
         poetry run python main.py
         ```
---
3. **О микросервисе**:
	- Сервис полностью осуществляет взаимодействие с аккаунтами пользователей в календаре.
	- Также под контролем сервиса находится взаимодействие со всеми данными аккаунта пользователя и токенами.
	- Функционал:
        - **login** - **Получение токенов при успешной авторизации**

        - **register** - **Регистрация пользователя**

        - **auth** - **Получение данных пользователя**

        - **get_new_access_token** - **Получение токена доступа**

        - **generate_tokens** - **Генерация токенов**

		- **get_user_by_id** - **Получение пользователя по ID**

		- **get_users_by_id** - **Получение пользователей по их ID**
			- Реализована **пагинация** (получение пользователей по номеру страницы любого размера)
				- Также возможно получение **полного** списка пользователей при условии **items_per_page = -1**.

		- **get_all_users** - **Получение списка всех пользователей**
			- Реализована **пагинация** (получение пользователей по номеру страницы любого размера)
				- Также возможно получение **полного** списка пользователей при условии **items_per_page = -1**.
			- **Метод доступен только пользователям с типом ADMIN**

		- **update_user** - **Обновление пользователя**

		- **delete_user** - **Удаление пользователя по его ID**

        - **logout** - **Удаление токена пользователя и выход из аккаунта**
---
* **Для каждого метода предусмотрена обработка всевозможных ошибок.** **Подробнее ознакомиться с функционалом можно, прочитав docstring'и к методам.**
---
