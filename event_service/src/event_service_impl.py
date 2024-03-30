"""Event Service Controller."""
import grpc

from proto.event_service_pb2_grpc import EventServiceServicer as GrpcServicer
import proto.event_service_pb2 as proto

from repository.event_repository_interface import EventRepositoryInterface


class EventServiceImpl(GrpcServicer):
    """
    Implementation of the Event Service.

    Attributes
    ----------
    _event_repository : EventRepositoryInterface

    Methods
    -------
    get_events(request, context)
        Function that need to be bind to the server that returns events list.
    create_event(request, context)
        Function that need to be bind to the server that creates the event.
    update_event(request, context)
        Function that need to be bind to the server that updates the event.
    delete_event(request, context)
        Function that need to be bind to the server that deletes the event.

    """

    _event_repository: EventRepositoryInterface

    def __init__(
        self,
        event_repository: EventRepositoryInterface,
    ) -> None:
        self._event_repository = event_repository

    def get_events(
        self, request: proto.EventsRequest, context: grpc.ServicerContext
    ) -> proto.EventsResponse:
        """
        Get all events.

        Parameters
        ----------
        request : proto.EventsRequest
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.EventsResponse
            Response object for event response.

        """
        pass

    def create_event(
        self, request: proto.Event, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Create event.

        Parameters
        ----------
        request : proto.Event
            Request data containing GrpcEvent.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.BaseResponse
            Object containing status code and message if the response status is not 200.

        """
        pass

    def update_event(
        self, request: proto.Event, context: grpc.ServicerContext
    ) -> proto.BaseResponse:
        """
        Update event.

        Parameters
        ----------
        request : proto.Event
            Request data containing GrpcEvent.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.BaseResponse
            Object containing status code and message if the response status is not 200.

        """
        pass

    def delete_event(
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
        proto.BaseResponse
            Object containing status code and message if the response status is not 200.

        """
        pass
