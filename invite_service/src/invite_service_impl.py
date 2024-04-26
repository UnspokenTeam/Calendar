"""Invite Service Controller"""

import grpc
import prisma.errors

import generated.invite_service.invite_service_pb2 as proto
from errors.permission_denied import PermissionDeniedError
from errors.value_not_found_error import ValueNotFoundError
from generated.invite_service.invite_service_pb2 import (
    GetAllInvitesRequest as GrpcGetAllInvitesRequest,
    InviteStatus as GrpcInviteStatus,
)
from generated.invite_service.invite_service_pb2_grpc import (
    InviteServiceServicer as GrpcServicer,
)
from generated.user.user_pb2 import GrpcUserType
from repository.invite_repository_interface import InviteRepositoryInterface
from src.models.invite import Invite, InviteStatus


class InviteServiceImpl(GrpcServicer):
    """
    Implementation of the Invite Service.

    Attributes
    ----------
    _invite_repository: InviteRepositoryInterface
        Invite repository interface attribute.

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
        request : proto.InvitesByAuthorIdRequest
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.InvitesResponse
            Invites object for invite response.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        try:
            if (
                request.requesting_user != request.author_id
                and request.requesting_user.type != GrpcUserType.ADMIN
            ):
                raise PermissionDeniedError("Permission denied")
            invites = await self._invite_repository.get_invites_by_author_id(
                author_id=request.author_id,
                status=InviteStatus.from_proto(request.invite_status)
                if request.invite_status != GrpcInviteStatus.UNSPECIFIED
                else None,
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
        except PermissionDeniedError:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return proto.InvitesResponse(status_code=403, message="Permission denied")

    async def get_all_invites(
        self, request: GrpcGetAllInvitesRequest, context: grpc.ServicerContext
    ) -> proto.InvitesResponse:
        """
        Get all invites.

        Parameters
        ----------
        request : proto.RequestingUser
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.InvitesResponse
            Response object for invite response.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        try:
            if request.requesting_user.type != GrpcUserType.ADMIN:
                raise PermissionDeniedError("Permission denied")
            invites = await self._invite_repository.get_all_invites(
                status=InviteStatus.from_proto(request.invite_status)
                if request.invite_status != GrpcInviteStatus.UNSPECIFIED
                else None
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
        except PermissionDeniedError:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return proto.InvitesResponse(status_code=403, message="Permission denied")

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

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        try:
            invite = await self._invite_repository.get_invite_by_invite_id(
                invite_id=request.invite_id
            )
            if (
                request.requesting_user.id != invite.author_id
                and request.requesting_user.id != invite.invitee_id
                and request.requesting_user.type != GrpcUserType.ADMIN
            ):
                raise PermissionDeniedError("Permission denied")
            context.set_code(grpc.StatusCode.OK)
            return proto.InviteResponse(status_code=200, invite=invite.to_grpc_invite())
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.InviteResponse(status_code=404, message="Invite not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.InviteResponse(
                status_code=500, message="Internal server error"
            )
        except PermissionDeniedError:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return proto.InviteResponse(status_code=403, message="Permission denied")

    async def get_invites_by_invitee_id(
        self, request: proto.GetInvitesByInviteeIdRequest, context: grpc.ServicerContext
    ) -> proto.InvitesResponse:
        """
        Get all invites by invitee id.

        Parameters
        ----------
        request : proto.GetInvitesByInviteeIdRequest
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.InvitesResponse
            Invites object for invite response.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        try:
            if (
                request.requesting_user.id != request.invitee_id
                and request.requesting_user.type != GrpcUserType.ADMIN
            ):
                raise PermissionDeniedError("Permission denied")
            invites = await self._invite_repository.get_invites_by_invitee_id(
                invitee_id=request.invitee_id,
                status=InviteStatus.from_proto(request.invite_status)
                if request.invite_status != GrpcInviteStatus.UNSPECIFIED
                else None,
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
        except PermissionDeniedError:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return proto.InvitesResponse(status_code=403, message="Permission denied")

    async def create_invite(
        self, request: proto.InviteRequest, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Create invite.

        Parameters
        ----------
        request : proto.InviteRequest
            Request data containing GrpcInvite.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.BaseResponse
            Object containing status code and message if the response status is not 200.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        try:
            invite = Invite.from_grpc_invite(request.invite)
            if (
                request.requesting_user.id != invite.author_id
                and request.requesting_user.type != GrpcUserType.ADMIN
            ):
                raise PermissionDeniedError("Permission denied")
            await self._invite_repository.create_invite(invite=invite)
            context.set_code(grpc.StatusCode.OK)
            return proto.BaseResponse(status_code=200)
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")
        except PermissionDeniedError:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return proto.BaseResponse(status_code=403, message="Permission denied")

    async def update_invite(
        self, request: proto.InviteRequest, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Update invite.

        Parameters
        ----------
        request : proto.InviteRequest
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

    async def delete_invite_by_id(
        self, request: proto.DeleteInviteByIdRequest, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Delete invite by invite id.

        Parameters
        ----------
        request : proto.DeleteInviteByIdRequest
            Request data containing invite ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.BaseResponse
            Object containing status code and message if the response status is not 200.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        try:
            invite = await self._invite_repository.get_invite_by_invite_id(
                request.invite_id
            )
            if (
                request.requesting_user.id != invite.author_id
                and request.requesting_user.type != GrpcUserType.ADMIN
            ):
                raise PermissionDeniedError("Permission denied")
            await self._invite_repository.delete_invite_by_invite_id(
                invite_id=request.invite_id
            )
            context.set_code(grpc.StatusCode.OK)
            return proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.BaseResponse(status_code=404, message="Invite not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")
        except PermissionDeniedError:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return proto.BaseResponse(status_code=403, message="Permission denied")

    async def delete_invites_by_event_id(
        self,
        request: proto.DeleteInvitesByEventIdRequest,
        context: grpc.ServicerContext,
    ) -> proto.BaseResponse:
        """
        Delete invite by event id.

        Parameters
        ----------
        request : proto.DeleteInvitesByInviteeIdRequest
            Request data containing invitee ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.BaseResponse
            Object containing status code and message if the response status is not 200.

        """
        try:
            await self._invite_repository.delete_invites_by_event_id(
                event_id=request.event_id
            )
            return proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            return proto.BaseResponse(status_code=404, message="No invites found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")

    async def delete_invites_by_author_id(
        self,
        request: proto.DeleteInvitesByAuthorIdRequest,
        context: grpc.ServicerContext,
    ) -> proto.BaseResponse:
        """
        Delete invite by author id.

        Parameters
        ----------
        request : proto.DeleteInvitesByAuthorIdRequest
            Request data containing author ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.BaseResponse
            Object containing status code and message if the response status is not 200.

        """
        try:
            await self._invite_repository.delete_invites_by_author_id(
                author_id=request.author_id
            )
            return proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            return proto.BaseResponse(status_code=404, message="No invites found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")

    async def delete_invites_by_invitee_id(
        self,
        request: proto.DeleteInvitesByInviteeIdRequest,
        context: grpc.ServicerContext,
    ) -> proto.BaseResponse:
        """
        Delete invite by invitee id.

        Parameters
        ----------
        request : proto.DeleteInvitesByInviteeIdRequest
            Request data containing invitee ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.BaseResponse
            Object containing status code and message if the response status is not 200.

        """
        try:
            await self._invite_repository.delete_invites_by_invitee_id(
                invitee_id=request.invitee_id
            )
            return proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            return proto.BaseResponse(status_code=404, message="No invites found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")
