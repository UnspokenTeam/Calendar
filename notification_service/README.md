___
# Notification service
[![Build notification service](https://github.com/UnspokenTeam/Calendar/actions/workflows/build_notification_service.yaml/badge.svg)](https://github.com/UnspokenTeam/Calendar/actions/workflows/build_notification_service.yaml)
___
**Установка и описание**
___
1. **Образец .env файла**
	```
	DATABASE_URL="DATABASE_URL"
	ENVIRONMENT="ENVIRONMENT"
	```
___
2. **Установка**:
	- Доступно несколько способов установки.
    2. **Через docker**
       - Установка осуществляется через **docker**, для установки пакета микросервиса введите и выполните команду:
		```
    	docker pull ghcr.io/unspokenteam/notification_service:latest
 		```
       - Создайте .env файл, укажите его путь в команде и выполните её:
		```
		docker run -d -p 8083=8083 —env-file $PATH_TO_ENV ghcr.io/unspokenteam/notification_service:latest
 		```
	2. **Через poetry**
        - Также возможен локальный запуск при помощи утилиты poetry **без использования docker'a**. Для этого введите и выполните команду:
        ```
    	poetry install
    	```
        - Создайте .env файл в папке микросервиса. Добавьте вызов load_dotenv из модуля dotenv в методе serve в файле main.py и выполните команду:
        ```
        poetry run python main.py
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
