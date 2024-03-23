"""Invite Service Controller"""
import grpc

from proto.invite_service_pb2_grpc import InviteServiceServicer as GrpcServicer
import proto.invite_service_pb2 as proto
from proto.invite_service_pb2 import (
    Invite as GrpcInvite,
    InvitesRequestByUserId,
    InviteStatus as GrpcInviteStatus,
    InvitesResponseByUserId,
    ListOfInvites,
)
from src.models.invite import Invite


class InviteServiceImpl(GrpcServicer):
    def __init__(self):
        self.invites = [
            Invite(
                "id", "event_id", "author_id", "invitee_id", GrpcInviteStatus.PENDING
            ),
            Invite(
                "id", "event_id", "author_id", "invitee_id", GrpcInviteStatus.PENDING
            ),
        ]

    def get_invites_by_user_id(
        self, request: InvitesRequestByUserId, context: grpc.ServicerContext
    ) -> proto.InvitesResponseByUserId:
        return InvitesResponseByUserId(
            code=200,
            invites=ListOfInvites(
                invites=[invite.to_grpc_invite() for invite in self.invites]
            ),
        )

    def get_invites_by_event_id(
        self, request: InvitesResponseByUserId, context: grpc.ServicerContext
    ) -> proto.InvitesResponseByUserId:
        pass

    def update_status(
        self, request: GrpcInviteStatus, context: grpc.ServicerContext
    ) -> proto.Invite:
        pass

    def on_accept(
        self, request: GrpcInvite, context: grpc.ServicerContext
    ) -> proto.Invite:
        pass
