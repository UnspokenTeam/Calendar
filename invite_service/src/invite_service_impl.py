"""Invite Service Controller"""

import grpc

from errors import PermissionDeniedError
from src.generated.invite_service.invite_service_pb2 import (
    GetAllInvitesRequest as GrpcGetAllInvitesRequest,
)
from src.generated.invite_service.invite_service_pb2_grpc import (
    InviteServiceServicer as GrpcServicer,
)
from src.generated.user.user_pb2 import GrpcUserType
from src.models.invite import Invite, InviteStatus
from src.repository.invite_repository_interface import InviteRepositoryInterface
import src.generated.invite_service.invite_service_pb2 as proto

from google.protobuf.empty_pb2 import Empty


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
    async get_invites_by_event_id(request, context)
        Function that need to be bind to the server that returns invites list by event id.
    async get_all_invites(request, context)
        Function that need to be bind to the server that returns all invites in list.
    async get_invite_by_invite_id(request, context)
        Function that need to be bind to the server that returns invite.
    async get_invites_by_invitee_id(request, context)
        Function that need to be bind to the server that returns invites list by invitee id.
    async create_invite(request, context)
        Function that need to be bind to the server that creates the invite or updates the existing one.
    async create_multiple_invites(request, context)
        Function that need to be bind to the server that creates multiple invites or updates the existing ones.
    async update_invite(request, context)
        Function that need to be bind to the server that updates the invite.
    async delete_invite_by_id(request, context)
        Function that need to be bind to the server that deletes invite by invite id.
    async delete_invites_by_event_id(request, context)
        Function that need to be bind to the server that deletes invites by event id.
    async delete_invites_by_author_id(request, context)
        Function that need to be bind to the server that deletes invites by author id.
    async delete_invites_by_invitee_id(request, context)
        Function that need to be bind to the server that deletes invites by invitee id.

    """

    _invite_repository: InviteRepositoryInterface

    def __init__(self, invite_repository: InviteRepositoryInterface) -> None:
        self._invite_repository = invite_repository

    async def get_invites_by_event_id(
        self, request: proto.InvitesByEventIdRequest, context: grpc.ServicerContext
    ) -> proto.InvitesResponse:
        """
        Get all invites by event id.

        Parameters
        ----------
        request : proto.InvitesByEventIdRequest
            Event id and optional invite status
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.InvitesResponse
            Invites list.

        """
        invites = await self._invite_repository.get_invites_by_event_id(
            event_id=request.event_id,
            status=InviteStatus.from_proto(request.invite_status)
            if request.WhichOneof("optional_invite_status") is not None
            else None,
            page_number=request.page_number,
            items_per_page=request.items_per_page,
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.InvitesResponse(
            invites=proto.ListOfInvites(
                invites=[invite.to_grpc_invite() for invite in invites]
            )
        )

    async def get_invites_by_author_id(
        self, request: proto.InvitesByAuthorIdRequest, context: grpc.ServicerContext
    ) -> proto.ListOfInvites:
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
        proto.ListOfInvites
            Invites object for several invites.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if (
            request.requesting_user.id != request.author_id
            and request.requesting_user.type != GrpcUserType.ADMIN
        ):
            raise PermissionDeniedError("Permission denied")
        invites = await self._invite_repository.get_invites_by_author_id(
            author_id=request.author_id,
            status=InviteStatus.from_proto(request.invite_status)
            if request.WhichOneof("optional_invite_status") is not None
            else None,
            page_number=request.page_number,
            items_per_page=request.items_per_page,
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfInvites(
            invites=[invite.to_grpc_invite() for invite in invites]
        )

    async def get_all_invites(
        self, request: GrpcGetAllInvitesRequest, context: grpc.ServicerContext
    ) -> proto.ListOfInvites:
        """
        Get all invites.

        Parameters
        ----------
        request : GrpcGetAllInvitesRequest
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.ListOfInvites
            Response object for several invites.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if request.requesting_user.type != GrpcUserType.ADMIN:
            raise PermissionDeniedError("Permission denied")
        invites = await self._invite_repository.get_all_invites(
            status=InviteStatus.from_proto(request.invite_status)
            if request.WhichOneof("optional_invite_status") is not None
            else None,
            page_number=request.page_number,
            items_per_page=request.items_per_page,
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfInvites(
            invites=[invite.to_grpc_invite() for invite in invites]
        )

    async def get_invite_by_invite_id(
        self, request: proto.InviteRequestByInviteId, context: grpc.ServicerContext
    ) -> proto.GrpcInvite:
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
        proto.GrpcInvite
            Response object for invite.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
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
        return invite.to_grpc_invite()

    async def get_invites_by_invitee_id(
        self, request: proto.GetInvitesByInviteeIdRequest, context: grpc.ServicerContext
    ) -> proto.ListOfInvites:
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
        proto.ListOfInvites
            Invites object for several invite.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if (
            request.requesting_user.id != request.invitee_id
            and request.requesting_user.type != GrpcUserType.ADMIN
        ):
            raise PermissionDeniedError("Permission denied")
        invites = await self._invite_repository.get_invites_by_invitee_id(
            invitee_id=request.invitee_id,
            status=InviteStatus.from_proto(request.invite_status)
            if request.WhichOneof("optional_invite_status") is not None
            else None,
            page_number=request.page_number,
            items_per_page=request.items_per_page,
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfInvites(
            invites=[invite.to_grpc_invite() for invite in invites]
        )

    async def create_invite(
        self, request: proto.InviteRequest, context: grpc.ServicerContext
    ) -> proto.GrpcInvite:
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
        proto.GrpcInvite
            Response object for invite.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        invite = Invite.from_grpc_invite(request.invite)
        if (
            request.requesting_user.id != invite.author_id
            and request.requesting_user.type != GrpcUserType.ADMIN
        ):
            raise PermissionDeniedError("Permission denied")
        await self._invite_repository.create_invite(invite=invite)
        context.set_code(grpc.StatusCode.OK)
        return invite.to_grpc_invite()

    async def create_multiple_invites(
        self, request: proto.InvitesRequest, context: grpc.ServicerContext
    ) -> proto.ListOfInvites:
        """
        Create multiple invites.

        Parameters
        ----------
        request : proto.InvitesRequest
            Request data containing GrpcInvites.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.ListOfInvites
            Response object for invites.

        """
        if any(
            [
                invite.author_id != request.requesting_user.id
                for invite in request.invites.invites
            ]
        ):
            raise PermissionDeniedError("Permission denied")
        invites = await self._invite_repository.create_multiple_invites(
            invites=[
                Invite.from_grpc_invite(invite) for invite in request.invites.invites
            ]
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfInvites(
            invites=[invite.to_grpc_invite() for invite in invites]
        )

    async def update_invite(
        self, request: proto.InviteRequest, context: grpc.ServicerContext
    ) -> proto.GrpcInvite:
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
        proto.GrpcInvite
            Response object for invite.

        """
        invite = Invite.from_grpc_invite(request.invite)
        if (
            request.requesting_user.id != invite.author_id
            and request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != invite.invitee_id
        ):
            raise PermissionDeniedError("Permission denied")
        await self._invite_repository.update_invite(invite=invite)
        context.set_code(grpc.StatusCode.OK)
        return invite.to_grpc_invite()

    async def delete_invite_by_id(
        self, request: proto.DeleteInviteByIdRequest, context: grpc.ServicerContext
    ) -> Empty:
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
        Empty
            Empty response object.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
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
        return Empty()

    async def delete_invites_by_event_id(
        self,
        request: proto.DeleteInvitesByEventIdRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
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
        Empty
            Empty response object.

        """
        if (
            request.requesting_user.id != request.event_id
            and request.requesting_user.type != GrpcUserType.ADMIN
        ):
            raise PermissionDeniedError("Permission denied")
        await self._invite_repository.delete_invites_by_event_id(
            event_id=request.event_id
        )
        context.set_code(grpc.StatusCode.OK)
        return Empty()

    async def delete_invites_by_author_id(
        self,
        request: proto.DeleteInvitesByAuthorIdRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
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
        Empty
            Empty response object.

        """
        if (
            request.requesting_user.id != request.author_id
            and request.requesting_user.type != GrpcUserType.ADMIN
        ):
            raise PermissionDeniedError("Permission denied")
        await self._invite_repository.delete_invites_by_author_id(
            author_id=request.author_id
        )
        context.set_code(grpc.StatusCode.OK)
        return Empty()

    async def delete_invites_by_invitee_id(
        self,
        request: proto.DeleteInvitesByInviteeIdRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
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
        Empty
            Empty response object.

        """
        if (
            request.requesting_user.id != request.invitee_id
            and request.requesting_user.type != GrpcUserType.ADMIN
        ):
            raise PermissionDeniedError("Permission denied")
        await self._invite_repository.delete_invites_by_invitee_id(
            invitee_id=request.invitee_id
        )
        context.set_code(grpc.StatusCode.OK)
        return Empty()
