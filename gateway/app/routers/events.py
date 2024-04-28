from datetime import datetime
from typing import Annotated, List, Optional

from fastapi import APIRouter, Security, Depends
from grpc import RpcError
from pydantic import BaseModel

from app.errors import PermissionDeniedError
from app.generated.event_service.event_service_pb2 import (
    EventsRequestByAuthorId as GrpcGetEventsByAuthorIdRequest,
    EventsResponse as GrpcGetEventsResponse,
    EventsRequestByEventsIds as GrpcGetEventsRequestByEventsIdsRequest,
    ListOfEventsIds,
    EventResponse as GrpcEventResponse,
    EventRequestByEventId as GrpcGetEventByEventIdRequest,
    DeleteEventRequest as GrpcDeleteEventRequest,
    EventRequest as GrpcEventRequest,
    GenerateDescriptionRequest as GrpcGenerateDescriptionRequest,
    GenerateDescriptionResponse as GrpcGenerateDescriptionResponse,
)
from app.generated.identity_service.get_user_pb2 import (
    UsersByIdRequest as GrpcGetUsersByIdsRequest,
    UsersResponse as GrpcGetUsersResponse,
)
from app.generated.invite_service.invite_service_pb2 import (
    GetInvitesByInviteeIdRequest as GrpcGetInvitesByInviteeIdRequest,
    InvitesResponse as GrpcGetInvitesResponse,
    DeleteInvitesByEventIdRequest as GrpcDeleteInvitesByEventIdRequest,
    InvitesByEventIdRequest as GrpcInvitesByEventIdRequest,
    InviteStatus,
)
from app.generated.notification_service.notification_service_pb2 import (
    DeleteNotificationsByEventIdRequest as GrpcDeleteNotificationsByEventIdRequest,
)
from app.generated.notification_service.notification_service_pb2 import (
    NotificationResponse as GrpcNotificationResponse,
)
from app.generated.user.user_pb2 import GrpcUser
from app.middleware import auth
from app.models import User, Event
from app.params import GrpcClientParams

router = APIRouter(prefix="/events", tags=["events"])


class EventResponse(BaseModel):
    """
    Detailed information about an event.

    Attributes
    ----------
    event : Event
        Event object.
    invited_users : List[User]
        List of users who are invited to the event.
    notification_turned_on : bool
        Whether the event is notified turned on.

    """
    event: Event
    invited_users: List[User]
    notification_turned_on: bool


class CreateEventRequest(BaseModel):
    """
    Request to create an event.

    Attributes
    ----------
    title : str
        Title of the event.
    start : datetime
        Start time of the event.
    end : datetime
        End time of the event.
    description : Optional[str]
        Description of the event.
    color : Optional[str]
        Color of the event.
    repeating_delay : Optional[datetime]
        Repeating delay of the event.

    """
    title: str
    start: datetime
    end: datetime
    description: Optional[str]
    color: Optional[str]
    repeating_delay: Optional[datetime]


@router.get("/my/created")
async def get_my_created_events(
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
        page: int,
        items_per_page: int,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
) -> List[Event]:
    """
    Fast api route to get all events created by a user.

    Parameters
    ----------
    user : Annotated[GrpcUser, Security]
        Authenticated user data.
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI
    page : int
        Page number greater than 0.
    items_per_page : int
        Number of items per page. If -1 then all items are returned.
    start : Optional[datetime]
        Start date and time.
    end : Optional[datetime]
        End date and time.

    Returns
    -------
    List[Event]
        List of events created by a user.

    """
    my_events_result: GrpcGetEventsResponse = (
        grpc_clients.event_service_client.request().get_events_by_author_id(
            GrpcGetEventsByAuthorIdRequest(
                author_id=user.id,
                requesting_user=user,
                page_number=page,
                items_per_page=items_per_page,
            )
        )
    )
    return [Event.from_proto(event_proto) for event_proto in my_events_result.events.events]


@router.get("/my/invited")
async def get_my_invited_events(
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
        page: int,
        items_per_page: int,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
) -> List[Event]:
    """
    Fast api route to get all events where user is invited.

    Parameters
    ----------
    user : Annotated[GrpcUser, Security]
        Authenticated user data.
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI
    page : int
        Page number greater than 0.
    items_per_page : int
        Number of items per page. If -1 then all items are returned.
    start : Optional[datetime]
        Start date and time.
    end : Optional[datetime]
        End date and time.

    Returns
    -------
    List[Event]
        List of events where user is invited.

    """
    invite_result: GrpcGetInvitesResponse = (
        grpc_clients.invite_service_client.request().get_invites_by_author_id(
            GrpcGetInvitesByInviteeIdRequest(
                invitee_id=user.id,
                requesting_user=user,
            )
        )
    )

    invited_events_id_list = set(
        item.event_id for item in invite_result.invites.invites
    )

    invited_events_request: GrpcGetEventsResponse = (
        grpc_clients.event_service_client.request().get_events_by_events_ids(
            GrpcGetEventsRequestByEventsIdsRequest(
                events_ids=ListOfEventsIds(ids=invited_events_id_list),
                page_number=page,
                items_per_page=items_per_page // 2 + items_per_page % 2,
            )
        )
    )

    return [Event.from_proto(event) for event in invited_events_request.events.events]


