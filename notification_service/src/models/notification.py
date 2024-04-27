"""Notification Model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Self

from prisma.models import Notification as PrismaNotification

from generated.notification_service.notification_service_pb2 import GrpcNotification


@dataclass
class Notification:
    """
    Class with data about the notification.

    Attributes
    ----------
    id : str
        Notification id.
    event_id : str
        Event id.
    author_id : str
        User id.
    enabled : bool
        Enable notification flag.
    created_at : datetime
        Time when the notification was created.
    deleted_at : Optional[datetime]
        Time when the notification was deleted.

    Methods
    -------
    to_grpc_notification()
        Converts notification to grpc notification.
    to_dict(exclude)
        Converts notification to dictionary.
    from_prisma_notification(prisma_notification)
        Converts prisma notification to notification object.
    from_grpc_notification(grpc_notification)
        Converts grpc notification to notification object.

    """

    id: str
    event_id: str
    author_id: str
    created_at: datetime
    deleted_at: Optional[datetime] = None
    enabled: bool = True

    def to_grpc_notification(self) -> GrpcNotification:
        """
        Generate grpc notification instance.

        Returns
        -------
        notification: GrpcNotification
            GrpcNotification instance.

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

    def to_dict(self, exclude: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Converts notification data to dictionary.

        Parameters
        ----------
        exclude : Optional[List[str]]
            List of fields to exclude.

        Returns
        -------
        Dict[str, Any]
            Notification data dictionary.

        """
        exclude_set = (set(exclude) if exclude is not None else set()) | {"id"}
        attrs = vars(self)
        return {
            attr.lstrip("_"): value
            for attr, value in attrs.items()
            if attr not in exclude_set
        }

    @classmethod
    def from_prisma_notification(cls, prisma_notification: PrismaNotification) -> Self:
        """
        Converts prisma notification.

        Parameters
        ----------
        prisma_notification : PrismaNotification
            Prisma notification.

        Returns
        -------
        Notification
            Notification class instance.

        """
        return cls(
            id=prisma_notification.id,
            event_id=prisma_notification.event_id,
            author_id=prisma_notification.author_id,
            enabled=prisma_notification.enabled,
            created_at=prisma_notification.created_at,
            deleted_at=prisma_notification.deleted_at,
        )

    @classmethod
    def from_grpc_notification(cls, grpc_notification: GrpcNotification) -> Self:
        """
        Converts grpc notification.

        Parameters
        ----------
        grpc_notification : GrpcNotification
            Grpc notification.

        Returns
        -------
        Notification
            Notification class instance.

        """
        return cls(
            id=grpc_notification.id,
            event_id=grpc_notification.event_id,
            author_id=grpc_notification.author_id,
            enabled=grpc_notification.enabled,
            created_at=datetime.fromtimestamp(
                grpc_notification.created_at.seconds
                + grpc_notification.created_at.nanos / 1e9
            ),
            deleted_at=(
                datetime.fromtimestamp(
                    grpc_notification.deleted_at.seconds
                    + grpc_notification.deleted_at.nanos / 1e9
                )
                if grpc_notification.WhichOneof("optional_deleted_at") is not None
                else None
            ),
        )

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Notification):
            return NotImplemented
        return self.id == other.id
