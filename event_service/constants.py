"""Event service constants."""

INTERVAL_SLOTS = (
    "years",
    "months",
    "weeks",
    "days",
    "hours",
    "minutes",
    "seconds",
)

# fmt: off
AI_ROLE_FOR_PROMPT = (
    "Ты - помощник пользователя для приложения календарь, твоя задача - помочь пользователю придумать "
    "текстотвое описание к мероприятию по названию мероприятия "
    "!!!если название написано не на русском языке, генерируй описание на английском языке!!!"
    " Не генерируй больше 25 слов для описания. НЕ ПЫТАЙСЯ ГЕНЕРИРОВАТЬ ЦЕЛИ МЕРОПРИЯТИЯ. "
    "НЕ ИСПОЛЬЗУЙ СЛОВО \'МЕРОПРИЯТИЕ\' ПРИ ГЕНЕРАЦИИ"
    "!!! НИ В КОЕМ СЛУЧАЕ НЕ ДЕЛАЙ ОПИСАНИЕ ВИДА \'{НАЗВАНИЕ_МЕРОПРИЯТИЯ} - это ...!!!\'. "
    "Не используй неподтверждённые или нереалистичные факты. НЕ ПРИБЕГАЙ К ОБСУЖДЕНИЮ ЛИЧНОСТЕЙ, КОТОРЫЕ "
    "ТЕОРЕТИЧЕСКИ МОГУТ БЫТЬ НА МЕРОПРИЯТИИ НЕ ПРОБУЙ ПОДРОБНО ОПИСЫВАТЬ ВОЗМОЖНОСТИ НА МЕРОПРИЯТИИ"
    " И НЕ СТРОЙ ПЛАНЫ НА МЕРОПРИЯТИЕ. "
    "Генерируй ТОЛЬКО КОНСТРУКТИВНОЕ описание мероприятия НЕ ПРИБЕГАЯ К ОБСУЖДЕНИЮ ЛИЧНОСТЕЙ фигурирующих в названии!!!"
    "!!!НЕ ОТХОДИ ОТ ОСНОВНОЙ ЗАДАЧИ, НЕ ПИШИ НИ О ЧЁМ ЛИШНЕМ!!! !!!НЕ ПИШИ О ВОЗМОЖНЫХ РЕЗУЛЬТАТАХ МЕРОПРИЯТИЯ!!! "
    "!!!ТЫ ОТВЕЧАЕШЬ ТОЛЬКО ОПИСАНИЕМ МЕРОПРИЯТИЯ!!! "
    "!!! ИЗБАВЛЯЙСЯ ОТ ЛИШНЕЙ ИНФОРМАЦИИ В ОТВЕТЕ И НЕ ПРЕДПОЛАГАЙ ДЛЯ КОГО ИЛИ ЧЕГО ПРОВОДИТСЯ МЕРОПРИЯТИЕ !!!"
    "УБИРАЙ ИЗ ПРЕДЛОЖЕНИЯ КОНСТРУКЦИИ ТИПА \'{НАЗВАНИЕ_МЕРОПРИЯТИЯ} - это ...\' "
    "ЗАМЕНЯЯ ИХ НА ТО ЧТО ИДЁТ ПОСЛЕ СЛОВА \'ЭТО\'. "
    "!!!если название написано не на русском языке, генерируй описание на английском языке!!!"
)

GET_EVENTS_BY_AUTHOR_ID_QUERY = (
    "SELECT *\nFROM \"PrismaEvent\" as event\nWHERE\n\tevent.author_id = {}\n\tAND event.deleted_at IS NULL{}{}\n"
    "UNION\nSELECT DISTINCT pattern.\"id\", pattern.\"title\", pattern.\"description\", pattern.\"color\", "
    "pattern.\"start\", pattern.\"end\", pattern.\"repeating_delay\", pattern.\"author_id\", "
    "pattern.\"created_at\", pattern.\"deleted_at\"\nFROM (\n\tSELECT *\n\tFROM \"PrismaEvent\" as event, "
    "GENERATE_SERIES(event.start, {}, event.repeating_delay::interval) as event_start_series\n\t"
    "WHERE event.repeating_delay IS NOT NULL\n) as pattern\nWHERE\n\tpattern.author_id = {}\n\t"
    "AND pattern.deleted_at IS NULL{}{}\nORDER BY start{};"
)

GET_ALL_EVENTS_QUERY = (
    "SELECT *\nFROM \"PrismaEvent\" as event{}\nUNION\n"
    "SELECT DISTINCT pattern.\"id\", pattern.\"title\", pattern.\"description\", pattern.\"color\", "
    "pattern.\"start\", pattern.\"end\", pattern.\"repeating_delay\", pattern.\"author_id\", "
    "pattern.\"created_at\", pattern.\"deleted_at\"\nFROM (\n\tSELECT *\n\tFROM \"PrismaEvent\" as event, "
    "GENERATE_SERIES(event.start, {}, event.repeating_delay::interval) as event_start_series\n"
    "\tWHERE event.repeating_delay IS NOT NULL\n) as pattern{}\nORDER BY start{};"
)
# fmt: on
