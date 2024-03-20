from proto.event_service_pb2_grpc import EventServiceServicer as GrpcServicer
from proto.event_service_pb2 import EventsRequest, EventsResponse, ListOfEvents, Event as GrpcEvent, StandardResponse, DeleteEventRequest
from src.models.event import Event
from datetime import datetime


class EventServiceImpl(GrpcServicer):
    def __init__(self):
        self.events = [
            Event(
                id="1",
                title="Sample Event",
                description="This is a sample event.",
                color="blue",
                start=datetime(2024, 3, 19, 10, 0),  # Example start time
                end=datetime(2024, 3, 19, 12, 0),  # Example end time
                repeating_delay=datetime(
                    2024, 3, 19, 12, 0
                ),  # Assuming no repeating delay
                author_id="123",  # Example author ID
            ),
            Event(
                id="2",
                title="Sample Event",
                description="This is a sample event.",
                color="blue",
                start=datetime(2024, 3, 19, 10, 0),  # Example start time
                end=datetime(2024, 3, 19, 12, 0),  # Example end time
                repeating_delay=datetime(
                    2024, 3, 19, 12, 0
                ),  # Assuming no repeating delay
                author_id="123",  # Example author ID
            ),
        ]

    def get_events(self, request: EventsRequest, context) -> EventsResponse:
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

    def create_event(self, request: GrpcEvent, context) -> StandardResponse:
        pass

    def update_event(self, request: GrpcEvent, context) -> StandardResponse:
        pass

    def delete_event(self, request: DeleteEventRequest, context) -> StandardResponse:
        pass
