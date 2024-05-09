"""Event routes"""
from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID, uuid4

from grpc import RpcError

from app.errors import PermissionDeniedError
from app.generated.event_service.event_service_pb2 import DeleteEventByIdRequest as GrpcDeleteEventByIdRequest
from app.generated.event_service.event_service_pb2 import EventRequest as GrpcEventRequest
from app.generated.event_service.event_service_pb2 import EventRequestByEventId as GrpcGetEventByEventIdRequest
from app.generated.event_service.event_service_pb2 import EventsRequestByAuthorId as GrpcGetEventsByAuthorIdRequest
from app.generated.event_service.event_service_pb2 import (
    EventsRequestByEventsIds as GrpcGetEventsRequestByEventsIdsRequest,
)
from app.generated.event_service.event_service_pb2 import GenerateDescriptionRequest as GrpcGenerateDescriptionRequest
from app.generated.event_service.event_service_pb2 import (
    GenerateDescriptionResponse as GrpcGenerateDescriptionResponse,
)
from app.generated.event_service.event_service_pb2 import GetAllEventsRequest as GrpcGetAllEventsRequest
from app.generated.event_service.event_service_pb2 import GrpcEvent, ListOfEventsIds
from app.generated.event_service.event_service_pb2 import ListOfEvents as GrpcListOfEvents
from app.generated.identity_service.get_user_pb2 import ListOfUser as GrpcListOfUsers
from app.generated.identity_service.get_user_pb2 import UsersByIdRequest as GrpcGetUsersByIdsRequest
from app.generated.invite_service.invite_service_pb2 import (
    DeleteInvitesByEventIdRequest as GrpcDeleteInvitesByEventIdRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    GetInvitesByInviteeIdRequest as GrpcGetInvitesByInviteeIdRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    InvitesByEventIdRequest as GrpcInvitesByEventIdRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    InvitesResponse as GrpcGetInvitesResponse,
)
from app.generated.invite_service.invite_service_pb2 import (
    InviteStatus as GrpcInviteStatus,
)
from app.generated.notification_service.notification_service_pb2 import (
    DeleteNotificationsByEventIdRequest as GrpcDeleteNotificationsByEventIdRequest,
)
from app.generated.notification_service.notification_service_pb2 import (
    GrpcNotification,
)
from app.generated.notification_service.notification_service_pb2 import (
    NotificationRequestByEventAndAuthorIds as GrpcGetNotificationByEventAndAuthorIdsRequest,
)
from app.generated.user.user_pb2 import GrpcUser, GrpcUserType
from app.middleware import auth
from app.models import Event, User
from app.models.event import Interval
from app.params import GrpcClientParams

from fastapi import APIRouter, Depends
from pydantic import UUID4, AfterValidator, BaseModel, Field
from pytz import utc

router = APIRouter(prefix="/events", tags=["events"])


class EventResponse(BaseModel):
    """
    Event response with generated classname

    Attributes
    ----------
    event : Event
        Event data
    classname : str
        Generated widget classname

    """

    event: Event
    classname: str


class DetailedEventResponse(BaseModel):
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
    repeating_delay: Optional[Interval] = None


@router.get("/my/created")
async def get_my_created_events(
        page: Annotated[int, Field(1, ge=1)],
        items_per_page: Annotated[int, Field(-1, ge=-1)],
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
) -> List[EventResponse]:
    """
    \f

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
    List[EventResponse]
        List of events created by a user.

    """
    request_data = GrpcGetEventsByAuthorIdRequest(
        author_id=user.id,
        requesting_user=user,
        page_number=page,
        items_per_page=items_per_page,
    )

    if start is not None:
        request_data.start.FromDatetime(start.astimezone(utc))
    if end is not None:
        request_data.end.FromDatetime(end.astimezone(utc))

    my_events_result: GrpcListOfEvents = (
        grpc_clients.event_service_client.request().get_events_by_author_id(
            request_data
        )
    )

    events = [Event.from_proto(event_proto) for event_proto in my_events_result.events]

    return [EventResponse(event=event, classname=generate_classname(event.color)) for event in events]


