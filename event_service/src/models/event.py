"""Event Model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Self

from prisma.models import Event as PrismaEvent

from proto.event_service_pb2 import GrpcEvent


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
    repeating_delay : Optional[datetime]
        The delay between the same event.
    created_at : datetime
        Time when the event was created.
    deleted_at : Optional[datetime]
        Time when the event was deleted.

    Methods
    -------
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
    repeating_delay: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        self.created_at = datetime.now()

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
        )
        event.start.FromDatetime(self.start)
        event.end.FromDatetime(self.end)
        event.repeating_delay.FromDatetime(self.repeating_delay)
        event.created_at.FromDatetime(self.created_at)
        event.deleted_at.FromDatetime(self.created_at)

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
        exclude_set = set(exclude) if exclude is not None else set()
        attrs = vars(self)
        return {
            attr.lstrip("_"): value
            for attr, value in attrs.items()
            if attr not in exclude_set
        }

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
            start=datetime.fromtimestamp(
                grpc_event.start.seconds + grpc_event.start.nanos / 1e9
            ),
            end=datetime.fromtimestamp(
                grpc_event.end.seconds + grpc_event.end.nanos / 1e9
            ),
            author_id=grpc_event.author_id,
            description=grpc_event.description,
            color=grpc_event.color,
            repeating_delay=datetime.fromtimestamp(
                grpc_event.repeating_delay.seconds
                + grpc_event.repeating_delay.nanos / 1e9
            )
            if grpc_event.repeating_delay is not None
            else None,
            created_at=datetime.fromtimestamp(
                grpc_event.created_at.seconds + grpc_event.created_at.nanos / 1e9
            ),
            deleted_at=datetime.fromtimestamp(
                grpc_event.deleted_at.seconds + grpc_event.deleted_at.nanos / 1e9
            )
            if grpc_event.deleted_at is not None
            else None,
        )

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return NotImplemented
        return self.id == other.id
