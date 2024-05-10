___
# Notification service
[![Build notification service](https://github.com/UnspokenTeam/Calendar/actions/workflows/build_notification_service.yaml/badge.svg)](https://github.com/UnspokenTeam/Calendar/actions/workflows/build_notification_service.yaml)
___
**Установка и описание**
___
1. **Образец .env файла**
	```env
	; Адрес базы данных
	DATABASE_URL="DATABASE_URL"
	; Вид окружения
	ENVIRONMENT="ENVIRONMENT"
	```
___
2. **Установка**:
___  
**Перед установкой**:

1. Сделать ```docker pull``` для custom_postgres или подготовить собственный instance PostgreSQL
```bash
docker pull ghcr.io/unspokenteam/custom_postgres:latest
```
___  
- Далее доступно несколько способов установки.

    1. **Через docker**
       - Установка осуществляется через **docker**, для установки пакета микросервиса введите и выполните команду:
		```bash
    	docker pull ghcr.io/unspokenteam/notification_service:latest
 		```
       - Сгенерируйте proto файлы, выполнив команду:
    	```bash
    	poetry run python -m grpc_tools.protoc -I ../shared/proto --python_out=./src/generated --grpc_python_out=./src/generated --pyi_out=./src/generated ../shared/proto/user/*.proto ../shared/proto/notification_service/*.proto ../shared/proto/interval/*.proto && poetry run protol --create-package --in-place --python-out ./src/generated protoc --experimental_allow_proto3_optional --proto-path=../shared/proto ../shared/proto/notification_service/*.proto ../shared/proto/user/*.proto ../shared/proto/interval/*.proto
        ```
    	- Сгенерируйте prisma клиент, выполнив команду:
    	```bash
    	poetry run prisma generate
        ```
        - Создайте .env файл, укажите его путь в команде и выполните её:
		```bash
		docker run -d -p 8083=8083 —env-file $PATH_TO_ENV ghcr.io/unspokenteam/notification_service:latest
 		```

	2. **Через poetry**
        - Также возможен локальный запуск при помощи утилиты poetry **без использования docker'a**. Для этого введите и выполните команду:
        ```bash
    	poetry install
    	```
        - Создайте .env файл в папке микросервиса. Добавьте вызов load_dotenv из модуля dotenv в методе serve в файле main.py и выполните команду:
        ```bash
        poetry run python -m src.main
        ```
---
3. **О микросервисе**:
	- Сервис полностью осуществляет взаимодействие с уведомлениями (**notification**'ами) в календаре.
	- Также под контролем сервиса находится взаимодействие с данными о уведомлениях.
	- Функционал:
		- **get_notifications_by_author_id** - **Получение списка уведомлений по ID автора**.
			- Реализована **пагинация** (получение уведомлений по номеру страницы любого размера)
				- Также возможно получение **полного** списка уведомлений при условии **items_per_page = -1**.
			- Реализована возможность отбора уведомлений по **временному интервалу**.

		- **get_notifications_by_event_id** - **Получение списка уведомлений по ID события**.
			- Реализована **пагинация** (получение уведомлений по номеру страницы любого размера)
				- Также возможно получение **полного** списка уведомлений при условии **items_per_page = -1**.

		- **get_notification_by_notification_id** - **Получение уведомления по ID**

		- **get_notification_by_event_and_author_ids** - **Получение уведомления по ID события и ID автора**

		- **get_notifications_by_notifications_ids** - **Получение уведомлений по их ID**
			- Реализована **пагинация** (получение уведомлений по номеру страницы любого размера)
				- Также возможно получение **полного** списка уведомлений при условии **items_per_page = -1**.

		- **get_all_notifications** - **Получение списка всех уведомлений**
			- Реализована **пагинация** (получение уведомлений по номеру страницы любого размера)
				- Также возможно получение **полного** списка уведомлений при условии **items_per_page = -1**.
			- **Метод доступен только пользователям с типом ADMIN**

		- **create_notification** - **Создание уведомления**
			- Основные аттрибуты уведомления:
				1. **event_id** - ID события
              2. **author_id** - ID автора уведомления
              3. **enabled** - булевый флаг, отвечающий за работу уведомления

		- **update_notification** - **Обновление уведомления**

		- **delete_notification_by_id** - **Удаление уведомления по его ID**

		- **delete_notifications_by_author_id** - **Удаление всех уведомлений по указанному ID автора.**

        - **delete_notifications_by_event_id** - **Удаление всех уведомлений по указанному ID события.**

        - **delete_notifications_by_events_and_author_ids** - **Удаление всех уведомлений по указанным ID событий и ID автора.**
---
* **Для каждого метода предусмотрена обработка всевозможных ошибок.** **Подробнее ознакомиться с функционалом можно, прочитав docstring'и к методам.**
---
