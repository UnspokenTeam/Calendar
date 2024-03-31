"""Event Service Controller."""
import grpc
import prisma.errors

from errors.value_not_found_error import ValueNotFoundError
from proto.event_service_pb2_grpc import EventServiceServicer as GrpcServicer
import proto.event_service_pb2 as proto
from repository.event_repository_interface import EventRepositoryInterface
from src.models.event import Event


class EventServiceImpl(GrpcServicer):
    """
    Implementation of the Event Service.

    Attributes
    ----------
    _event_repository : EventRepositoryInterface

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
    async delete_event(request, context)
        Function that need to be bind to the server that deletes the event.

    """

    _event_repository: EventRepositoryInterface

    def __init__(
        self,
        event_repository: EventRepositoryInterface,
    ):
        self._event_repository = event_repository

    async def get_events_by_author_id(
        self, request: proto.EventsRequestByAuthorId, context: grpc.ServicerContext
    ) -> proto.EventsResponse:
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
        EventsResponse
            Response object for event response.

        """
        try:
            if (
                request.user.type != proto.GrpcUserType.ADMIN
                and request.user.id != request.author_id
            ):
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                return proto.EventsResponse(
                    status_code=403, message="Permission denied"
                )
            events = await self._event_repository.get_events_by_author_id(
                author_id=request.author_id
            )
            context.set_code(grpc.StatusCode.OK)
            return proto.EventsResponse(
                status_code=200,
                events=proto.ListOfEvents(
                    events=[event.to_grpc_event() for event in events]
                ),
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.EventsResponse(status_code=404, message="Events not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.EventsResponse(
                status_code=500, message="Internal server error"
            )

    async def get_event_by_event_id(
        self, request: proto.EventRequestByEventId, context: grpc.ServicerContext
    ) -> proto.EventResponse:
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
        EventResponse
            Response object for event response.

        """
        try:
            event = await self._event_repository.get_event_by_event_id(
                event_id=request.event_id
            )
            if (
                request.user.type != proto.GrpcUserType.ADMIN
                and request.user.id != event.author_id
            ):
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                return proto.EventResponse(status_code=403, message="Permission denied")
            context.set_code(grpc.StatusCode.OK)
            return proto.EventResponse(status_code=200, event=event.to_grpc_event())
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.EventResponse(status_code=404, message="Events not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.EventResponse(status_code=500, message="Internal server error")

    async def get_events_by_events_ids(
        self, request: proto.EventsRequestByEventsIds, context: grpc.ServicerContext
    ) -> proto.EventsResponse:
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
        EventsResponse
            Response object for event response.

        """
        try:
            events = await self._event_repository.get_events_by_events_ids(
                events_ids=list(request.events_ids.ids)
            )
            if request.user.type == proto.GrpcUserType.ADMIN:
                context.set_code(grpc.StatusCode.OK)
                return proto.EventsResponse(
                    status_code=200,
                    events=proto.ListOfEvents(
                        events=[event.to_grpc_event() for event in events]
                    ),
                )
            accessible_events = [
                event for event in events if request.user.id == event.author_id
            ]
            if accessible_events is None or len(accessible_events) == 0:
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                return proto.EventsResponse(
                    status_code=403, message="Permission denied"
                )
            context.set_code(grpc.StatusCode.OK)
            return proto.EventsResponse(
                status_code=200,
                events=proto.ListOfEvents(
                    events=[event.to_grpc_event() for event in accessible_events]
                ),
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.EventsResponse(status_code=404, message="Events not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.EventsResponse(
                status_code=500, message="Internal server error"
            )

    async def get_all_events(
        self, request: proto.RequestingUser, context: grpc.ServicerContext
    ) -> proto.EventsResponse:
        """
        Get all events.

        Parameters
        ----------
        request : Empty
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        EventsResponse
            Response object for event response.

        """
        try:
            if request.user.type != proto.GrpcUserType.ADMIN:
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                return proto.EventsResponse(
                    status_code=403, message="Permission denied"
                )
            events = await self._event_repository.get_all_events()
            context.set_code(grpc.StatusCode.OK)
            return proto.EventsResponse(
                status_code=200,
                events=proto.ListOfEvents(
                    events=[event.to_grpc_event() for event in events]
                ),
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.EventsResponse(status_code=404, message="Events not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.EventsResponse(
                status_code=500, message="Internal server error"
            )

    async def create_event(
        self, request: proto.GrpcEvent, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Create event.

        Parameters
        ----------
        request : proto.GrpcEvent
            Request data containing GrpcEvent.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        BaseResponse
            Object containing status code and message if the response status is not 200.

        """
        try:
            event = Event.from_grpc_event(request)
            await self._event_repository.create_event(event=event)
            context.set_code(grpc.StatusCode.OK)
            return proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.BaseResponse(status_code=404, message="Event not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")

    async def update_event(
        self, request: proto.UpdateEventRequest, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Update event.

        Parameters
        ----------
        request : proto.GrpcEvent
            Request data containing GrpcEvent.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        BaseResponse
            Object containing status code and message if the response status is not 200.

        """
        try:
            if (
                request.user.type != proto.GrpcUserType.ADMIN
                and request.user.id != request.event.author_id
            ):
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                return proto.BaseResponse(status_code=403, message="Permission denied")
            event = Event.from_grpc_event(request.event)
            await self._event_repository.update_event(event=event)
            context.set_code(grpc.StatusCode.OK)
            return proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.BaseResponse(status_code=404, message="Event not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")

    async def delete_event(
        self, request: proto.DeleteEventRequest, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Delete event.

        Parameters
        ----------
        request : proto.DeleteEventRequest
            Request data containing event ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        BaseResponse
            Object containing status code and message if the response status is not 200.

        """
        try:
            event = await self._event_repository.get_event_by_event_id(request.event_id)
            if (
                request.user.type != proto.GrpcUserType.ADMIN
                and request.user.id != event.author_id
            ):
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                return proto.BaseResponse(status_code=403, message="Permission denied")
            await self._event_repository.delete_event(event_id=request.event_id)
            context.set_code(grpc.StatusCode.OK)
            return proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return proto.BaseResponse(status_code=404, message="Event not found")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return proto.BaseResponse(status_code=500, message="Internal server error")
