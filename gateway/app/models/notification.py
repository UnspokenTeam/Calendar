"""User model"""
from datetime import datetime
from typing import Annotated, Optional, Self
from uuid import UUID

from app.generated.notification_service.notification_service_pb2 import GrpcNotification
from app.validators import str_special_characters_validator

from pydantic import AfterValidator, BaseModel, Field
from pytz import utc


class Notification(BaseModel):
    """
    Notification dataclass

    Attributes
    ----------
    id : UUID
    event_id : UUID
    author_id : UUID
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

    id: UUID
    event_id: UUID
    author_id: UUID
    enabled: Annotated[bool, Field(True)]
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
            if proto.WhichOneof("optional_deleted_at") is not None
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
        notification = GrpcNotification(
            id=str(self.id),
            event_id=str(self.event_id),
            author_id=str(self.author_id),
            enabled=self.enabled,
        )

        notification.created_at.FromDatetime(self.created_at.astimezone(utc))
        if self.deleted_at is not None:
            notification.deleted_at.FromDatetime(self.deleted_at.astimezone(utc))

        return notification
