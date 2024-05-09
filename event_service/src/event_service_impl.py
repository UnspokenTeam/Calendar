"""Event Service Controller."""
from datetime import datetime

import grpc

from src.models.event import Event
from utilities.ai_client import AIClient

from errors_package.errors import PermissionDeniedError
from generated.event_service.event_service_pb2_grpc import (
    EventServiceServicer as GrpcServicer,
)
from generated.user.user_pb2 import GrpcUserType
from google.protobuf.empty_pb2 import Empty
from repository.event_repository_interface import EventRepositoryInterface
import generated.event_service.event_service_pb2 as proto


class EventServiceImpl(GrpcServicer):
    """
    Implementation of the Event Service.

    Attributes
    ----------
    _event_repository : EventRepositoryInterface
        The event repository interface attribute.

    Methods
    -------
    async get_events_by_author_id(request, context)
        Function that need to be bind to the server that returns events list.
    async get_event_by_event_id(request, context)
        Function that need to be bind to the server that returns event.
    async get_events_by_events_ids(request, context)
        Function that need to be bind to the server that returns events list.
    async get_all_events(request, context)
        Function that need to be bind to the server that returns all events in list.
    async create_event(request, context)
        Function that need to be bind to the server that creates the event.
    async update_event(request, context)
        Function that need to be bind to the server that updates the event.
    async delete_event_by_id(request, context)
        Function that need to be bind to the server that deletes the event that matches id.
    async delete_events_by_author_id(request, context)
        Function that need to be bind to the server that deletes events that match id.
    async generate_event_description(request, context)
        Function that need to be bind to the server that creates the event description.

    """

    _event_repository: EventRepositoryInterface

    def __init__(
        self,
        event_repository: EventRepositoryInterface,
    ) -> None:
        self._event_repository = event_repository

    async def get_events_by_author_id(
        self, request: proto.EventsRequestByAuthorId, context: grpc.ServicerContext
    ) -> proto.ListOfEvents:
        """
        Get events by author id.

        Parameters
        ----------
        request : proto.EventsRequestByAuthorId
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.ListOfEvents
            Response object for several events.

        """
        events = await self._event_repository.get_events_by_author_id(
            author_id=request.author_id,
            page_number=request.page_number,
            items_per_page=request.items_per_page,
            start=datetime.utcfromtimestamp(
                request.start.seconds + request.start.nanos / 1e9
            )
            if request.WhichOneof("optional_start") is not None
            else None,
            end=datetime.utcfromtimestamp(request.end.seconds + request.end.nanos / 1e9)
            if request.WhichOneof("optional_end") is not None
            else None,
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfEvents(events=[event.to_grpc_event() for event in events])

    async def get_event_by_event_id(
        self, request: proto.EventRequestByEventId, context: grpc.ServicerContext
    ) -> proto.GrpcEvent:
        """
        Get event by event id.

        Parameters
        ----------
        request : proto.EventRequestByEventId
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.GrpcEvent
            Response object for event.

        """
        event = await self._event_repository.get_event_by_event_id(
            event_id=request.event_id
        )
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != event.author_id
        ):
            raise PermissionDeniedError("Permission denied.")
        context.set_code(grpc.StatusCode.OK)
        return event.to_grpc_event()

    async def get_events_by_events_ids(
        self, request: proto.EventsRequestByEventsIds, context: grpc.ServicerContext
    ) -> proto.ListOfEvents:
        """
        Get events by events ids.

        Parameters
        ----------
        request : proto.EventsRequestByEventsIds
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.ListOfEvents
            Response object for several events.

        """
        events = await self._event_repository.get_events_by_events_ids(
            events_ids=list(request.events_ids.ids),
            page_number=request.page_number,
            items_per_page=request.items_per_page,
            start=datetime.utcfromtimestamp(
                request.start.seconds + request.start.nanos / 1e9
            )
            if request.WhichOneof("optional_start") is not None
            else None,
            end=datetime.utcfromtimestamp(request.end.seconds + request.end.nanos / 1e9)
            if request.WhichOneof("optional_end") is not None
            else None,
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfEvents(events=[event.to_grpc_event() for event in events])

    async def get_all_events(
        self, request: proto.GetAllEventsRequest, context: grpc.ServicerContext
    ) -> proto.ListOfEvents:
        """
        Get all events.

        Parameters
        ----------
        request : proto.RequestingUser
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.ListOfEvents
            Response object for several events.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if request.requesting_user.type != GrpcUserType.ADMIN:
            raise PermissionDeniedError("Permission denied")
        events = await self._event_repository.get_all_events(
            page_number=request.page_number,
            items_per_page=request.items_per_page,
            start=datetime.utcfromtimestamp(
                request.start.seconds + request.start.nanos / 1e9
            )
            if request.WhichOneof("optional_start") is not None
            else None,
            end=datetime.utcfromtimestamp(request.end.seconds + request.end.nanos / 1e9)
            if request.WhichOneof("optional_end") is not None
            else None,
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfEvents(events=[event.to_grpc_event() for event in events])

    async def create_event(
        self, request: proto.EventRequest, context: grpc.ServicerContext
    ) -> proto.GrpcEvent:
        """
        Create event.

        Parameters
        ----------
        request : proto.EventRequest
            Request data containing GrpcEvent.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.GrpcEvent
            Response object for event.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        event = Event.from_grpc_event(request.event)
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != event.author_id
        ):
            raise PermissionDeniedError("Permission denied")
        event = await self._event_repository.create_event(event=event)
        context.set_code(grpc.StatusCode.OK)
        return event.to_grpc_event()

    async def update_event(
        self, request: proto.EventRequest, context: grpc.ServicerContext
    ) -> proto.GrpcEvent:
        """
        Update event.

        Parameters
        ----------
        request : proto.EventRequest
            Request data containing GrpcEvent.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.GrpcEvent
            Response object for event.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != request.event.author_id
        ):
            raise PermissionDeniedError("Permission denied")
        event = Event.from_grpc_event(request.event)
        event = await self._event_repository.update_event(event=event)
        context.set_code(grpc.StatusCode.OK)
        return event.to_grpc_event()

    async def delete_event_by_id(
        self, request: proto.DeleteEventByIdRequest, context: grpc.ServicerContext
    ) -> Empty:
        """
        Delete event.

        Parameters
        ----------
        request : proto.DeleteEventByIdRequest
            Request data containing event ID.
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
        event = await self._event_repository.get_event_by_event_id(request.event_id)
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != event.author_id
        ):
            raise PermissionDeniedError("Permission denied")
        await self._event_repository.delete_event_by_id(event_id=request.event_id)
        context.set_code(grpc.StatusCode.OK)
        return Empty()

    async def delete_events_by_author_id(
        self,
        request: proto.DeleteEventsByAuthorIdRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        """
        Delete events by author id.

        Parameters
        ----------
        request : proto.DeleteEventByAuthorIdRequest
            Request data containing author ID.
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
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != request.author_id
        ):
            raise PermissionDeniedError("Permission denied")
        await self._event_repository.delete_events_by_author_id(
            author_id=request.author_id
        )
        context.set_code(grpc.StatusCode.OK)
        return Empty()

    async def generate_event_description(
        self, request: proto.GenerateDescriptionRequest, context: grpc.ServicerContext
    ) -> proto.GenerateDescriptionResponse:
        """
        Generate event description.

        Parameters
        ----------
        request : proto.GenerateDescriptionRequest
            Request event description by event title from AI Client.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.GenerateDescriptionResponse
            Response object for generate description request.

        """
        event_description = await AIClient.generate_event_description(
            request.event_title
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.GenerateDescriptionResponse(
            event_description=event_description,
        )
