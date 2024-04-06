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
        List of invites.

    Methods
    -------
    get_invites_by_user_id(request, context)
        Function that need to be bind to the server that returns invites list by user id.
    create_invite(request, context)
        Function that need to be bind to the server that creates the invite.
    update_invite(request, context)
        Function that need to be bind to the server that updates the invite.
    delete_invite(request, context)
        Function that need to be bind to the server that deletes the invite.
     get_invites_by_invitee_id(request, context)
        Function that need to be bind to the server that returns invites list by invitee id.

    """

    def __init__(self) -> None:
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
        Get all invites by user id.

        Parameters
        ----------
        request : proto.InvitesByUserIdRequest
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.InvitesResponse
            Invites object for invite response.

        """
        context.set_code(grpc.StatusCode.OK)

        return proto.InvitesResponse(
            code=200,
            invites=proto.ListOfInvites(
                invites=[
                    invite.to_grpc_invite()
                    for invite in self.invites
                    if invite.author_id == request.author_id
                ]
            ),
        )

    def get_invites_by_invitee_id(
        self, request: proto.GetInviteeByInviteIdRequest, context: grpc.ServicerContext
    ) -> proto.InvitesResponse:
        """
        Get all invites by invitee id.

        Parameters
        ----------
        request : proto.GetInviteeByInviteIdRequest
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.InvitesResponse
            Invites object for invite response.

        """
        pass

    def create_invite(
        self, request: proto.Invite, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Create invite.

        Parameters
        ----------
        request : proto.Invite
            Request data containing GrpcInvite.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.BaseResponse
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
        request : proto.Invite
            Request data containing GrpcInvite.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.BaseResponse
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
        request : proto.DeleteInviteRequest
            Request data containing invite ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.BaseResponse
            Object containing status code and message if the response status is not 200.

        """
        pass