@router.get("/{id}")
async def get_event(
        event_id: str,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> EventResponse:
    """
    Fast api route to get a specific event.

    Parameters
    ----------
    event_id : str
        Event id.
    user : Annotated[GrpcUser, Security]
        Authenticated user data.
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Returns
    -------
    EventResponse
        Event response containing event, all invitees and notification status.

    """
    event_response: GrpcEventResponse = (
        grpc_clients.event_service_client.request().get_event_by_event_id(
            GrpcGetEventByEventIdRequest(
                event_id=event_id,
                requesting_user=user,
            )
        )
    )

    response = EventResponse(
        event=Event.from_proto(event_response.event),
        invited_users=[],
        notification_turned_on=False,
    )

    try:
        invited_people_request: GrpcGetInvitesResponse = (
            grpc_clients.invite_service_client.request().get_invites_by_event_id(
                GrpcInvitesByEventIdRequest(
                    event_id=event_id, invite_status=InviteStatus.ACCEPTED
                )
            )
        )

        invited_people_response: GrpcGetUsersResponse = (
            grpc_clients.identity_service_client.request().get_users_by_id(
                GrpcGetUsersByIdsRequest(
                    page=-1,
                    items_per_page=-1,
                    id=[
                        invite.event_id
                        for invite in invited_people_request.invites.invites
                    ],
                )
            )
        )
        response.invited_users = [
            User.from_proto(person) for person in invited_people_response.users.users
        ]
    except RpcError:
        pass

    # TODO: @Nhsdkk make request to get notification by event_id and author_id
    notification_request: GrpcNotificationResponse = GrpcNotificationResponse()

    response.notification_turned_on = notification_request.notification.enabled

    return response


@router.get("/description/")
async def generate_event_description(
        event_title: str,
        _: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> str:
    """
    Fast api route to generate event description by AI.

    Parameters
    ----------
    event_title : str
        Event title.
    _ : Annotated[GrpcUser, Security]
        Authenticated user data.
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Returns
    -------
    str
        Event description.

    """
    description_response: GrpcGenerateDescriptionResponse = (
        grpc_clients.event_service_client.request().generate_event_description(
            GrpcGenerateDescriptionRequest(event_title=event_title)
        )
    )
    return description_response.event_description


@router.post("/")
def create_event(
        event_data: CreateEventRequest,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    Fast api route to create event.

    Parameters
    ----------
    event_data : CreateEventRequest
        Event data.
    user : Annotated[GrpcUser, Security]
        Authenticated user data.
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    """
    event = Event(
        id="",
        title=event_data.title,
        start=event_data.start,
        end=event_data.end,
        author_id=user.id,
        created_at=datetime.now(),
        deleted_at=None,
        description=event_data.description,
        color=event_data.color,
        repeating_delay=event_data.repeating_delay,
    )
    grpc_clients.event_service_client.request().create_event(
        GrpcEventRequest(event=event.to_proto(), requesting_user=user)
    )


@router.put("/")
def update_event(
        event: Event,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    Fast api route to update event.

    Parameters
    ----------
    event : Event
        Event to update.
    user : Annotated[GrpcUser, Security]
        Authenticated user data.
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Raises
    ------
    PermissionDeniedError
        Permission denied.

    """
    if event.author_id != user.id:
        raise PermissionDeniedError

    event.deleted_at = None

    grpc_clients.event_service_client.request().update_event(
        GrpcEventRequest(event=event.to_proto(), requesting_user=user)
    )


@router.delete("/")
def delete_event(
        event_id: str,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    Fast api route to delete event.

    Parameters
    ----------
    event_id : str
        Event id.
    user : Annotated[GrpcUser, Security]
        Authenticated user data.
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    """
    grpc_clients.event_service_client.request().delete_event(
        GrpcDeleteEventRequest(event_id=event_id, requesting_user=user)
    )

    grpc_clients.notification_service_client.request().delete_notifications_by_event_id(
        GrpcDeleteNotificationsByEventIdRequest(event_id=event_id, requesting_user=user)
    )

    grpc_clients.invite_service_client.request().delete_invites_by_event_id(
        GrpcDeleteInvitesByEventIdRequest(
            event_id=event_id,
        )
    )
