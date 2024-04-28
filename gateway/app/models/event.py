from datetime import datetime
from typing import Optional, Self

from pydantic import BaseModel

from app.generated.event_service.event_service_pb2 import GrpcEvent


class Event(BaseModel):
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

    @classmethod
    def from_proto(cls, proto: GrpcEvent) -> Self:
        return cls(
            id=proto.id,
            title=proto.title,
            start=datetime.fromtimestamp(proto.start.seconds + proto.start.nanos / 1e9),
            end=datetime.fromtimestamp(proto.end.seconds + proto.end.nanos / 1e9),
            author_id=proto.author_id,
            created_at=datetime.fromtimestamp(
                proto.created_at.seconds + proto.created_at.nanos / 1e9
            ),
            description=proto.description if proto.WhichOneof("optional_description") is not None else None,
            color=proto.color if proto.WhichOneof("optional_color") is not None else None,
            repeating_delay=datetime.fromtimestamp(
                proto.repeating_delay.seconds + proto.repeating_delay.nanos / 1e9
            )
            if proto.WhichOneof("optional_repeating_delay") is not None
            else None,
            deleted_at=datetime.fromtimestamp(
                proto.deleted_at.seconds + proto.deleted_at.nanos / 1e9
            )
            if proto.WhichOneof("optional_deleted_at") is not None
            else None,
        )

    def to_proto(self) -> GrpcEvent:
        event = GrpcEvent(
            id=self.id,
            title=self.title,
            author_id=self.author_id,
            description=self.description if self.description is not None else None,
            color=self.color if self.color is not None else None,
        )

        event.created_at.FromDatetime(self.created_at)
        event.start.FromDatetime(self.start)
        event.end.FromDatetime(self.end)
        if self.repeating_delay is not None:
            event.repeating_delay.FromDatetime(self.repeating_delay)
        if self.deleted_at is not None:
            event.deleted_at.FromDatetime(self.deleted_at)

        return event
