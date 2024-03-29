"""Mock event repository"""
from typing import List
from uuid import uuid4

from errors.value_not_found_error import ValueNotFoundError
from proto.event_service_pb2 import ListOfEventsIds
from repository.event_repository_interface import EventRepositoryInterface
from src.models.event import Event


class MockEventRepositoryImpl(EventRepositoryInterface):
    """
    Mock class for manipulating with event data

    Attributes
    ----------
    _events: List[Event]
        List of events

    Methods
    -------
    async get_events_by_author_id(author_id)
        Returns events that has matches with given author id.
    async get_event_by_event_id(event_id)
        Returns event that has matches with given event id.
    async get_events_by_events_ids(events_ids)
        Returns events that has matches with given list of event ids.
    async create_event(event)
        Creates new event inside db or throws an exception.
    async update_event(event)
        Updates event that has the same id as provided event object inside db or throws an exception.
    async delete_event(event_id)
        Deletes event that has matching id from database or throws an exception.

    """

    _events: List[Event]

    def __init__(self) -> None:
        self._events = []

    async def get_events_by_author_id(self, author_id: str) -> List[Event]:
        """
        Get events by author id.

        Parameters
        ----------
        author_id : str
            Author's id.

        Returns
        -------
        List[Event]
            List of events that matches by author id.

        Raises
        ------
        ValueNotFoundError
            No events was found for given author id.

        """
        events = [event for event in self._events if event.author_id == author_id]
        if events is None or len(events) == 0:
            raise ValueNotFoundError("Events not found")
        return events

    async def get_event_by_event_id(self, event_id: str) -> Event:
        """
        Get event by event id.

        Parameters
        ----------
        event_id : str
            Event's id.

        Returns
        -------
        List[Event]
            List of events that matches by event id.

        Raises
        ------
        ValueNotFoundError
            No events was found for given event id.

        """
        try:
           event = next(event for event in self._events if event.id == event_id)
           return event
        except StopIterationError:
           raise ValueNotFoundError("Events not found")

    async def get_events_by_events_ids(
        self, events_ids: ListOfEventsIds
    ) -> List[Event]:
        """
        Get events by events ids.

        Parameters
        ----------
        events_ids : ListOfEventsIds
            List of events ids.

        Returns
        -------
        List[Event]
            List of events that matches by event id.

        Raises
        ------
        ValueNotFoundError
            No events was found for given author id.

        """
        events = [event for event in self._events if event.id in events_ids.ids]
        if events is None or len(events) == 0:
            raise ValueNotFoundError("Events not found")
        return events

    async def create_event(self, event: Event) -> None:
        """
        Creates event with matching data or throws an exception

        Parameters
        ----------
        event : Event
            Event data

        """
        event.id = str(uuid4())
        self._events.append(event)

    async def update_event(self, event: Event) -> None:
        """
        Updates event with matching id or throws an exception

        Parameters
        ----------
        event : Event
            Event data

        Raises
        ------
        ValueNotFoundError
            Can't update event with provided data

        """
        try:
            index = next(i for i in range(len(self._events)) if self._events[i].id == event.id)
            if self._events[index].author_id == event.author_id:
                self._events[index] = event
            else:
                raise ValueNotFoundError("Events authors must be same")
        except StopIterationError:
            raise ValueNotFoundError("Event not found")

    async def delete_event(self, event_id: str) -> None:
        """
        Deletes event with matching id or throws an exception

        Parameters
        ----------
        event_id : str
            Event's id

        Raises
        ------
        ValueNotFoundError
            Can't delete event with provided data

        """
        try:
            index = next(i for i in range(len(self._events)) if self._events[i].id == event_id)
            self._events.pop(index)
        except StopIterationError:
            raise ValueNotFoundError("Event not found")
