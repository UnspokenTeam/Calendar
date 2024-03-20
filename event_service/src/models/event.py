"""Event Model."""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from proto.event_service_pb2 import Event as GrpcEvent


@dataclass
class Event:
    """
    Class with data about the event.

    ...

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
