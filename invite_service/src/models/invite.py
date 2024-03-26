"""Invite Model"""
from dataclasses import dataclass
from proto.invite_service_pb2 import Invite as GrpcInvite, InviteStatus


@dataclass
class Invite:
    """
    Data class that stores user information

    Attributes
    ----------
    id : str
        ID of the user
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
        invite = GrpcInvite(
            id=self.id,
            event_id=self.event_id,
            author_id=self.author_id,
            invitee_id=self.invitee_id,
            status=self.status,
        )

        return invite
