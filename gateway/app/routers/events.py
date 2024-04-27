from datetime import datetime
from typing import Annotated, List, Optional

from fastapi import APIRouter, Security, Depends
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
)
from app.generated.notification_service.notification_service_pb2 import (
    DeleteNotificationsByEventIdRequest as GrpcDeleteNotificationsByEventIdRequest,
)
from app.generated.notification_service.notification_service_pb2 import (
    NotificationResponse as GrpcNotificationResponse
)
from app.generated.user.user_pb2 import GrpcUser
from app.middleware import auth
from app.models import User, UserType, Event
from app.params import GrpcClientParams

router = APIRouter(prefix="/events", tags=["events"])


class EventResponse(BaseModel):
    event: Event
    invited_users: List[User]
    notification_turned_on: bool


@router.get("/my")
async def get_my_events(
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
        page: int,
        items_per_page: int,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
) -> List[Event]:
    my_events_result: GrpcGetEventsResponse = grpc_clients.event_service_client.request().get_events_by_author_id(
        GrpcGetEventsByAuthorIdRequest(
            author_id=user.id,
            requesting_user=user,
            page_number=page,
            items_per_page=items_per_page // 2,
        )
    )

    invite_result: GrpcGetInvitesResponse = grpc_clients.invite_service_client.request().get_invites_by_author_id(
        GrpcGetInvitesByInviteeIdRequest(
            invitee_id=user.id,
            requesting_user=user,
        )
    )

    invited_events_id_list = set(item.event_id for item in invite_result.invites.invites)

    invited_events_request: GrpcGetEventsResponse = grpc_clients.event_service_client.request().get_events_by_events_ids(
        GrpcGetEventsRequestByEventsIdsRequest(
            events_ids=ListOfEventsIds(
                ids=invited_events_id_list
            ),
            page_number=page,
            items_per_page=items_per_page // 2 + items_per_page % 2
        )
    )

    return (
            [Event.from_proto(event) for event in my_events_result.events.events] +
            [Event.from_proto(event) for event in invited_events_request.events.events]
    )


@router.get("/{id}")
async def get_event(
        event_id: str,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> EventResponse:
    event_response: GrpcEventResponse = grpc_clients.event_service_client.request().get_event_by_event_id(
        GrpcGetEventByEventIdRequest(
            event_id=event_id,
            requesting_user=user,
        )
    )

    response = EventResponse(
        event=Event.from_proto(event_response.event),
        invited_users=[],
        notification_turned_on=False
    )

    # TODO: @Nhsdkk make request to get all invites by event_id
    invited_people_request: GrpcGetInvitesResponse = GrpcGetInvitesResponse()

    if len(invited_people_request.invites.invites) != 0:
        invited_people_response: GrpcGetUsersResponse = grpc_clients.identity_service_client.request().get_users_by_id(
            GrpcGetUsersByIdsRequest(
                page=-1,
                items_per_page=-1,
                id=[invite.event_id for invite in invited_people_request.invites.invites],
            )
        )
        response.invited_users = [User.from_proto(person) for person in invited_people_response.users.users]

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
    description_response: GrpcGenerateDescriptionResponse = grpc_clients.event_service_client.request().generate_event_description(
        GrpcGenerateDescriptionRequest(
            event_title=event_title
        )
    )
    return description_response.event_description


@router.post("/")
def create_event(
        event: Event,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    if event.author_id != user.id and user.id != UserType.ADMIN:
        raise PermissionDeniedError

    grpc_clients.event_service_client.request().create_event(
        GrpcEventRequest(
            event=event.to_proto(),
            requesting_user=user
        )
    )


@router.put("/")
def update_event(
        event: Event,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    if event.author_id != user.id and user.id != UserType.ADMIN:
        raise PermissionDeniedError

    grpc_clients.event_service_client.request().update_event(
        GrpcEventRequest(
            event=event.to_proto(),
            requesting_user=user
        )
    )


@router.delete("/")
def delete_event(
        event_id: str,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    grpc_clients.event_service_client.request().delete_event(
        GrpcDeleteEventRequest(
            event_id=event_id,
            requesting_user=user
        )
    )

    grpc_clients.notification_service_client.request().delete_notifications_by_event_id(
        GrpcDeleteNotificationsByEventIdRequest(
            event_id=event_id,
            requesting_user=user
        )
    )

    grpc_clients.invite_service_client.request().delete_invites_by_event_id(
        GrpcDeleteInvitesByEventIdRequest(
            event_id=event_id,
        )
    )
