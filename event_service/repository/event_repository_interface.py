"""Event repository interface"""
from abc import ABC, abstractmethod
from typing import List

from src.models.event import Event


class EventRepositoryInterface(ABC):
    """
    Interface for class for manipulating with event data.

    Methods
    -------
    async get_events_by_author_id(author_id)
        Returns events that has matches with given author id.
    async get_event_by_event_id(event_id)
        Returns event that has matches with given event id.
    async get_events_by_events_ids(events_ids)
        Returns events that has matches with given list of event ids.
    async get_all_events()
        Returns all events.
    async create_event(event)
        Creates new event inside db or throws an exception.
    async update_event(event)
        Updates event that has the same id as provided event object inside db or throws an exception.
    async delete_event(event_id)
        Deletes event that has matching id from database or throws an exception.

    """

    @abstractmethod
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
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No events was found for given author id.

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
            List of events that matches by event id.

        Raises
        ------
        ValueNotFoundError
            No events was found for given event id.

        """
        pass

    @abstractmethod
    async def get_events_by_events_ids(self, events_ids: List[str]) -> List[Event]:
        """
        Get events by events ids.

        Parameters
        ----------
        events_ids : List[str]
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
        pass

    @abstractmethod
    async def get_all_events(self) -> List[Event]:
        """
        Get all events.

        Returns
        -------
        List[Event]
            List of events that matches by event id.

        Raises
        ------
        ValueNotFoundError
            No events was found for given author id.

        """
        pass

    @abstractmethod
    async def create_event(self, event: Event) -> None:
        """
        Create an event.

        Parameters
        ----------
        event : Event
            Event object.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        pass

    @abstractmethod
    async def update_event(self, event: Event) -> None:
        """
        Update event data.

        Parameters
        ----------
        event : Event
            Event object.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        pass

    @abstractmethod
    async def delete_event(self, event_id: str) -> None:
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
