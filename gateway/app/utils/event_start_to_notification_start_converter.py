"""Event start to notification start converter."""
from datetime import datetime
from typing import Optional

from app.models.Interval import Interval


def convert_event_start_to_notification_start(event_start: datetime, delay: Optional[Interval]) -> datetime:
    """
    Convert event start to notification start with delay

    Parameters
    ----------
    event_start : datetime
        Event start datetime
    delay : Interval
        Delay of the notification

    Returns
    -------
    datetime
        Notification start datetime

    """
    start = event_start

    if delay is not None:
        start -= delay.to_relative_delta()

    return start
