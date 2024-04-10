"""Invite Service Controller"""
import grpc

import prisma.errors

from proto.invite_service_pb2_grpc import InviteServiceServicer as GrpcServicer
import proto.invite_service_pb2 as proto

from google.protobuf.empty_pb2 import Empty
from errors.value_not_found_error import ValueNotFoundError
from src.models.invite import Invite
from repository.invite_repository_interface import InviteRepositoryInterface


class InviteServiceImpl(GrpcServicer):
    """
    Implementation of the Invite Service.

    Attributes
    ----------
    _invite_repository: InviteRepositoryInterface

    Methods
    -------
    async get_invites_by_author_id(request, context)
        Function that need to be bind to the server that returns invites list by author id.
    async get_all_invites(request, context)
        Function that need to be bind to the server that returns all invites in list.
    async get_invite_by_invite_id(request, context)
        Function that need to be bind to the server that returns invite.
    async get_invites_by_invitee_id(request, context)
        Function that need to be bind to the server that returns invites list by invitee id.
    async create_invite(request, context)
        Function that need to be bind to the server that creates the invite.
    async update_invite(request, context)
        Function that need to be bind to the server that updates the invite.
    async delete_invite(request, context)
        Function that need to be bind to the server that deletes the invite.

    """

    _invite_repository: InviteRepositoryInterface

    def __init__(self, invite_repository: InviteRepositoryInterface) -> None:
        self._invite_repository = invite_repository

    async def get_invites_by_author_id(
        self, request: proto.InvitesByAuthorIdRequest, context: grpc.ServicerContext
    ) -> proto.InvitesResponse:
        """
        Get all invites by author id.

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
        try:
            invites = await self._invite_repository.get_invites_by_author_id(
                author_id=request.author_id,
            )
            context.set_code(grpc.StatusCode.OK)
            return proto.InvitesResponse(
                status_code=200,
                invites=proto.ListOfInvites(
                    invites=[invite.to_grpc_invite() for invite in invites]
                ),
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.InvitesResponse(status_code=404, message="Invite not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.InvitesResponse(
                status_code=500, message="Internal server error"
            )

    async def get_all_invites(
        self, request: Empty, context: grpc.ServicerContext
    ) -> proto.InvitesResponse:
        """
        Get all invites.

        Parameters
        ----------
        request : Empty
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        List[Invite]
            List of all invites.

        Raises
        ------
        InvitesResponse
            Response object for invite response.

        """
        try:
            if request.user.type != proto.GrpcUserType.ADMIN:
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                return proto.InvitesResponse(
                    status_code=403, message="Permission denied"
                )
            invites = await self._invite_repository.get_all_invites()
            context.set_code(grpc.StatusCode.OK)
            return proto.InvitesResponse(
                status_code=200,
                invites=proto.ListOfInvites(
                    invites=[invite.to_grpc_invite() for invite in invites]
                ),
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.InvitesResponse(status_code=404, message="Invites not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.InvitesResponse(
                status_code=500, message="Internal server error"
            )

    async def get_invite_by_invite_id(
        self, request: proto.InviteRequestByInviteId, context: grpc.ServicerContext
    ) -> proto.InviteResponse:
        """
        Get invite by invite id.

        Parameters
        ----------
        request : proto.InviteRequestByInviteId
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.InviteResponse
            Response object for invite response.

        """
        try:
            invite = await self._invite_repository.get_invite_by_invite_id(
                invite_id=request.invite_id
            )
            context.set_code(grpc.StatusCode.OK)
            return proto.InviteResponse(status_code=200, invite=invite.to_grpc_invite())
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.InviteResponse(status_code=404, message="Invites not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.InviteResponse(
                status_code=500, message="Internal server error"
            )

    async def get_invites_by_invitee_id(
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
        try:
            invites = await self._invite_repository.get_invites_by_invitee_id(
                invitee_id=request.invite_id,
            )
            context.set_code(grpc.StatusCode.OK)
            return proto.InvitesResponse(
                status_code=200,
                invites=proto.ListOfInvites(
                    invites=[invite.to_grpc_invite() for invite in invites]
                ),
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.InvitesResponse(status_code=404, message="Invites not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.InvitesResponse(
                status_code=500, message="Internal server error"
            )

    async def create_invite(
        self, request: proto.InviteRequest, context: grpc.ServicerContext
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
        try:
            invite = Invite.from_grpc_invite(request.invite)
            await self._invite_repository.create_invite(invite=invite)
            context.set_code(grpc.StatusCode.OK)
            return proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.BaseResponse(status_code=404, message="Invite not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")

    async def update_invite(
        self, request: proto.InviteRequest, context: grpc.ServicerContext
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
        try:
            invite = Invite.from_grpc_invite(request.invite)
            await self._invite_repository.update_invite(invite=invite)
            context.set_code(grpc.StatusCode.OK)
            return proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.BaseResponse(status_code=404, message="Invite not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")

    async def delete_invite(
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
        try:
            await self._invite_repository.delete_invite(invite_id=request.invite_id)
            context.set_code(grpc.StatusCode.OK)
            return proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.BaseResponse(status_code=404, message="Invite not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")
