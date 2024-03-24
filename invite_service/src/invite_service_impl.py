"""Invite Service Controller"""

import grpc

from proto.invite_service_pb2_grpc import InviteServiceServicer as GrpcServicer
import proto.invite_service_pb2 as proto
from src.models.invite import Invite


class InviteServiceImpl(GrpcServicer):
    """
    Implementation of the Event Service.

    Attributes
    ----------
    invites : List[Invite]
        List of invites

    Methods
    -------
    get_invites_by_user_id()
        Function that need to be bind to the server that returns invites list.
    create_invite()
        Function that need to be bind to the server that creates the invite.
    update_invite()
        Function that need to be bind to the server that updates the invite.
    delete_invite()
        Function that need to be bind to the server that deletes the invite.
    """

    def __init__(self):
        self.invites = [
            Invite(
                "id", "event_id", "author_id", "invitee_id", proto.InviteStatus.PENDING
            ),
            Invite(
                "id", "event_id", "author_id", "invitee_id", proto.InviteStatus.PENDING
            ),
        ]

    def get_invites_by_user_id(
        self, request: proto.InvitesByUserIdRequest, context: grpc.ServicerContext
    ) -> proto.InvitesResponse:
        """
        Get all invites.

        Parameters
        ----------
        request : InvitesByUserIdRequest
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        InvitesResponse
            Invites object for event response.
        """
        return proto.InvitesResponse(
            code=200,
            invites=proto.ListOfInvites(
                invites=[invite.to_grpc_invite() for invite in self.invites]
            ),
        )

    def create_invite(
        self, request: proto.Invite, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Create invite.

        Parameters
        ----------
        request : GrpcInvite
            Request data containing GrpcInvite.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        BaseResponse
            Object containing status code and message if the response status is not 200.
        """
        pass

    def update_invite(
        self, request: proto.Invite, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Update invite.

        Parameters
        ----------
        request : GrpcInvite
            Request data containing GrpcInvite.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        BaseResponse
            Object containing status code and message if the response status is not 200.
        """
        pass

    def delete_invite(
        self, request: proto.DeleteInviteRequest, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Delete invite.

        Parameters
        ----------
        request : DeleteInviteRequest
            Request data containing invite ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        BaseResponse
            Object containing status code and message if the response status is not 200.
        """
        pass
