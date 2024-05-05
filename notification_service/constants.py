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
    "SELECT *\nFROM \"PrismaNotification\" as notification\nWHERE\n\tnotification.author_id = {}\n\tAND "
    "notification.deleted_at IS NULL{}{}\nUNION\nSELECT DISTINCT pattern.\"id\", pattern.\"event_id\", "
    "pattern.\"author_id\", pattern.\"start\", pattern.\"repeating_delay\", pattern.\"enabled\", "
    "pattern.\"created_at\", pattern.\"deleted_at\"\nFROM (\n\tSELECT *\n\t"
    "FROM \"PrismaNotification\" as notification, GENERATE_SERIES(notification.start, {}, "
    "notification.repeating_delay::interval) as notification_start_series\n\t"
    "WHERE notification.repeating_delay IS NOT NULL\n) as pattern\nWHERE\n\tpattern.author_id = {}\n\t"
    "AND pattern.deleted_at IS NULL{}{};"
)
# fmt: on
