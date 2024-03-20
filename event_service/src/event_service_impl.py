"""Event Service Controller"""
from proto.event_service_pb2_grpc import EventServiceServicer as GrpcServicer
from proto.event_service_pb2 import (
    EventsRequest,
    EventsResponse,
    ListOfEvents,
    Event as GrpcEvent,
    BaseResponse,
    DeleteEventRequest,
)
from src.models.event import Event
from datetime import datetime


class EventServiceImpl(GrpcServicer):
    """
    Implementation of the Event Service.

    Attributes
    ----------
    events : List[Event]
        List of events

    Methods
    -------
    get_events()
        Function that need to be bind to the server that returns events list.
    create_event()
        Function that need to be bind to the server that creates the event.
    update_event()
        Function that need to be bind to the server that updates the event.
    delete_event()
        Function that need to be bind to the server that deletes the event.
    """

    def __init__(self):
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

    def get_events(self, request: EventsRequest, context) -> EventsResponse:
        """
        Get all events.

        Parameters
        ----------
        request : EventsRequest
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        EventsResponse
            Response object for event response.
        """
        if request.offset == -1:
            return EventsResponse(
                status=400,
            )

        return EventsResponse(
            status=200,
            events=ListOfEvents(
                events=[event.to_grpc_event() for event in self.events]
            ),
        )

    def create_event(self, request: GrpcEvent, context) -> BaseResponse:
        """
        Create event.

        Parameters
        ----------
        request : GrpcEvent
            Request data containing GrpcEvent.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        BaseResponse
            Object containing status code and message if the response status is not 200.
        """
        pass

    def update_event(self, request: GrpcEvent, context) -> BaseResponse:
        """
        Update event.

        Parameters
        ----------
        request : GrpcEvent
            Request data containing GrpcEvent.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        BaseResponse
            Object containing status code and message if the response status is not 200.
        """
        pass

    def delete_event(self, request: DeleteEventRequest, context) -> BaseResponse:
        """
        Delete event.

        Parameters
        ----------
        request : DeleteEventRequest
            Request data containing event ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        BaseResponse
            Object containing status code and message if the response status is not 200.
        """
        pass
