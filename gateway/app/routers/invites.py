"""Invite routes"""
from datetime import datetime
from typing import Annotated, List
from uuid import UUID, uuid4

from grpc import RpcError

from app.errors import PermissionDeniedError
from app.generated.event_service.event_service_pb2 import (
    EventRequestByEventId as GrpcGetEventByEventIdRequest,
)
from app.generated.event_service.event_service_pb2 import (
    EventsRequestByEventsIds as GrpcGetEventsByEventIdsRequest,
)
from app.generated.event_service.event_service_pb2 import (
    ListOfEvents as GrpcListOfEvents,
)
from app.generated.event_service.event_service_pb2 import (
    ListOfEventsIds as GrpcListOfEventsIds,
)
from app.generated.identity_service.get_user_pb2 import (
    ListOfUser as GrpcListOfUsers,
)
from app.generated.identity_service.get_user_pb2 import (
    UserByIdRequest as GrpcGetUserByIdRequest,
)
from app.generated.identity_service.get_user_pb2 import (
    UsersByIdRequest as GrpcGetUsersByIdRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    DeleteInviteByIdRequest as GrpcDeleteInviteByIdRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    GetAllInvitesRequest as GrpcGetAllInvitesRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    GetInvitesByInviteeIdRequest as GrpcGetInvitesByInviteeIdRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    InviteRequest as GrpcInviteRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    InviteRequestByInviteId as GrpcGetInviteByInviteIdRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    InviteResponse as GrpcInviteResponse,
)
from app.generated.invite_service.invite_service_pb2 import (
    InvitesByAuthorIdRequest as GrpcGetInvitesByAuthorIdRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    InvitesRequest as GrpcInvitesRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    InvitesResponse as GrpcInvitesResponse,
)
from app.generated.invite_service.invite_service_pb2 import (
    InviteStatus as GrpcInviteStatus,
)
from app.generated.invite_service.invite_service_pb2 import (
    ListOfInvites as GrpcListOfInvites,
)
from app.generated.notification_service.notification_service_pb2 import (
    DeleteNotificationsByEventsAndAuthorIdsRequest as GrpcDeleteNotificationsByEventsAndAuthorIdsRequest,
)
from app.generated.notification_service.notification_service_pb2 import (
    ListOfIds as GrpcListOfNotificationIds,
)
from app.generated.user.user_pb2 import GrpcUser, GrpcUserType
from app.middleware import auth
from app.models import Invite, InviteStatus
from app.params import GrpcClientParams

from fastapi import APIRouter, Depends
from pydantic import UUID4, AfterValidator, BaseModel, Field

router = APIRouter(prefix="/invites", tags=["invites"])


class CreateInviteData(BaseModel):
    """
    Create invite dataclass

    Attributes
    ----------
    invitee_id : UUID4 | str
        Invitee id
    event_id : UUID4 | str
        Event id

    """

    invitee_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    event_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]


