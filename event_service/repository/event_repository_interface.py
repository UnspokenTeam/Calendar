"""Event repository interface"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.models.event import Event


class EventRepositoryInterface(ABC):
    """
    Interface for class for manipulating with event data.

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
        Deletes events that have matches with given author id.

    """

    @abstractmethod
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
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No events were found for given author id.
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        pass

    @abstractmethod
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
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No event was found for given event id.

        """
        pass

    @abstractmethod
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
            List of events that match by event id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No events were found for given event ids.

        """
        pass

    @abstractmethod
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
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No events were found.
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        pass

    @abstractmethod
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
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        pass

    @abstractmethod
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
            Event with updated data.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        pass

    @abstractmethod
    async def delete_event_by_id(self, event_id: str) -> None:
        """
        Delete the event.

        Parameters
        ----------
        event_id : str
            Event id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        pass

    @abstractmethod
    async def delete_events_by_author_id(self, author_id: str) -> None:
        """
        Delete events.

        Parameters
        ----------
        author_id : str
            Author id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        pass
