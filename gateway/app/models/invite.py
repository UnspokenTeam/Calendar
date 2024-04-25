from datetime import datetime
from enum import StrEnum
from typing import Optional, Self

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel

from app.generated.invite_service.invite_service_pb2 import (
    GrpcInvite,
    InviteStatus as GrpcInviteStatus
)


class InviteStatus(StrEnum):
    """
    Invite status enum

    Methods
    -------
    static from_proto(proto)
        Get invite status instance from proto invite status
    to_proto()
        Get proto invite status from invite status instance

    """

    PENDING = "PENDING"
    """Invite pending approval"""
    ACCEPTED = "ACCEPTED"
    """Invite accepted"""
    REJECTED = "REJECTED"
    """Invite rejected"""

    @classmethod
    def from_proto(cls, proto: GrpcInviteStatus):
        """
        Get invite status instance from proto invite status

        Parameters
        ----------
        proto : GrpcInviteStatus
            Proto invite status

        Returns
        -------
        InviteStatus
            Invite status instance

        """
        return cls(str(proto))

    def to_proto(self) -> GrpcInviteStatus:
        """
        Get proto invite status from invite status instance

        Returns
        -------
        GrpcInviteStatus
            Proto invite status

        """
        return GrpcInviteStatus(str(self))


class Invite(BaseModel):
    """
    Invite data class

    Attributes
    ----------
    id : str
        Id of the invite
    event_id : str
        Id of the related event
    author_id : str
        Id of the author of the invite
    invitee_id : str
        Id of the invitee 
    status : InviteStatus
        Invite status
    created_at : datetime
        Time when the invite was created
    deleted_at : Optional[datetime]
        Time when invite was deleted

    Methods
    -------
    static from_proto(proto)
        Get invite instance from proto invite
    to_proto()
        Get proto invite from invite instance


    """
    id: str
    event_id: str
    author_id: str
    invitee_id: str
    status: InviteStatus
    created_at: datetime
    deleted_at: Optional[datetime] = None

    @classmethod
    def from_proto(cls, proto: GrpcInvite) -> Self:
        """
        Get invite instance from proto invite

        Parameters
        ----------
        proto : GrpcInvite
            Proto invite

        Returns
        -------
        Invite
            Invite instance

        """
        return cls(
            id=proto.id,
            event_id=proto.event_id,
            author_id=proto.author_id,
            invitee_id=proto.invitee_id,
            status=InviteStatus.from_proto(proto.status),
            created_at=datetime.fromtimestamp(
                proto.created_at.seconds + proto.created_at.nanos / 1e9
            ),
            deleted_at=datetime.fromtimestamp(
                proto.deleted_at.seconds + proto.deleted_at.nanos / 1e9
            ) if proto.deleted_at is not None else None
        )

    def to_proto(self) -> GrpcInvite:
        """
        Get proto invite from invite instance

        Returns
        -------
        GrpcInvite
            Proto invite

        """
        return GrpcInvite(
            id=self.id,
            event_id=self.event_id,
            author_id=self.author_id,
            invitee_id=self.invitee_id,
            status=self.status.to_proto(),
            created_at=Timestamp.FromDatetime(self.created_at),
            deleted_at=Timestamp.FromDatetime(self.deleted_at) if self.deleted_at is not None else None
        )