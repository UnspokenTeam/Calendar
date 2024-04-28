from datetime import datetime
from typing import Optional, Self

from google.protobuf.timestamp_pb2 import Timestamp
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
            description=proto.description if proto.description is not None else None,
            color=proto.color if proto.color is not None else None,
            repeating_delay=datetime.fromtimestamp(
                proto.repeating_delay.seconds + proto.repeating_delay.nanos / 1e9
            )
            if proto.repeating_delay is not None
            else None,
            deleted_at=datetime.fromtimestamp(
                proto.deleted_at.seconds + proto.deleted_at.nanos / 1e9
            )
            if proto.deleted_at is not None
            else None,
        )

    def to_proto(self) -> GrpcEvent:
        return GrpcEvent(
            id=self.id,
            title=self.title,
            start=Timestamp.FromDatetime(self.start),
            end=Timestamp.FromDatetime(self.end),
            author_id=self.author_id,
            created_at=Timestamp.FromDatetime(self.created_at),
            description=self.description if self.description is not None else None,
            color=self.color if self.color is not None else None,
            repeating_delay=Timestamp.FromDatetime(self.repeating_delay)
            if self.repeating_delay is not None
            else None,
            deleted_at=Timestamp.FromDatetime(self.deleted_at)
            if self.deleted_at is not None
            else None,
        )
