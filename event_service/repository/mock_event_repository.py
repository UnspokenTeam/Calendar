"""Mock event repository"""

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from errors.value_not_found_error import ValueNotFoundError
from src.models.event import Event
from utils.singleton import singleton

from repository.event_repository_interface import EventRepositoryInterface


@singleton
class MockEventRepositoryImpl(EventRepositoryInterface):
    """
    Mock class for manipulating with event data.

    Attributes
    ----------
    _events: List[Event]
        List of events.

    Methods
    -------
    async get_events_by_author_id(author_id, page_number, items_per_page, start, end)
        Returns page with events those have matches with given author id.
    async get_event_by_event_id(event_id)
        Returns event that has matches with given event id.
    async get_events_by_events_ids(events_ids, page_number, items_per_page)
        Returns page of events those have matches with given list of event ids.
    async get_all_events(page_number, items_per_page, start, end)
        Returns page that contains part of all events.
    async create_event(event)
        Creates new event inside db or throws an exception.
    async update_event(event)
        Updates event that has the same id as provided event object inside db or throws an exception.
    async delete_event_by_id(event_id)
        Deletes event that has matching id from database or throws an exception.
    async delete_events_by_author_id(author_id)
        Deletes events those have matching author events id from database or throws an exception

    """

    _events: List[Event]

    def __init__(self) -> None:
        self._events = []

    async def get_events_by_author_id(
        self,
        author_id: str,
        page_number: int,
        items_per_page: int,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[Event]:
        """
        Get events by author id and optionally timestamp.

        Parameters
        ----------
        author_id : str
            Author's id.
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.
        start : Optional[datetime]
            Start of time interval for search.
        end : Optional[datetime]
            End of time interval for search.

        Returns
        -------
        List[Event]
            List of events those match by author id.

        Raises
        ------
        ValueNotFoundError
            No events were found for given author id.

        """
        events = [
            event
            for event in self._events
            if event.author_id == author_id
            and (
                (True if start is None else start <= event.start)
                and (True if end is None else event.start <= end)
            )
            and event.deleted_at is None
        ]
        events = (
            events[items_per_page * (page_number - 1) : items_per_page * page_number]
            if items_per_page != -1
            else events
        )
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
        Event
            Event that matches by event id.

        Raises
        ------
        ValueNotFoundError
            No event was found for given event id.

        """
        try:
            return next(
                event
                for event in self._events
                if event.id == event_id and event.deleted_at is None
            )
        except StopIteration:
            raise ValueNotFoundError("Event not found")

    async def get_events_by_events_ids(
        self, events_ids: List[str], page_number: int, items_per_page: int
    ) -> List[Event]:
        """
        Get events by events ids.

        Parameters
        ----------
        events_ids : List[str]
            List of events ids.
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.

        Returns
        -------
        List[Event]
            List of events those match by event id.

        Raises
        ------
        ValueNotFoundError
            No events were found for given event ids.

        """
        events = [
            event
            for event in self._events
            if event.id in events_ids and event.deleted_at is None
        ]
        events = (
            events[items_per_page * (page_number - 1) : items_per_page * page_number]
            if items_per_page != -1
            else events
        )
        if events is None or len(events) == 0:
            raise ValueNotFoundError("Events not found")
        return events

    async def get_all_events(
        self,
        page_number: int,
        items_per_page: int,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[Event]:
        """
        Get all events, optionally in the custom timestamp.

        Parameters
        ----------
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.
        start : Optional[datetime]
            Start of time interval for search.
        end : Optional[datetime]
            End of time interval for search.

        Returns
        -------
        List[Event]
            List of events.

        Raises
        ------
        ValueNotFoundError
            No events were found.

        """
        events = [
            event
            for event in self._events
            if (
                (True if start is None else start <= event.start)
                and (True if end is None else event.start <= end)
            )
        ]
        events = (
            events[items_per_page * (page_number - 1) : items_per_page * page_number]
            if items_per_page != -1
            else events
        )
        if events is None or len(events) == 0:
            raise ValueNotFoundError("Events not found")
        return events

    async def create_event(self, event: Event) -> None:
        """
        Creates event with matching data or throws an exception.

        Parameters
        ----------
        event : Event
            Event data.

        """
        event.id = str(uuid4())
        event.created_at = datetime.now()
        event.deleted_at = None
        self._events.append(event)

    async def update_event(self, event: Event) -> None:
        """
        Updates event with matching id or throws an exception.

        Parameters
        ----------
        event : Event
            Event data.

        Raises
        ------
        ValueNotFoundError
            Can't update event with provided data.

        """
        try:
            index = next(
                i for i in range(len(self._events)) if self._events[i].id == event.id
            )
            if self._events[index].author_id == event.author_id:
                self._events[index] = event
            else:
                raise ValueNotFoundError("Events authors must be same")
        except StopIteration:
            raise ValueNotFoundError("Event not found")

    async def delete_event_by_id(self, event_id: str) -> None:
        """
        Deletes event with matching id or throws an exception.

        Parameters
        ----------
        event_id : str
            Event's id.

        Raises
        ------
        ValueNotFoundError
            Can't delete event with provided data.

        """
        try:
            index = next(
                i
                for i in range(len(self._events))
                if self._events[i].id == event_id and self._events[i].deleted_at is None
            )
            self._events[index].deleted_at = datetime.now()
        except StopIteration:
            raise ValueNotFoundError("Event not found")

    async def delete_events_by_author_id(self, author_id: str) -> None:
        """
        Deletes events with matching author ids or throws an exception.

        Parameters
        ----------
        author_id : str
            Author's id.

        Raises
        ------
        ValueNotFoundError
            Can't delete event with provided data.

        """
        try:
            index = next(
                i
                for i in range(len(self._events))
                if self._events[i].author_id == author_id
                and self._events[i].deleted_at is None
            )
            self._events[index].deleted_at = datetime.now()
        except StopIteration:
            raise ValueNotFoundError("Event not found")
