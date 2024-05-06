"""Mock event repository"""

from calendar import isleap
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4

from errors.value_not_found_error import ValueNotFoundError
from errors.wrong_interval_error import WrongIntervalError
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
        Returns page with events that have matches with given author id.
    async get_event_by_event_id(event_id)
        Returns event that has matches with given event id.
    async get_events_by_events_ids(events_ids, page_number, items_per_page)
        Returns page of events that have matches with given list of event ids.
    async get_all_events(page_number, items_per_page, start, end)
        Returns page that contains part of all events.
    async create_event(event)
        Creates new event inside db or throws an exception.
    async update_event(event)
        Updates event that has the same id as provided event object inside db or throws an exception.
    async delete_event_by_id(event_id)
        Deletes event that has matching id from database or throws an exception.
    async delete_events_by_author_id(author_id)
        Deletes events that have matching author events id from database or throws an exception

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
            List of events that match by author id.

        Raises
        ------
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        if start is not None and end is not None and start > end:
            raise WrongIntervalError("Request failed. Wrong time interval.")
        events = []
        for event in self._events:
            if event.repeating_delay is not None and not (
                (True if start is None else start <= event.start)
                and (True if end is None else event.start <= end)
            ):
                repeating_delay = (
                    datetime.now()
                    - (
                        datetime.now()
                        - event.delay_string_to_timedelta(event.repeating_delay)
                    )
                ).total_seconds()
                start_modulo, end_modulo = None, None
                if start is not None:
                    start_seconds = int(start.timestamp())
                    start_modulo = start_seconds % repeating_delay
                if end is not None:
                    end_seconds = int(end.timestamp())
                    end_modulo = end_seconds % repeating_delay
                    end_modulo = repeating_delay if not end_modulo else end_modulo
                event_seconds = int(event.start.timestamp())
                event_modulo = event_seconds % repeating_delay
                if (
                    (True if start is None else start_modulo <= event_modulo)
                    and (True if end is None else event_modulo <= end_modulo)
                    and (True if end is None else event.start <= end)
                    and event.author_id == author_id
                    and event.deleted_at is None
                ):
                    events.append(event)
            else:
                if (
                    (start <= event.start if start is not None else True)
                    and (event.start <= end if end is not None else True)
                    and event.author_id == author_id
                    and event.deleted_at is None
                ):
                    events.append(event)
        if events is None or len(events) == 0:
            return []
        if start is not None and end is None:
            end = start + timedelta(days=366 if isleap(start.year) else 365)
        for event in events[:]:
            if event.repeating_delay is not None:
                amount_of_repeats = 1
                repeating_event = event.__copy__()
                while True:
                    repeating_event.start += (
                        Event.delay_string_to_timedelta(event.repeating_delay)
                        * amount_of_repeats
                    )
                    repeating_event.end += (
                        Event.delay_string_to_timedelta(event.repeating_delay)
                        * amount_of_repeats
                    )
                    if repeating_event.start > end:
                        break
                    if (
                        start <= repeating_event.start if start is not None else True
                    ) and (repeating_event.start <= end if end is not None else True):
                        events.append(repeating_event)
                    amount_of_repeats += 1
                    repeating_event = event.__copy__()
        events = sorted(events, key=lambda event_sort: event_sort.start)
        return (
            events[items_per_page * (page_number - 1) : items_per_page * page_number]
            if items_per_page != -1
            else events
        )

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
        self,
        events_ids: List[str],
        page_number: int,
        items_per_page: int,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
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
        start : Optional[datetime]
            Start of time interval for search.
        end : Optional[datetime]
            End of time interval for search.

        Returns
        -------
        List[Event]
            List of events that match by event id.

        Raises
        ------
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        if start is not None and end is not None and start > end:
            raise WrongIntervalError("Request failed. Wrong time interval.")
        events = []
        for event in self._events:
            if event.repeating_delay is not None and not (
                (True if start is None else start <= event.start)
                and (True if end is None else event.start <= end)
            ):
                repeating_delay = (
                    datetime.now()
                    - (
                        datetime.now()
                        - event.delay_string_to_timedelta(event.repeating_delay)
                    )
                ).total_seconds()
                start_modulo, end_modulo = None, None
                if start is not None:
                    start_seconds = int(start.timestamp())
                    start_modulo = start_seconds % repeating_delay
                if end is not None:
                    end_seconds = int(end.timestamp())
                    end_modulo = end_seconds % repeating_delay
                    end_modulo = repeating_delay if not end_modulo else end_modulo
                event_seconds = int(event.start.timestamp())
                event_modulo = event_seconds % repeating_delay
                if (
                    (True if start is None else start_modulo <= event_modulo)
                    and (True if end is None else event_modulo <= end_modulo)
                    and (True if end is None else event.start <= end)
                    and event.id in events_ids
                    and event.deleted_at is None
                ):
                    events.append(event)
            else:
                if (
                    (start <= event.start if start is not None else True)
                    and (event.start <= end if end is not None else True)
                    and event.id in events_ids
                    and event.deleted_at is None
                ):
                    events.append(event)
        if events is None or len(events) == 0:
            return []
        if start is not None and end is None:
            end = start + timedelta(days=366 if isleap(start.year) else 365)
        for event in events[:]:
            if event.repeating_delay is not None:
                amount_of_repeats = 1
                repeating_event = event.__copy__()
                while True:
                    repeating_event.start += (
                        Event.delay_string_to_timedelta(event.repeating_delay)
                        * amount_of_repeats
                    )
                    repeating_event.end += (
                        Event.delay_string_to_timedelta(event.repeating_delay)
                        * amount_of_repeats
                    )
                    if repeating_event.start > end:
                        break
                    if (
                        start <= repeating_event.start if start is not None else True
                    ) and (repeating_event.start <= end if end is not None else True):
                        events.append(repeating_event)
                    amount_of_repeats += 1
                    repeating_event = event.__copy__()
        events = sorted(events, key=lambda event_sort: event_sort.start)
        return (
            events[items_per_page * (page_number - 1) : items_per_page * page_number]
            if items_per_page != -1
            else events
        )

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
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        if start is not None and end is not None and start > end:
            raise WrongIntervalError("Request failed. Wrong time interval.")
        events = []
        for event in self._events:
            if event.repeating_delay is not None and not (
                (True if start is None else start <= event.start)
                and (True if end is None else event.start <= end)
            ):
                repeating_delay = (
                    datetime.now()
                    - (
                        datetime.now()
                        - event.delay_string_to_timedelta(event.repeating_delay)
                    )
                ).total_seconds()
                start_modulo, end_modulo = None, None
                if start is not None:
                    start_seconds = int(start.timestamp())
                    start_modulo = start_seconds % repeating_delay
                if end is not None:
                    end_seconds = int(end.timestamp())
                    end_modulo = end_seconds % repeating_delay
                    end_modulo = repeating_delay if not end_modulo else end_modulo
                event_seconds = int(event.start.timestamp())
                event_modulo = event_seconds % repeating_delay
                if (
                    (True if start is None else start_modulo <= event_modulo)
                    and (True if end is None else event_modulo <= end_modulo)
                    and (True if end is None else event.start <= end)
                ):
                    events.append(event)
            else:
                if (start <= event.start if start is not None else True) and (
                    event.start <= end if end is not None else True
                ):
                    events.append(event)
        if events is None or len(events) == 0:
            return []
        if start is not None and end is None:
            end = start + timedelta(days=366 if isleap(start.year) else 365)
        for event in events[:]:
            if event.repeating_delay is not None:
                amount_of_repeats = 1
                repeating_event = event.__copy__()
                while True:
                    repeating_event.start += (
                        Event.delay_string_to_timedelta(event.repeating_delay)
                        * amount_of_repeats
                    )
                    repeating_event.end += (
                        Event.delay_string_to_timedelta(event.repeating_delay)
                        * amount_of_repeats
                    )
                    if repeating_event.start > end:
                        break
                    if (
                        start <= repeating_event.start if start is not None else True
                    ) and (repeating_event.start <= end if end is not None else True):
                        events.append(repeating_event)
                    amount_of_repeats += 1
                    repeating_event = event.__copy__()
        events = sorted(events, key=lambda event_sort: event_sort.start)
        return (
            events[items_per_page * (page_number - 1) : items_per_page * page_number]
            if items_per_page != -1
            else events
        )

    async def create_event(self, event: Event) -> Event:
        """
        Create an event.

        Parameters
        ----------
        event : Event
            Event object.

        Returns
        -------
        Event
            Created event.

        Raises
        ------
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        if event.start > event.end:
            raise WrongIntervalError(
                "Request failed. Can't create event with wrong time interval."
            )
        event.id = str(uuid4())
        event.created_at = datetime.utcnow()
        event.deleted_at = None
        self._events.append(event)
        return event

    async def update_event(self, event: Event) -> Event:
        """
        Update event data.

        Parameters
        ----------
        event : Event
            Event object.

        Returns
        -------
        Event
            Updated event.

        Raises
        ------
        ValueNotFoundError
            Can't update event with provided data.
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        if event.start > event.end:
            raise WrongIntervalError(
                "Request failed. Can't create event with wrong time interval."
            )
        try:
            index = next(
                i for i in range(len(self._events)) if self._events[i].id == event.id
            )
            if self._events[index].author_id == event.author_id:
                self._events[index] = event
                return event
            raise ValueNotFoundError("Events authors must be same")
        except StopIteration:
            raise ValueNotFoundError("Event not found")

    async def delete_event_by_id(self, event_id: str) -> None:
        """
        Delete the event.

        Parameters
        ----------
        event_id : str
            Event id.

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
            self._events[index].deleted_at = datetime.utcnow()
        except StopIteration:
            raise ValueNotFoundError("Event not found")

    async def delete_events_by_author_id(self, author_id: str) -> None:
        """
        Delete events.

        Parameters
        ----------
        author_id : str
            Event id.

        Raises
        ------
        ValueNotFoundError
            Can't delete event with provided data.

        """
        indexes = tuple(
            i
            for i in range(len(self._events))
            if self._events[i].author_id == author_id
            and self._events[i].deleted_at is None
        )
        if len(indexes) == 0:
            raise ValueNotFoundError("Events not found")
        for index in indexes:
            self._events[index].deleted_at = datetime.utcnow()