@router.get("/my/invited/")
async def get_my_invited_events(
        page: Annotated[int, Field(1, ge=1)],
        items_per_page: Annotated[int, Field(-1, ge=-1)],
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
) -> List[EventResponse]:
    """
    \f

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
    List[EventResponse]
        List of events where user is invited.

    """
    invite_result: GrpcGetInvitesResponse = (
        grpc_clients.invite_service_client.request().get_invites_by_invitee_id(
            GrpcGetInvitesByInviteeIdRequest(
                invitee_id=user.id,
                requesting_user=user,
                page_number=1,
                items_per_page=-1,
                invite_status=GrpcInviteStatus.ACCEPTED,
            )
        )
    )

    invited_events_id_list = list(
        item.event_id for item in invite_result.invites.invites
    )

    if len(invited_events_id_list) == 0:
        return []

    events_request = GrpcGetEventsRequestByEventsIdsRequest(
        events_ids=ListOfEventsIds(ids=invited_events_id_list),
        page_number=page,
        items_per_page=items_per_page,
    )

    if start is not None:
        events_request.start.FromDatetime(start.astimezone(utc))

    if end is not None:
        events_request.end.FromDatetime(end.astimezone(utc))

    invited_events_request: GrpcListOfEvents = (
        grpc_clients.event_service_client.request().get_events_by_events_ids(
            events_request
        )
    )

    events = [Event.from_proto(event_proto) for event_proto in invited_events_request.events]

    return [EventResponse(event=event, classname=generate_classname(event.color)) for event in events]


