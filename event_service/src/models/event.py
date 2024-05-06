"""Event Model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Self

from prisma.models import PrismaEvent

from constants import INTERVAL_SLOTS
from dateutil.relativedelta import relativedelta
from generated.event_service.event_service_pb2 import GrpcEvent, Interval
from pytz import utc


@dataclass
class Event:
    """
    Class with data about the event.

    Attributes
    ----------
    id : str
        Event id.
    title : str
        Event title.
    start : datetime
        Start time of the event.
    end : datetime
        End time of the event.
    author_id : str
        Id of the event author.
    description : Optional[str]
        Event description.
    color : Optional[str]
        Event color for the UI.
    repeating_delay : Optional[str]
        The delay between the same event.
    created_at : datetime
        Time when the event was created.
    deleted_at : Optional[datetime]
        Time when the event was deleted.

    Methods
    -------
    static delay_string_to_interval(delay)
        Converts event repeating delay into interval.
    static delay_string_to_timedelta(delay)
        Converts event repeating delay into timedelta.
    to_grpc_event()
        Converts event to grpc event.
    to_dict(exclude)
        Converts event to dictionary.
    from_prisma_event(prisma_event)
        Converts prisma event to event object.
    from_grpc_event(grpc_event)
        Converts grpc event to event object.

    """

    id: str
    title: str
    start: datetime
    end: datetime
    author_id: str
    created_at: datetime
    description: Optional[str] = None
    color: Optional[str] = None
    repeating_delay: Optional[str] = None
    deleted_at: Optional[datetime] = None

    @staticmethod
    def delay_string_to_interval(delay: str) -> Interval:
        """
        Converts event repeating delay into interval.

        Parameters
        ----------
        delay : str
            Event repeating delay.

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
        Converts event repeating delay into interval.

        Parameters
        ----------
        delay : str
            Event repeating delay.

        Returns
        -------
        relativedelta
            relativedelta object.

        """
        delay_interval = Event.delay_string_to_interval(delay)
        return relativedelta(
            years=delay_interval.years,
            months=delay_interval.months,
            weeks=delay_interval.weeks,
            days=delay_interval.days,
            hours=delay_interval.hours,
            minutes=delay_interval.minutes,
            seconds=delay_interval.seconds,
        )

    def to_grpc_event(self) -> GrpcEvent:
        """
        Generate grpc event instance.

        Returns
        -------
        event: GrpcEvent
            GrpcEvent instance.

        """
        event = GrpcEvent(
            id=self.id,
            title=self.title,
            description=self.description,
            color=self.color,
            author_id=self.author_id,
            repeating_delay=self.delay_string_to_interval(self.repeating_delay)
            if self.repeating_delay is not None
            else None,
        )
        event.start.FromDatetime(self.start.astimezone(utc))
        event.end.FromDatetime(self.end.astimezone(utc))
        event.created_at.FromDatetime(self.created_at.astimezone(utc))
        if self.deleted_at is not None:
            event.deleted_at.FromDatetime(self.deleted_at.astimezone(utc))
        return event

    def to_dict(self, exclude: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Converts event data to dictionary.

        Parameters
        ----------
        exclude : Optional[List[str]]
            List of fields to exclude.

        Returns
        -------
        Dict[str, Any]
            Event data dictionary.

        """
        exclude_set = (set(exclude) if exclude is not None else set()) | {"id"}
        attrs = vars(self)
        return {
            attr.lstrip("_"): value
            for attr, value in attrs.items()
            if attr not in exclude_set
        }

    def __copy__(self) -> "Event":
        """
        Copies event.

        Returns
        -------
        Event
            Event class instance.

        """
        return Event(
            id=self.id,
            title=self.title,
            start=self.start,
            end=self.end,
            author_id=self.author_id,
            description=self.description,
            color=self.color,
            repeating_delay=self.repeating_delay,
            created_at=self.created_at,
            deleted_at=self.deleted_at,
        )

    @classmethod
    def from_prisma_event(cls, prisma_event: PrismaEvent) -> Self:
        """
        Converts prisma event.

        Parameters
        ----------
        prisma_event : PrismaEvent
            Prisma event.

        Returns
        -------
        Event
            Event class instance.

        """
        return cls(
            id=prisma_event.id,
            title=prisma_event.title,
            start=prisma_event.start,
            end=prisma_event.end,
            author_id=prisma_event.author_id,
            description=prisma_event.description,
            color=prisma_event.color,
            repeating_delay=prisma_event.repeating_delay,
            created_at=prisma_event.created_at,
            deleted_at=prisma_event.deleted_at,
        )

    @classmethod
    def from_grpc_event(cls, grpc_event: GrpcEvent) -> Self:
        """
        Converts grpc event.

        Parameters
        ----------
        grpc_event : GrpcEvent
            Grpc event.
        Returns
        -------
        Event
            Event class instance.

        """
        return cls(
            id=grpc_event.id,
            title=grpc_event.title,
            start=datetime.utcfromtimestamp(
                grpc_event.start.seconds + grpc_event.start.nanos / 1e9
            ),
            end=datetime.utcfromtimestamp(
                grpc_event.end.seconds + grpc_event.end.nanos / 1e9
            ),
            author_id=grpc_event.author_id,
            description=grpc_event.description
            if grpc_event.WhichOneof("optional_description") is not None
            else None,
            color=grpc_event.color
            if grpc_event.WhichOneof("optional_color") is not None
            else None,
            repeating_delay=(
                None
                if not (
                    delay := " ".join(
                        f"{value} {name.upper()}"
                        for name in INTERVAL_SLOTS
                        if (value := getattr(grpc_event.repeating_delay, name)) != 0
                    )
                )
                else delay
                if grpc_event.WhichOneof("optional_repeating_delay") is not None
                else None
            ),
            created_at=datetime.utcfromtimestamp(
                grpc_event.created_at.seconds + grpc_event.created_at.nanos / 1e9
            ),
            deleted_at=(
                datetime.utcfromtimestamp(
                    grpc_event.deleted_at.seconds + grpc_event.deleted_at.nanos / 1e9
                )
                if grpc_event.WhichOneof("optional_deleted_at") is not None
                else None
            ),
        )

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return NotImplemented
        return self.id == other.id
