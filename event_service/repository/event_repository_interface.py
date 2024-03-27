"""Event repository interface"""
# mypy: ignore-errors
from typing import List

from src.models.event import Event


class EventRepositoryInterface:
    """
    Interface for class for manipulating with event data

    Methods
    -------
    async get_events(author_id)
        Returns events that has matches with given author id.
    async create_event(event)
        Creates new event inside db or throws an exception.
    async update_event(event)
        Updates event that has the same id as provided event object inside db or throws an exception.
    async delete_event(event_id)
        Deletes event that has matching id from database or throws an exception.

    """

    async def get_events(self, author_id: str) -> List[Event]:
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
