"""User model"""
from datetime import datetime
from typing import Optional, Self

from app.generated.notification_service.notification_service_pb2 import GrpcNotification

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel


class Notification(BaseModel):
    """
    Notification dataclass

    Attributes
    ----------
    id : str
    event_id : str
    author_id : str
    enabled : bool
    created_at : datetime
    deleted_at : Optional[datetime]

    Methods
    -------
    static from_proto(proto)
        Get notification instance from proto object
    to_proto()
        Get proto object from Notification instance

    """

    id: str
    event_id: str
    author_id: str
    enabled: bool
    created_at: datetime
    deleted_at: Optional[datetime] = None

    @classmethod
    def from_proto(cls, proto: GrpcNotification) -> Self:
        """
        Get notification instance from proto object

        Parameters
        ----------
        proto : GrpcNotification
            Proto notification object

        Returns
        -------
        Notification
            Notification instance

        """
        return cls(
            id=proto.id,
            event_id=proto.event_id,
            author_id=proto.author_id,
            enabled=proto.enabled,
            created_at=datetime.fromtimestamp(
                proto.created_at.seconds + proto.created_at.nanos / 1e9
            ),
            deleted_at=datetime.fromtimestamp(
                proto.deleted_at.seconds + proto.deleted_at.nanos / 1e9
            )
            if proto.deleted_at is not None
            else None,
        )

    def to_proto(self) -> GrpcNotification:
        """
        Get proto object from Notification instance

        Returns
        -------
        GrpcNotification
            Proto notification object

        """
        return GrpcNotification(
            id=self.id,
            event_id=self.event_id,
            author_id=self.author_id,
            enabled=self.enabled,
            created_at=Timestamp.FromDatetime(self.created_at),
            deleted_at=Timestamp.FromDatetime(self.deleted_at)
            if self.deleted_at is not None
            else None,
        )
