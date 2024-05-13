"""Invite Model"""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List, Optional, Self

from prisma.models import Invite as PrismaInvite

from src.generated.invite_service.invite_service_pb2 import (
    GrpcInvite,
)
from src.generated.invite_service.invite_service_pb2 import (
    InviteStatus as GrpcInviteStatus,
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

        raise ValueError("Invalid proto")

    def to_proto(self) -> GrpcInviteStatus:
        """
        Get proto invite status from invite status instance

        Returns
        -------
        GrpcInviteStatus
            Proto invite status

        """
        match self:
            case self.PENDING:
                return GrpcInviteStatus.PENDING
            case self.ACCEPTED:
                return GrpcInviteStatus.ACCEPTED
            case self.REJECTED:
                return GrpcInviteStatus.REJECTED


@dataclass
class Invite:
    """
    Data class that stores invite information

    Attributes
    ----------
    id : str
        ID of the invite
    event_id : str
        ID of the event
    author_id : str
        ID of the author
    invitee_id : str
        ID of the invitee
    status: InviteStatus:
        Invite status
    created_at : datetime
        Time when the invite was created.
    deleted_at: Optional[datetime]
        Time when the invite was deleted.


    Methods
    -------
    to_grpc_invite()
        Returns invite's information as a GrpcInvite class instance
    to_dict(exclude)
        Converts invite to dictionary.
    from_prisma_invite(prisma_invite)
        Converts prisma invite to invite object.
    from_grpc_invite(grpc_invite)
        Converts grpc invite to invite object.

    """

    id: str
    event_id: str
    author_id: str
    invitee_id: str
    status: InviteStatus
    created_at: datetime
    deleted_at: Optional[datetime] = None

    def to_grpc_invite(self) -> GrpcInvite:
        """
        Converts invite information to GrpcInvite

        Returns
        -------
        GrpcInvite
            Invite data in GrpcInvite instance

        """
        invite = GrpcInvite(
            id=self.id,
            event_id=self.event_id,
            author_id=self.author_id,
            invitee_id=self.invitee_id,
            status=self.status.to_proto(),
        )
        invite.created_at.FromNanoseconds(
            int(self.created_at.replace(tzinfo=datetime.now().tzinfo).timestamp() * 1e9)
        )
        if self.deleted_at is not None:
            invite.deleted_at.FromNanoseconds(
                int(
                    self.deleted_at.replace(tzinfo=datetime.now().tzinfo).timestamp()
                    * 1e9
                )
            )

        return invite

    def to_dict(self, exclude: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Converts invite data to dictionary.

        Parameters
        ----------
        exclude : Optional[List[str]]
            List of fields to exclude.

        Returns
        -------
        Dict[str, Any]
            Invent data dictionary.

        """
        exclude_set = (set(exclude) if exclude is not None else set()) | {"id"}
        attrs = vars(self)
        return {
            attr.lstrip("_"): value
            for attr, value in attrs.items()
            if attr not in exclude_set
        }

    @classmethod
    def from_prisma_invite(cls, prisma_invite: PrismaInvite) -> Self:
        """
        Converts prisma invite.

        Parameters
        ----------
        prisma_invite : PrismaInvite
            Prisma invite.
        Returns
        -------
        Invite
            Invite class instance.

        """
        return cls(
            id=prisma_invite.id,
            event_id=prisma_invite.event_id,
            author_id=prisma_invite.author_id,
            status=InviteStatus(prisma_invite.status),
            invitee_id=prisma_invite.invitee_id,
            created_at=prisma_invite.created_at,
            deleted_at=prisma_invite.deleted_at,
        )

    @classmethod
    def from_grpc_invite(cls, grpc_invite: GrpcInvite) -> Self:
        """
        Converts grpc invite.

        Parameters
        ----------
        grpc_invite : GrpcInvite
            Grpc invite.
        Returns
        -------
        Invite
            Invite class instance.

        """
        return cls(
            id=grpc_invite.id,
            event_id=grpc_invite.event_id,
            author_id=grpc_invite.author_id,
            invitee_id=grpc_invite.invitee_id,
            status=InviteStatus.from_proto(grpc_invite.status),
            created_at=datetime.utcfromtimestamp(
                grpc_invite.created_at.seconds + grpc_invite.created_at.nanos / 1e9
            ),
            deleted_at=(
                datetime.utcfromtimestamp(
                    grpc_invite.deleted_at.seconds + grpc_invite.deleted_at.nanos / 1e9
                )
                if grpc_invite.WhichOneof("optional_deleted_at") is not None
                else None
            ),
        )

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Invite):
            return NotImplemented
        return self.id == other.id
