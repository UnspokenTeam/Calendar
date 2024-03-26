"""Event Service Controller."""
from datetime import datetime

import grpc

from proto.event_service_pb2_grpc import EventServiceServicer as GrpcServicer
import proto.event_service_pb2 as proto
from src.models.event import Event


class EventServiceImpl(GrpcServicer):
    """
    Implementation of the Event Service.

    Attributes
    ----------
    events : List[Event]
        List of events.

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

    def __init__(self) -> None:
        self.events = [
            Event(
                id="1",
                title="Sample Event",
                description="This is a sample event.",
                color="blue",
                start=datetime(2024, 3, 19, 10, 0),
                end=datetime(2024, 3, 19, 12, 0),
                repeating_delay=datetime(2024, 3, 19, 12, 0),
                author_id="123",
            ),
            Event(
                id="2",
                title="Sample Event",
                description="This is a sample event.",
                color="blue",
                start=datetime(2024, 3, 19, 10, 0),
                end=datetime(2024, 3, 19, 12, 0),
                repeating_delay=datetime(2024, 3, 19, 12, 0),
                author_id="123",
            ),
        ]

    def get_events(
        self, request: proto.EventsRequest, context: grpc.ServicerContext
    ) -> proto.EventsResponse:
        """
        Get all events.

        Parameters
        ----------
        request : proto.EventsRequestConfiguration Editor
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.EventsResponse
            Response object for event response.

        """
        if request.offset == -1:
            return proto.EventsResponse(
                status=400,
            )

        return proto.EventsResponse(
            status=200,
            events=proto.ListOfEvents(
                events=[event.to_grpc_event() for event in self.events]
            ),
        )

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
