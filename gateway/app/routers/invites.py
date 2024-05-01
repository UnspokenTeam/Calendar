import logging
from datetime import datetime
from typing import List, Annotated

from fastapi import APIRouter, Security, Depends
from grpc import RpcError
from pydantic import Field, BaseModel, AfterValidator

from app.errors import PermissionDeniedError
from app.generated.event_service.event_service_pb2 import (
    EventRequestByEventId as GrpcGetEventByEventIdRequest,
    EventsResponse as GrpcEventsResponse,
    ListOfEventsIds as GrpcListOfEventsIds,
    EventsRequestByEventsIds as GrpcGetEventsByEventIdsRequest,
)
from app.generated.identity_service.get_user_pb2 import (
    UserByIdRequest as GrpcGetUserByIdRequest,
    UsersByIdRequest as GrpcGetUsersByIdRequest,
    UsersResponse as GrpcUsersResponse,
)
from app.generated.notification_service.notification_service_pb2 import (
    DeleteNotificationsByEventsAndAuthorIdsRequest as GrpcDeleteNotificationsByEventsAndAuthorIdsRequest,
    ListOfIds as GrpcListOfNotificationIds,
)
from app.generated.invite_service.invite_service_pb2 import (
    GetInvitesByInviteeIdRequest as GrpcGetInvitesByInviteeIdRequest,
    InvitesResponse as GrpcInvitesResponse,
    InvitesByAuthorIdRequest as GrpcGetInvitesByAuthorIdRequest,
    InviteRequestByInviteId as GrpcGetInviteByInviteIdRequest,
    InviteResponse as GrpcInviteResponse,
    InviteRequest as GrpcInviteRequest,
    DeleteInviteByIdRequest as GrpcDeleteInviteByIdRequest,
    InviteStatus as GrpcInviteStatus,
    GetAllInvitesRequest as GrpcGetAllInvitesRequest,
    InvitesRequest as GrpcInvitesRequest,
    ListOfInvites as GrpcListOfInvites,
)
from app.validators import str_special_characters_validator
from app.generated.user.user_pb2 import GrpcUser, GrpcUserType
from app.middleware import auth
from app.models import Invite, InviteStatus
from app.params import GrpcClientParams

router = APIRouter(prefix="/invites", tags=["invites"])


class CreateInviteData(BaseModel):
    invitee_id: Annotated[
        str, Field("", min_length=1), AfterValidator(str_special_characters_validator)
    ]
    event_id: Annotated[
        str, Field("", min_length=1), AfterValidator(str_special_characters_validator)
    ]


