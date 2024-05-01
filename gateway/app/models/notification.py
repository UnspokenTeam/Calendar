"""User model"""
from datetime import datetime
from typing import Annotated, Optional, Self

from app.generated.notification_service.notification_service_pb2 import GrpcNotification
from app.validators import str_special_characters_validator

from pydantic import AfterValidator, BaseModel, Field


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

    id: Annotated[str, Field("", min_length=1), AfterValidator(str_special_characters_validator)]
    event_id: Annotated[str, Field("", min_length=1), AfterValidator(str_special_characters_validator)]
    author_id: Annotated[str, Field("", min_length=1), AfterValidator(str_special_characters_validator)]
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
            id=self.id,
            event_id=self.event_id,
            author_id=self.author_id,
            enabled=self.enabled,
        )

        notification.created_at.FromDatetime(self.created_at)
        if self.deleted_at is not None:
            notification.deleted_at.FromDatetime(self.deleted_at)

        return notification
