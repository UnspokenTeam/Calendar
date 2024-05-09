___
# Event service
[![Build event service](https://github.com/UnspokenTeam/Calendar/actions/workflows/build_event_service.yaml/badge.svg)](https://github.com/UnspokenTeam/Calendar/actions/workflows/build_event_service.yaml)
___
**Установка и описание**
___
1. **Образец .env файла**
	```env
	; Адрес базы данных
	DATABASE_URL="DATABASE_URL"
	; Вид окружения
	ENVIRONMENT="ENVIRONMENT"
	; Ключ для взаимодействия с LLM через API от OpenRouter
	OPENROUTER_API_KEY="API_KEY"
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
      docker pull ghcr.io/unspokenteam/event_service:latest
      ```
     - Создайте .env файл, укажите его путь в команде и выполните её:
      ```bash
      docker run -d -p 8081=8081 —env-file $PATH_TO_ENV ghcr.io/unspokenteam/event_service:latest
      ```

  2. **Через poetry**
      - Также возможен локальный запуск при помощи утилиты poetry **без использования docker'a**. Для этого введите и выполните команду:
      ```bash
      poetry install
      ```
      - Сгенерируйте proto файлы, выполнив команду:
      ```bash
      poetry run python -m grpc_tools.protoc -I ../shared/proto --python_out=./src/generated --grpc_python_out=./src/generated --pyi_out=./src/generated ../shared/proto/user/*.proto ../shared/proto/event_service/*.proto ../shared/proto/interval/*.proto && poetry run protol --create-package --in-place --python-out ./src/generated protoc --experimental_allow_proto3_optional --proto-path=../shared/proto ../shared/proto/event_service/*.proto ../shared/proto/user/*.proto ../shared/proto/interval/*.proto
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
	- Сервис полностью осуществляет взаимодействие с событиями (**event**'ами) в календаре.
	- Также под контролем сервиса находится взаимодействие с данными о событиях.
	- Функционал:
		- **get_events_by_author_id** - **Получение списка событий по ID автора**.
			- Реализована **пагинация** (получение событий по номеру страницы любого размера)
				- Также возможно получение **полного** списка событий при условии **items_per_page = -1**.
			- Реализована возможность отбора событий по **временному интервалу**.

		- **get_event_by_event_id** - **Получение события по ID**

		- **get_events_by_events_ids** - **Получение событий по их ID**
			- Реализована **пагинация** (получение событий по номеру страницы любого размера)
				- Также возможно получение **полного** списка событий при условии **items_per_page = -1**.
			- Реализована возможность отбора событий по **временному интервалу**.

		- **get_all_events** - **Получение списка всех событий**
			- Реализована **пагинация** (получение событий по номеру страницы любого размера)
				- Также возможно получение **полного** списка событий при условии **items_per_page = -1**.
			- **Метод доступен только пользователям с типом ADMIN**
			- Реализована возможность отбора событий **по временному интервалу**.

		- **create_event** - **Создание события**
			- Реализован выбор следующих аттрибутов событий:
				1. **title** - Название события.
				2. **start** - Время и дата начала события (datetime объект).
				3. **end** - Время и дата конца события (datetime объект).
				4. **description** - Описание события.
				5. **color** - Цвет, которым событие будет отмечено событие в календаре.
				6. **repeating_delay** - Частота повторения события (Интервал).
					- Предусмотрен **специальный тип Interval**, который содержит такие аттрибуты как:
						- **years** - количество лет
						- **months** - количество месяцев
						- **weeks** - количество недель
						- **days** - количество дней
						- **hours** - количество часов
						- **minutes** - количество минут
						- **seconds** - количество секунд

		- **update_event** - **Обновление события**

		- **delete_event_by_id** - **Удаление события по его ID**

		- **delete_events_by_author_id** - **Удаление всех событий по указанному ID автора**

        - **generate_event_description** - **Генерация описания к событию при помощи LLM**
---
* **Для каждого метода предусмотрена обработка всевозможных ошибок.** **Подробнее ознакомиться с функционалом можно, прочитав docstring'и к методам.**
---