@router.get("/all/")
async def get_all_invites(
    page: Annotated[int, Field(1, ge=1)],
    items_per_page: Annotated[int, Field(-1, ge=-1)],
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> List[Invite]:
    """
    \f
    Fast api route to get all invites

    Parameters
    ----------
    page : int
        Page number
    items_per_page : int
        Number of items per page
    user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Returns
    -------
    List[Invite]
        List of all invites

    """
    if user.type != GrpcUserType.ADMIN:
        raise PermissionDeniedError("Permission denied")

    invites_response: GrpcInvitesResponse = (
        grpc_clients.invite_service_client.request().get_all_invites(
            GrpcGetAllInvitesRequest(
                page_number=page,
                items_per_page=items_per_page,
                requesting_user=user,
            )
        )
    )
    return [Invite.from_proto(invite) for invite in invites_response.invites.invites]


@router.get("/my/invitee/")
async def get_users_invitee_invites(
    page: Annotated[int, Field(1, ge=1)],
    items_per_page: Annotated[int, Field(-1, ge=-1)],
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> List[Invite]:
    """
    \f
    Fast api route to get all invites where current user is invitee

    Parameters
    ----------
    page : int
        Page number
    items_per_page : int
        Number of items to return per page
    user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Returns
    -------
    List[Invite]
        Invites where user is an invitee

    """
    invites_request: GrpcInvitesResponse = (
        grpc_clients.invite_service_client.request().get_invites_by_invitee_id(
            GrpcGetInvitesByInviteeIdRequest(
                invitee_id=user.id,
                requesting_user=user,
                page_number=page,
                items_per_page=items_per_page,
            )
        )
    )
    return [Invite.from_proto(invite) for invite in invites_request.invites.invites]


@router.get("/my/author/")
async def get_users_author_invites(
    page: Annotated[int, Field(1, ge=1)],
    items_per_page: Annotated[int, Field(-1, ge=-1)],
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> List[Invite]:
    """
    \f
    Fast api route to get invites where user is an author

    Parameters
    ----------
    page : int
        Page number
    items_per_page : int
        Number of items to return per page
    user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Returns
    -------
    List[Invites]
        Invites where user is an author

    """
    invites_request: GrpcInvitesResponse = (
        grpc_clients.invite_service_client.request().get_invites_by_author_id(
            GrpcGetInvitesByAuthorIdRequest(
                author_id=user.id,
                requesting_user=user,
                page_number=page,
                items_per_page=items_per_page,
            )
        )
    )

    return [Invite.from_proto(invite) for invite in invites_request.invites.invites]


@router.get("/{invite_id}")
async def get_invite_by_invite_id(
    invite_id: str,
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> Invite:
    """
    \f
    Fast api route to get information about the invite

    Parameters
    ----------
    invite_id : str
        Invite id
    user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Returns
    -------
    Invite
        Invite instance

    """
    invite_request: GrpcInviteResponse = (
        grpc_clients.invite_service_client.request().get_invite_by_invite_id(
            GrpcGetInviteByInviteIdRequest(invite_id=invite_id, requesting_user=user)
        )
    )

    return Invite.from_proto(invite_request.invite)


@router.post("/")
async def create_invite(
    invitee_id: str,
    event_id: str,
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f
    Fast api route to create an invite

    Parameters
    ----------
    invitee_id : str
        Invitee user id
    event_id : str
        Event id
    user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    """
    if user.id == invitee_id:
        raise ValueError("Invitee and author cannot be the same person")

    await check_permission_for_event(
        requesting_user=user, event_id=event_id, grpc_clients=grpc_clients
    )

    await check_user_existence(user_id=invitee_id, grpc_clients=grpc_clients)

    invite = Invite(
        id="id",
        event_id=event_id,
        invitee_id=invitee_id,
        author_id=user.id,
        status=InviteStatus.PENDING,
        created_at=datetime.now(),
    )

    grpc_clients.invite_service_client.request().create_invite(
        GrpcInviteRequest(invite=invite.to_proto(), requesting_user=user)
    )


@router.post("/multiple/")
async def create_multiple_invites(
    invites: List[CreateInviteData],
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f
    Fast api route to create multiple invites

    Parameters
    ----------
    invites : List[CreateInviteData]
    user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Raises
    ------
    ValueError
        If some users or events does not exist or user does not have permission to them

    """
    users: GrpcUsersResponse = (
        await grpc_clients.identity_service_client.request().get_users_by_id(
            GrpcGetUsersByIdRequest(
                page=1, items_per_page=-1, id=[invite.invitee_id for invite in invites]
            )
        )
    )
    if len(users.users.users) != len(invites):
        raise ValueError("Some users do not exist")

    events: GrpcEventsResponse = (
        await grpc_clients.event_service_client.request().get_events_by_events_ids(
            GrpcGetEventsByEventIdsRequest(
                page_number=1,
                items_per_page=-1,
                events_ids=GrpcListOfEventsIds(
                    ids=[invite.event_id for invite in invites]
                ),
            )
        )
    )
    if len(events.events.events) != len(invites) and all(
        [event.author_id == user.id for event in events.events.events]
    ):
        raise ValueError("Some events do not exist")

    await grpc_clients.invite_service_client.request().create_multiple_invites(
        GrpcInvitesRequest(
            invites=GrpcListOfInvites(
                invites=[
                    Invite(
                        id="id",
                        event_id=invite_data.event_id,
                        invitee_id=invite_data.invitee_id,
                        author_id=user.id,
                        status=InviteStatus.PENDING,
                        created_at=datetime.now(),
                    ).to_proto()
                    for invite_data in invites
                ]
            )
        )
    )


@router.put("/")
async def update_invite(
    invite: Invite,
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f
    Fast api route to update invite data

    Parameters
    ----------
    invite : Invite
        Invite instance
    user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    """
    if invite.author_id != user.id and invite.invitee_id != user.id:
        raise PermissionDeniedError

    if invite.author_id == invite.invitee_id:
        raise ValueError("Invitee and author cannot be the same person")

    db_invite_response: GrpcInviteResponse = (
        grpc_clients.invite_service_client.request().get_invite_by_invite_id(
            GrpcGetInviteByInviteIdRequest(invite_id=invite.id, requesting_user=user)
        )
    )
    db_invite = Invite.from_proto(db_invite_response.invite)

    if db_invite.event_id != invite.event_id:
        _ = grpc_clients.event_service_client.request().get_event_by_event_id(
            GrpcGetEventByEventIdRequest(event_id=invite.event_id, requesting_user=user)
        )

    if db_invite.invitee_id != invite.invitee_id:
        _ = grpc_clients.identity_service_client.request().get_user_by_id(
            GrpcGetUserByIdRequest(user_id=invite.invitee_id)
        )

    invite.created_at = db_invite.created_at
    invite.deleted_at = db_invite.deleted_at

    grpc_clients.invite_service_client.request().update_invite(
        GrpcInviteRequest(
            invite=invite.to_proto(),
            requesting_user=user,
        )
    )


@router.delete("/")
async def delete_invite(
    invite_id: str,
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f
    Fast api route to delete invite

    Parameters
    ----------
    invite_id : str
        Delete invite
    user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    """
    invite_response: GrpcInviteResponse = (
        grpc_clients.invite_service_client.request().get_invite_by_invite_id(
            GrpcGetInviteByInviteIdRequest(invite_id=invite_id, requesting_user=user)
        )
    )

    invite = Invite.from_proto(invite_response.invite)

    grpc_clients.invite_service_client.request().delete_invite_by_id(
        GrpcDeleteInviteByIdRequest(invite_id=invite_id, requesting_user=user)
    )

    try:
        grpc_clients.notification_service_client.request().delete_notifications_by_events_and_author_ids(
            GrpcDeleteNotificationsByEventsAndAuthorIdsRequest(
                event_ids=GrpcListOfNotificationIds(ids=[invite.event_id]),
                author_id=user.id,
                requesting_user=user,
            )
        )
    except RpcError:
        pass


async def check_permission_for_event(
    requesting_user: GrpcUser, event_id: str, grpc_clients: GrpcClientParams
) -> None:
    """
    \f
    Check if user can access event.

    Parameters
    ----------
    requesting_user : GrpcUser
        User's data
    event_id : str
        Event id
    grpc_clients: GrpcClientParams
        Grpc clients

    Raises
    ------
    PermissionDeniedError
        Permission denied

    """
    try:
        _ = grpc_clients.event_service_client.request().get_event_by_event_id(
            GrpcGetEventByEventIdRequest(
                event_id=event_id,
                requesting_user=requesting_user,
            )
        )
    except RpcError as e:
        logging.error(e.details())
        invites: GrpcInvitesResponse = (
            grpc_clients.invite_service_client.request().get_invites_by_invitee_id(
                GrpcGetInvitesByInviteeIdRequest(
                    invitee_id=requesting_user.id,
                    invite_status=GrpcInviteStatus.ACCEPTED,
                    requesting_user=requesting_user,
                    page_number=1,
                    items_per_page=-1,
                )
            )
        )
        if not any([invite.event_id == event_id for invite in invites.invites.invites]):
            raise PermissionDeniedError("Permission denied")


async def check_user_existence(user_id: str, grpc_clients: GrpcClientParams) -> None:
    """
    \f
    Check if user with given id exists

    Parameters
    ----------
    user_id : str
        User's id
    grpc_clients : GrpcClientParams
        Grpc clients

    """
    _ = grpc_clients.identity_service_client.request().get_user_by_id(
        GrpcGetUserByIdRequest(user_id=user_id)
    )
