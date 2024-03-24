"""Event Model."""
from dataclasses import dataclass
from typing import Optional, Self, List, Any
from datetime import datetime

from prisma.models import Event as PrismaEvent

from proto.event_service_pb2 import Event as GrpcEvent


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

    Methods
    -------
    to_grpc_event()
        Converts event to grpc event.
    to_dict(exclude)
        Converts event to dictionary.
    from_prisma_event(prisma_event)
        Converts prisma event to event object.

    """

    id: str
    title: str
    start: datetime
    end: datetime
    author_id: str
    description: Optional[str] = None
    color: Optional[str] = None
    repeating_delay: Optional[datetime] = None

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

        return event

    def to_dict(self, exclude: Optional[List[str]] = None) -> dict[str, Any]:
        """
        Converts event data to dictionary.

        Parameters
        ----------
        exclude : Optional[List[str]]
            List of fields to exclude.

        Returns
        -------
        dict[str, Any]
            Event data dictionary.

        """
        exclude_set = set(exclude if exclude is not None else ["id"])
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
        )

    def __repr__(self) -> str:
        return f"{vars(self)}"
