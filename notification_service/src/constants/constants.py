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
    "SELECT pattern.\"id\", pattern.\"event_id\", pattern.\"author_id\","
    " pattern.\"notification_start\" as \"start\", pattern.\"delay_to_event\", pattern.\"repeating_delay\", "
    "pattern.\"enabled\", pattern.\"created_at\", pattern.\"deleted_at\"\nFROM (\n\tSELECT *\n\tFROM "
    "\"PrismaNotification\" as notification,\n\t\tGENERATE_SERIES(notification.start, {}, "
    "notification.repeating_delay::interval) as \"notification_start\"\n\tWHERE notification.repeating_delay IS"
    " NOT NULL\n) as pattern\nWHERE\n\tpattern.author_id = {}\n\tAND pattern.enabled = TRUE\n\tAND pattern.deleted_at "
    "IS NULL{}{}\nORDER BY start{};"
)
# fmt: on
