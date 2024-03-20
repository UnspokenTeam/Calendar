from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from proto.event_service_pb2 import Event as GrpcEvent


@dataclass
class Event:
    id: str
    title: str
    start: datetime
    end: datetime
    author_id: str
    description: Optional[str] = None
    color: Optional[str] = None
    repeating_delay: Optional[datetime] = None

    def to_grpc_event(self) -> GrpcEvent:
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
