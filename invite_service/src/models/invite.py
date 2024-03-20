from dataclasses import dataclass
from proto.invite_service_pb2 import Invite as GrpcInvite, InviteStatus


@dataclass
class Invite:
    id: str
    event_id: str
    author_id: str
    invitee_id: str
    status: InviteStatus

    def to_grpc_invite(self) -> GrpcInvite:
        invite = GrpcInvite(
            id=self.id,
            event_id=self.event_id,
            author_id=self.author_id,
            invitee_id=self.invitee_id,
            status=self.status,
        )

        return invite
