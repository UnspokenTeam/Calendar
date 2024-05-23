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
    "Твоя задача - помочь пользователю придумать текстовое описание к мероприятию по названию мероприятия. "
    "Не генерируй больше 25 слов для описания. Не пытайся генерировать цели мероприятия или использовать "
    "неподтверждённые или нереалистичные факты. СТАРАЙСЯ ИЗБЕГАТЬ ОБСУЖДЕНИЯ ЛИЧНОСТЕЙ, КОТОРЫЕ ТЕОРЕТИЧЕСКИ МОГУТ БЫТЬ"
    " НА МЕРОПРИЯТИИ ИЛИ ФИГУРИРУЮТ В НАЗВАНИИ, НЕ ПРЕДПОЛАГАЙ ДЛЯ КОГО ИЛИ ЧЕГО ПРОВОДИТСЯ МЕРОПРИЯТИЕ, НЕ ПРОБУЙ "
    "ПОДРОБНО ОПИСЫВАТЬ ВОЗМОЖНОСТИ НА МЕРОПРИЯТИИ, НЕ ПРОБУЙ СТРОИТЬ ПЛАНЫ ИЛИ РЕЗУЛЬТАТЫ МЕРОПРИЯТИЯ. Генерируй "
    "ТОЛЬКО КОНСТРУКТИВНОЕ описание мероприятия.!!!НЕ ОТХОДИ ОТ ОСНОВНОЙ ЗАДАЧИ, ТЫ ОТВЕЧАЕШЬ ТОЛЬКО ОПИСАНИЕМ "
    "МЕРОПРИЯТИЯ!!! Не используй конструкции типа \'${НАЗВАНИЕ_МЕРОПРИЯТИЯ} - это ...\' "
    "заменяй их на то что идёт после слова \'это\'.",
    "Your job is to help the user come up with a text description for the event based on the name of the event. Don\'t "
    "generate more than 25 words for the description. DON\'T TRY TO GENERATE EVENT GOALS. Don\'t use unconfirmed or "
    "unrealistic facts. DON\'T RESORT TO DISCUSSING PERSONALITIES THAT COULD THEORETICALLY BE AT THE EVENT OR APPEAR IN"
    " THE TITLE, DON\'T ASSUME WHO OR WHAT THE EVENT IS FOR, DON\'T TRY TO DETAIL THE OPPORTUNITIES AT THE EVENT, "
    "DON\'T TRY TO MAKE PLANS OR RESULTS OF THE EVENT. Generate ONLY a CONSTRUCTIVE description of the event. !!!DON\'T"
    " STRAY FROM THE MAIN TASK, YOU ARE ONLY RESPONDING WITH A DESCRIPTION OF THE EVENT!!! Don\'t use constructions"
    " like \'${EVENT_NAME} is ...\' replace them with what comes after the word \'it\'."
)

GET_EVENTS_BY_AUTHOR_ID_QUERY = (
    "SELECT *\nFROM \"prisma_events\" as event\nWHERE\n\tevent.author_id = {}\n\tAND event.deleted_at IS NULL{}{}\n"
    "\tAND event.repeating_delay IS NULL\nUNION\n"
    "SELECT pattern.\"id\", pattern.\"title\", pattern.\"description\", pattern.\"color\", pattern.\"event_start\" as "
    "\"start\", (pattern.\"event_start\" + (pattern.\"end\" - pattern.\"start\")) as \"end\", "
    "pattern.\"repeating_delay\", pattern.\"author_id\", pattern.\"created_at\", pattern.\"deleted_at\"\n"
    "FROM (\n\tSELECT *\n\tFROM \"prisma_events\" as event,\n\t\tGENERATE_SERIES(event.start, {}, "
    "event.repeating_delay::interval) as \"event_start\"\n\tWHERE event.repeating_delay IS NOT NULL\n) as pattern\n"
    "WHERE\n\tpattern.author_id = {}\n\tAND pattern.deleted_at IS NULL{}{}\nORDER BY start{};"
)
"""
str: SQL query for get events by author id request.

GET_EVENTS_BY_AUTHOR_ID_QUERY example:

    SET datestyle = DMY;
    SELECT *
    FROM "prisma_events" as event
    WHERE
        event.author_id = 'AUTHOR_ID'
        AND event.deleted_at IS NULL
        AND '01/01/1970 01:00:00'::timestamp <= event.start
        AND event.start <= '01/01/1970 05:00:00'::timestamp
        AND event.repeating_delay IS NULL
    UNION
    SELECT pattern."id", pattern."title", pattern."description", pattern."color", pattern."event_start" as "start",
    (pattern."event_start" + (pattern."end" - pattern."start")) as "end", pattern."repeating_delay",
    pattern."author_id", pattern."created_at", pattern."deleted_at"
    FROM (
        SELECT *
        FROM "prisma_events" as event,
            GENERATE_SERIES(event.start, '01/01/1970 05:00:00'::timestamp, event.repeating_delay::interval
            ) as "event_start"
        WHERE event.repeating_delay IS NOT NULL
    ) as pattern
    WHERE
        pattern.author_id = 'AUTHOR_ID'
        AND pattern.deleted_at IS NULL
        AND '01/01/1970 01:00:00'::timestamp <= pattern."event_start"
        AND pattern."event_start" <= '01/01/1970 05:00:00'::timestamp
    ORDER BY start
    LIMIT 10
    OFFSET 0;

"""

