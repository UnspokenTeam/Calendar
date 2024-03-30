"""Invite Model"""
from dataclasses import dataclass
from proto.invite_service_pb2 import Invite as GrpcInvite, InviteStatus
from typing import Optional, Self, List, Any, Dict

from prisma.models import Invite as PrismaInvite

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


    Methods
    -------
    to_grpc_invite()
        Returns invite's information as a GrpcInvite class instance

    """

    id: str
    event_id: str
    author_id: str
    invitee_id: str
    status: InviteStatus

    def to_grpc_invite(self) -> GrpcInvite:
        """
        Converts invite information to GrpcInvite

        Returns
        -------
        GrpcInvite
            Invite data in GrpcInvite instance

        """
        return GrpcInvite(
            id=self.id,
            event_id=self.event_id,
            author_id=self.author_id,
            invitee_id=self.invitee_id,
            status=self.status,
        )

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
        exclude_set = set(exclude if exclude is not None else ["id"])
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
            status=prisma_invite.status,
            invitee_id=prisma_invite.invitee_id,
        )
