"""Invite model"""
from datetime import datetime
from enum import StrEnum
from typing import Annotated, Optional, Self
from uuid import UUID

from app.generated.invite_service.invite_service_pb2 import (
    GrpcInvite,
)
from app.generated.invite_service.invite_service_pb2 import (
    InviteStatus as GrpcInviteStatus,
)

from pydantic import UUID4, AfterValidator, BaseModel
from pytz import UTC, utc


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
    def from_proto(cls, proto: GrpcInviteStatus) -> Self:
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
        match proto:
            case GrpcInviteStatus.PENDING:
                return cls("PENDING")
            case GrpcInviteStatus.ACCEPTED:
                return cls("ACCEPTED")
            case GrpcInviteStatus.REJECTED:
                return cls("REJECTED")

        raise ValueError("Unknown invite status")

    def to_proto(self) -> GrpcInviteStatus:
        """
        Get proto invite status from invite status instance

        Returns
        -------
        GrpcInviteStatus
            Proto invite status

        """
        match self:
            case InviteStatus.PENDING:
                return GrpcInviteStatus.PENDING
            case InviteStatus.ACCEPTED:
                return GrpcInviteStatus.ACCEPTED
            case InviteStatus.REJECTED:
                return GrpcInviteStatus.REJECTED

        raise ValueError("Unknown invite status")


class Invite(BaseModel):
    """
    Invite data class

    Attributes
    ----------
    id : UUID4 | str
        Id of the invite
    event_id : UUID4 | str
        Id of the related event
    author_id : UUID4 | str
        Id of the author of the invite
    invitee_id : UUID4 | str
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

    id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    event_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    author_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    invitee_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    status: InviteStatus = InviteStatus.PENDING
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
                proto.created_at.seconds + proto.created_at.nanos / 1e9,
                tz=UTC
            ),
            deleted_at=datetime.fromtimestamp(
                proto.deleted_at.seconds + proto.deleted_at.nanos / 1e9,
                tz=UTC
            )
            if proto.WhichOneof("optional_deleted_at") is not None
            else None,
        )

    def to_proto(self) -> GrpcInvite:
        """
        Get proto invite from invite instance

        Returns
        -------
        GrpcInvite
            Proto invite

        """
        invite = GrpcInvite(
            id=str(self.id),
            event_id=str(self.event_id),
            author_id=str(self.author_id),
            invitee_id=str(self.invitee_id),
            status=self.status.to_proto(),
        )

        invite.created_at.FromDatetime(self.created_at.astimezone(utc)),

        if self.deleted_at is not None:
            invite.deleted_at.FromDatetime(self.deleted_at.astimezone(utc))

        return invite