GET_EVENTS_BY_EVENT_IDS_QUERY = (
    "SELECT *\nFROM \"prisma_events\" as event\nWHERE\n\tevent.id IN ({})\n\tAND event.deleted_at IS NULL{}{}\n"
    "\tAND event.repeating_delay IS NULL\nUNION\n"
    "SELECT pattern.\"id\", pattern.\"title\", pattern.\"description\", pattern.\"color\", pattern.\"event_start\" as "
    "\"start\", (pattern.\"event_start\" + (pattern.\"end\" - pattern.\"start\")) as \"end\", "
    "pattern.\"repeating_delay\", pattern.\"author_id\", pattern.\"created_at\", pattern.\"deleted_at\"\n"
    "FROM (\n\tSELECT *\n\tFROM \"prisma_events\" as event,\n\t\tGENERATE_SERIES(event.start, {}, "
    "event.repeating_delay::interval) as \"event_start\"\n\tWHERE event.repeating_delay IS NOT NULL\n) as pattern\n"
    "WHERE\n\tpattern.id IN ({})\n\tAND pattern.deleted_at IS NULL{}{}\nORDER BY start{};"
)
"""
str: SQL query for get events by event ids request.

    GET_EVENTS_BY_EVENT_IDS_QUERY example:

        SET datestyle = DMY;
        SELECT *
        FROM "prisma_events" as event
        WHERE
            event.id IN ('FIRST_EVENT_ID', 'SECOND_EVENT_ID')
            AND event.deleted_at IS NULL
            AND '01/01/1970 01:00:00'::timestamp <= event.start
            AND event.start <= '01/01/1970 05:00:00'::timestamp
            AND event.repeating_delay IS NULL
        UNION
        SELECT pattern."id", pattern."title", pattern."description", pattern."color", pattern."event_start" as "start",
         (pattern."event_start" + (pattern."end" - pattern."start")) as "end", pattern."repeating_delay",
         pattern."author_id", pattern."created_at", pattern."deleted_at"
        FROM (
            SELECT *
            FROM "prisma_events" as event,
                GENERATE_SERIES(event.start, '01/01/1970 05:00:00'::timestamp, event.repeating_delay::interval
                ) as "event_start"
            WHERE event.repeating_delay IS NOT NULL
        ) as pattern
        WHERE
            pattern.id IN ('FIRST_EVENT_ID', 'SECOND_EVENT_ID')
            AND pattern.deleted_at IS NULL
            AND '01/01/1970 01:00:00'::timestamp <= pattern."event_start"
            AND pattern."event_start" <= '01/01/1970 05:00:00'::timestamp
        ORDER BY start
        LIMIT 10
        OFFSET 0;

"""

GET_ALL_EVENTS_QUERY = (
    "SELECT *\nFROM \"prisma_events\" as event\n{}\t\nAND event.repeating_delay IS NULL\n"
    "\tAND event.repeating_delay IS NULL\nUNION\n"
    "SELECT pattern.\"id\", pattern.\"title\", pattern.\"description\", pattern.\"color\", pattern.\"event_start\" as "
    "\"start\", (pattern.\"event_start\" + (pattern.\"end\" - pattern.\"start\")) as \"end\", "
    "pattern.\"repeating_delay\", pattern.\"author_id\", pattern.\"created_at\", pattern.\"deleted_at\"\n"
    "FROM (\n\tSELECT *\n\tFROM \"prisma_events\" as event,\n\t\tGENERATE_SERIES(event.start, {}, "
    "event.repeating_delay::interval) as \"event_start\"\n\tWHERE event.repeating_delay IS NOT NULL\n) as pattern\n"
    "{}\nORDER BY start{};"
)
"""
str: SQL query for get all events request.

    GET_ALL_EVENTS_QUERY example:

        SET datestyle = DMY;
        SELECT *
        FROM "prisma_events" as event
        WHERE
            '01/01/1970 01:00:00'::timestamp <= event.start
            AND event.start <= '01/01/1970 05:00:00'::timestamp
            AND event.repeating_delay IS NULL
        UNION
        SELECT pattern."id", pattern."title", pattern."description", pattern."color", pattern."event_start" as "start",
        (pattern."event_start" + (pattern."end" - pattern."start")) as "end", pattern."repeating_delay",
        pattern."author_id", pattern."created_at", pattern."deleted_at"
        FROM (
            SELECT *
            FROM "prisma_events" as event,
                GENERATE_SERIES(event.start, '01/01/1970 05:00:00'::timestamp, event.repeating_delay::interval
                ) as "event_start"
            WHERE event.repeating_delay IS NOT NULL
        ) as pattern
        WHERE
            '01/01/1970 01:00:00'::timestamp <= pattern."event_start"
            AND pattern."event_start" <= '01/01/1970 05:00:00'::timestamp
        ORDER BY start
        LIMIT 10
        OFFSET 0;

"""
# fmt: on
