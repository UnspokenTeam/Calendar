"""Notification service constants."""

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
GET_NOTIFICATIONS_BY_AUTHOR_ID_QUERY = (
    "SELECT *\nFROM \"prisma_notifications\" as notification\nWHERE\n\tnotification.author_id = {}\n\tAND "
    "notification.enabled = TRUE\n\tAND notification.deleted_at IS NULL{}{}\n"
    "\tAND notification.repeating_delay IS NULL\nUNION\n"
    "SELECT pattern.\"id\", pattern.\"event_id\", pattern.\"author_id\", pattern.\"enabled\","
    " pattern.\"notification_start\" as \"start\", pattern.\"delay_to_event\", pattern.\"repeating_delay\", "
    "pattern.\"created_at\", pattern.\"deleted_at\"\nFROM (\n\tSELECT *\n\tFROM "
    "\"prisma_notifications\" as notification,\n\t\tGENERATE_SERIES(notification.start, {}, "
    "notification.repeating_delay::interval) as \"notification_start\"\n\tWHERE notification.repeating_delay IS"
    " NOT NULL\n) as pattern\nWHERE\n\tpattern.author_id = {}\n\tAND pattern.enabled = TRUE\n\tAND pattern.deleted_at "
    "IS NULL{}{}\nORDER BY start{};"
)
"""
str: SQL query for get events by author id request.

GET_NOTIFICATIONS_BY_AUTHOR_ID_QUERY example:

    SET datestyle = DMY;
    SELECT *
    FROM "prisma_notifications" as notification
    WHERE
        notification.author_id = 'AUTHOR_ID'
        AND notification.enabled = TRUE
        AND notification.deleted_at IS NULL
        AND '01/01/1970 01:00:00'::timestamp <= notification.start
        AND notification.start <= '01/01/1970 05:00:00'::timestamp
        AND notification.repeating_delay IS NULL
    UNION
    SELECT pattern."id", pattern."event_id", pattern."author_id", pattern."notification_start" as "start",
    pattern."delay_to_event", pattern."repeating_delay", pattern."enabled", pattern."created_at", pattern."deleted_at"
    FROM (
        SELECT *
        FROM "prisma_notifications" as notification,
            GENERATE_SERIES(notification.start, '01/01/1970 05:00:00'::timestamp,
            notification.repeating_delay::interval) as "notification_start"
        WHERE notification.repeating_delay IS NOT NULL
    ) as pattern
    WHERE
        pattern.author_id = 'AUTHOR_ID'
        AND pattern.enabled = TRUE
        AND pattern.deleted_at IS NULL
        AND '01/01/1970 01:00:00'::timestamp <= pattern."notification_start"
        AND pattern."notification_start" <= '01/01/1970 05:00:00'::timestamp
    ORDER BY start
    LIMIT 10
    OFFSET 0;

"""
# fmt: on