@router.get("/{event_id}")
async def get_event(
        event_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> DetailedEventResponse:
    """
    \f

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
    DetailedEventResponse
        Event response containing event, all invitees and notification status.

    """
    event_response: GrpcEvent = (
        grpc_clients.event_service_client.request().get_event_by_event_id(
            GrpcGetEventByEventIdRequest(
                event_id=str(event_id),
                requesting_user=user,
            )
        )
    )

    response = DetailedEventResponse(
        event=Event.from_proto(event_response),
        invited_users=[],
        notification_turned_on=False,
    )

    invited_people_request: GrpcGetInvitesResponse = (
        grpc_clients.invite_service_client.request().get_invites_by_event_id(
            GrpcInvitesByEventIdRequest(
                event_id=str(event_id),
                invite_status=GrpcInviteStatus.ACCEPTED
            )
        )
    )

    invited_people_ids = [
        invite.event_id
        for invite in invited_people_request.invites.invites
    ]

    if len(invited_people_ids) != 0:
        invited_people_response: GrpcListOfUsers = (
            grpc_clients.identity_service_client.request().get_users_by_id(
                GrpcGetUsersByIdsRequest(
                    page=-1,
                    items_per_page=-1,
                    id=invited_people_ids,
                )
            )
        )

        response.invited_users = [
            User.from_proto(person) for person in invited_people_response.users
        ]

    notification_request: GrpcNotification = (
        grpc_clients.notification_service_client.request().get_notification_by_event_and_author_ids(
            GrpcGetNotificationByEventAndAuthorIdsRequest(
                event_id=str(event_id),
                author_id=user.id,
                requesting_user=user
            )
        )
    )

    response.notification_turned_on = notification_request.enabled

    return response


@router.get("/all/")
async def get_all_events(
        page: Annotated[int, Field(1, ge=1)],
        items_per_page: Annotated[int, Field(-1, ge=-1)],
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
) -> List[EventResponse]:
    """
    \f

    Get all events

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

    Raises
    ------
    PermissionDeniedError
        Permission denied

    Returns
    -------
    List[EventResponse]
        List of all events.

    """
    if user.type != GrpcUserType.ADMIN:
        raise PermissionDeniedError("Permission denied")

    events_request = GrpcGetAllEventsRequest(
        requesting_user=user,
        page_number=page,
        items_per_page=items_per_page,
    )

    if start is not None:
        events_request.start.FromDatetime(start.astimezone(utc))
    if end is not None:
        events_request.end.FromDatetime(end.astimezone(utc))

    events_response: GrpcListOfEvents = grpc_clients.event_service_client.request().get_all_events(
        events_request
    )

    events = [Event.from_proto(event_proto) for event_proto in events_response.events]

    return [EventResponse(event=event, classname=generate_classname(event.color)) for event in events]


@router.get("/description/")
async def generate_event_description(
        event_title: str,
        _: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> str:
    """
    \f

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
    return str(description_response.event_description)


@router.post("/")
async def create_event(
        event_data: CreateEventRequest,
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> EventResponse:
    """
    \f

    Fast api route to create event.

    Parameters
    ----------
    event_data : CreateEventRequest
        Event data.
    user : Annotated[GrpcUser, Security]
        Authenticated user data.
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Returns
    -------
    EventResponse
        Created event object.

    """
    event = Event(
        id=uuid4(),
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

    proto_event: GrpcEvent = grpc_clients.event_service_client.request().create_event(
        GrpcEventRequest(event=event.to_proto(), requesting_user=user)
    )

    event = Event.from_proto(proto_event)

    return EventResponse(event=event, classname=generate_classname(event.color))


@router.put("/")
async def update_event(
        event: Event,
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> EventResponse:
    """
    \f

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

    Returns
    -------
    EventResponse
        Updated event object.

    """
    if str(event.author_id) != user.id:
        raise PermissionDeniedError("Permission denied")

    db_event_response: GrpcEvent = grpc_clients.event_service_client.request().get_event_by_event_id(
        GrpcGetEventByEventIdRequest(
            event_id=str(event.id),
            requesting_user=user,
        )
    )
    db_event = Event.from_proto(db_event_response)

    event.deleted_at = None
    event.created_at = db_event.created_at

    event_proto: GrpcEvent = grpc_clients.event_service_client.request().update_event(
        GrpcEventRequest(event=event.to_proto(), requesting_user=user)
    )

    event = Event.from_proto(event_proto)

    return EventResponse(event=event, classname=generate_classname(event.color))


@router.put("/admin/")
async def update_event_as_admin(
        event: Event,
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> EventResponse:
    """
    \f

    Update event as admin

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
        Permission denied

    Returns
    -------
    EventResponse
        Updated event object.

    """
    if user.type != GrpcUserType.ADMIN:
        raise PermissionDeniedError("Permission denied")

    event_proto: GrpcEvent = grpc_clients.event_service_client.request().update_event(
        GrpcEventRequest(event=event.to_proto(), requesting_user=user)
    )
    event = Event.from_proto(event_proto)

    return EventResponse(event=event, classname=generate_classname(event.color))


@router.delete("/")
async def delete_event(
        event_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f

    Fast api route to delete event.

    Parameters
    ----------
    event_id : UUID4 | str
        Event id.
    user : Annotated[GrpcUser, Security]
        Authenticated user data.
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    """
    try:
        grpc_clients.notification_service_client.request().delete_notifications_by_event_id(
            GrpcDeleteNotificationsByEventIdRequest(event_id=str(event_id), requesting_user=user)
        )
    except RpcError:
        pass

    try:
        grpc_clients.invite_service_client.request().delete_invites_by_event_id(
            GrpcDeleteInvitesByEventIdRequest(
                event_id=str(event_id),
            )
        )
    except RpcError:
        pass

    grpc_clients.event_service_client.request().delete_event_by_id(
        GrpcDeleteEventByIdRequest(event_id=str(event_id), requesting_user=user)
    )


def generate_classname(color: Optional[str]) -> str:
    """
    Generate class name from color.

    Parameters
    ----------
    color : Optional[str]
        Color name.

    Returns
    -------
    str
        Class name.

    """
    color = color if color is not None else "RED"
    return f"!bg-{color}-100/50 !border-l-4 !border-r-0 !border-y-0 !border-{color}-500 !text-{color}-500 text-xl"