@router.get("/all/")
async def get_all_invites(
    page: Annotated[int, Field(1, ge=1)],
    items_per_page: Annotated[int, Field(-1, ge=-1)],
    user: Annotated[GrpcUser, Depends(auth)],
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
    user : Annotated[GrpcUser, Depends(auth)]
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
    user: Annotated[GrpcUser, Depends(auth)],
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
    user : Annotated[GrpcUser, Depends(auth)]
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
    user: Annotated[GrpcUser, Depends(auth)],
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
    user : Annotated[GrpcUser, Depends(auth)]
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
    invite_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
    user: Annotated[GrpcUser, Depends(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> Invite:
    """
    \f

    Fast api route to get information about the invite

    Parameters
    ----------
    invite_id : UUID4 | str
        Invite id
    user : Annotated[GrpcUser, Depends(auth)]
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
            GrpcGetInviteByInviteIdRequest(invite_id=str(invite_id), requesting_user=user)
        )
    )

    return Invite.from_proto(invite_request.invite)


@router.post("/")
async def create_invite(
    invitee_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
    event_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
    user: Annotated[GrpcUser, Depends(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f

    Fast api route to create an invite

    Parameters
    ----------
    invitee_id : UUID4 | str
        Invitee user id
    event_id : UUID4 | str
        Event id
    user : Annotated[GrpcUser, Depends(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Raises
    ------
    ValueError
        Invitee and author ids are identical

    """
    if user.id == str(invitee_id):
        raise ValueError("Invitee and author cannot be the same person")

    await check_permission_for_event(
        requesting_user=user, event_id=event_id, grpc_clients=grpc_clients
    )

    await check_user_existence(user_id=invitee_id, grpc_clients=grpc_clients)

    invite = Invite(
        id=uuid4(),
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
    user: Annotated[GrpcUser, Depends(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f

    Fast api route to create multiple invites

    Parameters
    ----------
    invites : List[CreateInviteData]
    user : Annotated[GrpcUser, Depends(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Raises
    ------
    ValueError
        If some users or events does not exist or user does not have permission to them

    """
    invitee_ids = list(set([str(invite.invitee_id) for invite in invites]))
    users: GrpcListOfUsers = (
        await grpc_clients.identity_service_client.request().get_users_by_id(
            GrpcGetUsersByIdRequest(
                page=1, items_per_page=-1, id=invitee_ids
            )
        )
    )
    if len(users.users) != len(invitee_ids):
        raise ValueError("Some users do not exist")

    event_ids = list(set([str(invite.event_id) for invite in invites]))
    events: GrpcListOfEvents = (
        await grpc_clients.event_service_client.request().get_events_by_events_ids(
            GrpcGetEventsByEventIdsRequest(
                page_number=1,
                items_per_page=-1,
                events_ids=GrpcListOfEventsIds(
                    ids=event_ids
                ),
            )
        )
    )
    if len(events.events) != len(event_ids):
        raise ValueError("Some events do not exist")

    if any([event.author_id != user.id for event in events.events]):
        raise PermissionDeniedError("Permission denied")

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
    user: Annotated[GrpcUser, Depends(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f

    Fast api route to update invite data

    Parameters
    ----------
    invite : Invite
        Invite instance
    user : Annotated[GrpcUser, Depends(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Raises
    ------
    PermissionDeniedError
        Permission denied
    ValueError
        Author and Invitee id are identical

    """
    if str(invite.author_id) != user.id and str(invite.invitee_id) != user.id:
        raise PermissionDeniedError("Permission denied")

    if invite.author_id == invite.invitee_id:
        raise ValueError("Invitee and author cannot be the same person")

    db_invite_response: GrpcInviteResponse = (
        grpc_clients.invite_service_client.request().get_invite_by_invite_id(
            GrpcGetInviteByInviteIdRequest(invite_id=str(invite.id), requesting_user=user)
        )
    )
    db_invite = Invite.from_proto(db_invite_response.invite)

    if db_invite.event_id != invite.event_id:
        await check_permission_for_event(
            requesting_user=user, event_id=invite.event_id, grpc_clients=grpc_clients
        )

    if db_invite.invitee_id != invite.invitee_id:
        await check_user_existence(user_id=invite.invitee_id, grpc_clients=grpc_clients)

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
    invite_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
    user: Annotated[GrpcUser, Depends(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f

    Fast api route to delete invite

    Parameters
    ----------
    invite_id : UUID4 | str
        Delete invite
    user : Annotated[GrpcUser, Depends(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    """
    invite_response: GrpcInviteResponse = (
        grpc_clients.invite_service_client.request().get_invite_by_invite_id(
            GrpcGetInviteByInviteIdRequest(invite_id=str(invite_id), requesting_user=user)
        )
    )

    invite = Invite.from_proto(invite_response.invite)

    try:
        grpc_clients.notification_service_client.request().delete_notifications_by_events_and_author_ids(
            GrpcDeleteNotificationsByEventsAndAuthorIdsRequest(
                event_ids=GrpcListOfNotificationIds(ids=[str(invite.event_id)]),
                author_id=user.id,
                requesting_user=user,
            )
        )
    except RpcError:
        pass

    grpc_clients.invite_service_client.request().delete_invite_by_id(
        GrpcDeleteInviteByIdRequest(invite_id=str(invite_id), requesting_user=user)
    )


async def check_permission_for_event(
        requesting_user: GrpcUser,
        event_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
        grpc_clients: GrpcClientParams
) -> None:
    """
    \f

    Check if user can access event.

    Parameters
    ----------
    requesting_user : GrpcUser
        User's data
    event_id : UUID4 | str
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
                event_id=str(event_id),
                requesting_user=requesting_user,
            )
        )
    except RpcError:
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
        if len(invites.invites.invites) == 0 or not any([invite.event_id == event_id for invite in invites.invites.invites]) :
            raise PermissionDeniedError("Permission denied")


async def check_user_existence(user_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))], grpc_clients: GrpcClientParams) -> None:
    """
    \f

    Check if user with given id exists

    Parameters
    ----------
    user_id : UUID4 | str
        User's id
    grpc_clients : GrpcClientParams
        Grpc clients

    """
    _ = grpc_clients.identity_service_client.request().get_user_by_id(
        GrpcGetUserByIdRequest(user_id=str(user_id))
    )
