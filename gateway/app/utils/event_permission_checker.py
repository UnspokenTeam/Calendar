"""Event permission checker."""
from typing import Annotated
from uuid import UUID

from errors import PermissionDeniedError
from grpc import RpcError
from pydantic import AfterValidator, UUID4

from app.generated.event_service.event_service_pb2 import (
    EventRequestByEventId as GrpcGetEventByEventIdRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    InviteStatus as GrpcInviteStatus,
)
from app.generated.invite_service.invite_service_pb2 import (
    GetInvitesByInviteeIdRequest as GrpcGetInvitesByInviteeIdRequest
)
from app.generated.event_service.event_service_pb2 import GrpcEvent
from app.generated.event_service.event_service_pb2 import ListOfEventsIds as GrpcListOfEventsIds
from app.generated.event_service.event_service_pb2 import EventsRequestByEventsIds as GrpcEventsByEventsIdsRequest
from app.generated.event_service.event_service_pb2 import ListOfEvents as GrpcListOfEvents
from app.generated.invite_service.invite_service_pb2 import InvitesResponse as GrpcInvitesResponse
from app.generated.user.user_pb2 import GrpcUser
from app.models import Event
from app.params import GrpcClientParams


def check_permission_for_event(
        grpc_user: GrpcUser,
        event_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
        grpc_clients: GrpcClientParams
) -> Event:
    """
    Check if user can access event.

    Parameters
    ----------
    grpc_user : GrpcUser
        User's data
    event_id : UUID4 | str
        Event id
    grpc_clients: GrpcClientParams
        Grpc clients

    Raises
    ------
    PermissionDeniedError
        Permission denied

    Returns
    -------
    Event
        Event data

    """
    try:
        event: GrpcEvent = grpc_clients.event_service_client.request().get_event_by_event_id(
            GrpcGetEventByEventIdRequest(
                event_id=str(event_id),
                requesting_user=grpc_user
            )
        )
        return Event.from_proto(event)
    except RpcError:
        invites: GrpcInvitesResponse = grpc_clients.invite_service_client.request().get_invites_by_invitee_id(
            GrpcGetInvitesByInviteeIdRequest(
                invitee_id=grpc_user.id,
                invite_status=GrpcInviteStatus.ACCEPTED,
                requesting_user=grpc_user,
                page_number=1,
                items_per_page=-1
            )
        )

        if (
                len(invites.invites.invites) == 0 or
                not any([invite.event_id == event_id for invite in invites.invites.invites])
        ):
            raise PermissionDeniedError("Permission denied")

        events_request: GrpcListOfEvents = grpc_clients.event_service_client.request().get_events_by_events_ids(
            GrpcEventsByEventsIdsRequest(
                events_ids=GrpcListOfEventsIds(ids=[event_id]),
                page_number=1,
                items_per_page=-1
            )
        )

        if len(events_request.events) != 1:
            raise ValueError("No notifications found")

        return Event.from_proto(events_request.events[0])
