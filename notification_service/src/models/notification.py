"""Notification Model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Self

from prisma.models import PrismaNotification

from src.constants.constants import INTERVAL_SLOTS
from src.generated.interval.interval_pb2 import Interval
from src.generated.notification_service.notification_service_pb2 import GrpcNotification

from dateutil.relativedelta import relativedelta


@dataclass
class Notification:
    """
    Class with data about the notification.

    Attributes
    ----------
    id : str
        Notification id.
    event_id : str
        Event id.
    author_id : str
        User id.
    enabled : bool
        Enable notification flag.
    start : datetime
        Start time of notification.
    repeating_delay : Optional[str]
        The delay between the same event.
    created_at : datetime
        Time when the notification was created.
    deleted_at : Optional[datetime]
        Time when the notification was deleted.

    Methods
    -------
    static delay_string_to_interval(delay)
        Converts notification repeating delay into interval.
    static delay_string_to_timedelta(delay)
        Converts notification repeating delay into timedelta.
    to_grpc_notification()
        Converts notification to grpc notification.
    to_dict(exclude)
        Converts notification to dictionary.
    from_prisma_notification(prisma_notification)
        Converts prisma notification to notification object.
    from_grpc_notification(grpc_notification)
        Converts grpc notification to notification object.

    """

    id: str
    event_id: str
    author_id: str
    start: datetime
    created_at: datetime
    repeating_delay: Optional[str] = None
    deleted_at: Optional[datetime] = None
    enabled: bool = True

    @staticmethod
    def delay_string_to_interval(delay: str) -> Interval:
        """
        Converts notification repeating delay into interval.

        Parameters
        ----------
        delay : str
            Notification repeating delay.

        Returns
        -------
        Interval
            Interval object.

        """
        delay_objects = delay.split()
        interval = Interval()
        for i in range(1, len(delay_objects), 2):
            interval.__setattr__(delay_objects[i].lower(), int(delay_objects[i - 1]))
        return interval

    @staticmethod
    def delay_string_to_timedelta(delay: str) -> relativedelta:
        """
        Converts notification repeating delay into interval.

        Parameters
        ----------
        delay : str
            Notification repeating delay.

        Returns
        -------
        relativedelta
            relativedelta object.

        """
        delay_interval = Notification.delay_string_to_interval(delay)
        return relativedelta(
            years=delay_interval.years,
            months=delay_interval.months,
            weeks=delay_interval.weeks,
            days=delay_interval.days,
            hours=delay_interval.hours,
            minutes=delay_interval.minutes,
            seconds=delay_interval.seconds,
        )

    def to_grpc_notification(self) -> GrpcNotification:
        """
        Generate grpc notification instance.

        Returns
        -------
        notification: GrpcNotification
            GrpcNotification instance.

        """
        notification = GrpcNotification(
            id=self.id,
            event_id=self.event_id,
            author_id=self.author_id,
            enabled=self.enabled,
            repeating_delay=self.delay_string_to_interval(self.repeating_delay)
            if self.repeating_delay is not None
            else None,
        )
        notification.start.FromDatetime(self.start)
        notification.created_at.FromNanoseconds(
            int(self.created_at.replace(tzinfo=datetime.now().tzinfo).timestamp() * 1e9)
        )
        if self.deleted_at is not None:
            notification.deleted_at.FromNanoseconds(
                int(
                    self.deleted_at.replace(tzinfo=datetime.now().tzinfo).timestamp()
                    * 1e9
                )
            )

        return notification

    def to_dict(self, exclude: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Converts notification data to dictionary.

        Parameters
        ----------
        exclude : Optional[List[str]]
            List of fields to exclude.

        Returns
        -------
        Dict[str, Any]
            Notification data dictionary.

        """
        exclude_set = (set(exclude) if exclude is not None else set()) | {"id"}
        attrs = vars(self)
        return {
            attr.lstrip("_"): value
            for attr, value in attrs.items()
            if attr not in exclude_set
        }

    def __copy__(self) -> "Notification":
        """
        Copies notification.

        Returns
        -------
        Notification
            Notification class instance.

        """
        return Notification(
            id=self.id,
            event_id=self.event_id,
            author_id=self.author_id,
            enabled=self.enabled,
            start=self.start,
            repeating_delay=self.repeating_delay,
            created_at=self.created_at,
            deleted_at=self.deleted_at,
        )

    @classmethod
    def from_prisma_notification(cls, prisma_notification: PrismaNotification) -> Self:
        """
        Converts prisma notification.

        Parameters
        ----------
        prisma_notification : PrismaNotification
            Prisma notification.

        Returns
        -------
        Notification
            Notification class instance.

        """
        return cls(
            id=prisma_notification.id,
            event_id=prisma_notification.event_id,
            author_id=prisma_notification.author_id,
            enabled=prisma_notification.enabled,
            start=prisma_notification.start,
            repeating_delay=prisma_notification.repeating_delay,
            created_at=prisma_notification.created_at,
            deleted_at=prisma_notification.deleted_at,
        )

    @classmethod
    def from_grpc_notification(cls, grpc_notification: GrpcNotification) -> Self:
        """
        Converts grpc notification.

        Parameters
        ----------
        grpc_notification : GrpcNotification
            Grpc notification.

        Returns
        -------
        Notification
            Notification class instance.

        """
        return cls(
            id=grpc_notification.id,
            event_id=grpc_notification.event_id,
            author_id=grpc_notification.author_id,
            enabled=grpc_notification.enabled,
            start=datetime.utcfromtimestamp(
                grpc_notification.start.seconds + grpc_notification.start.nanos / 1e9
            ),
            repeating_delay=(
                None
                if not (
                    delay := " ".join(
                        f"{value} {name.upper()}"
                        for name in INTERVAL_SLOTS
                        if (value := getattr(grpc_notification.repeating_delay, name))
                        != 0
                    )
                )
                else delay
                if grpc_notification.WhichOneof("optional_repeating_delay") is not None
                else None
            ),
            created_at=datetime.utcfromtimestamp(
                grpc_notification.created_at.seconds
                + grpc_notification.created_at.nanos / 1e9
            ),
            deleted_at=(
                datetime.utcfromtimestamp(
                    grpc_notification.deleted_at.seconds
                    + grpc_notification.deleted_at.nanos / 1e9
                )
                if grpc_notification.WhichOneof("optional_deleted_at") is not None
                else None
            ),
        )

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Notification):
            return NotImplemented
        return self.id == other.id
