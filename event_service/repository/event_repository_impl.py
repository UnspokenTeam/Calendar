"""Event repository with data from database."""
from datetime import datetime
from typing import Optional, List

from prisma.models import Event as PrismaEvent

from db.postgres_client import PostgresClient
from errors.value_not_found_error import ValueNotFoundError
from proto.event_service_pb2 import ListOfEventsIds
from repository.event_repository_interface import EventRepositoryInterface
from src.models.event import Event
from utils.singleton import singleton


@singleton
class EventRepositoryImpl(EventRepositoryInterface):
    """
    Class for manipulating with event data

    Attributes
    ----------
    _db_client : prisma.Client
        Postgres db client.

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

    _db_client: PostgresClient

    def __init__(self) -> None:
        self._db_client = PostgresClient()

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
        db_events: Optional[
            List[PrismaEvent]
        ] = await self._db_client.db.event.find_many(where={"id": author_id})
        if db_events is None or len(db_events) == 0:
            raise ValueNotFoundError("Events not found")
        return [
            Event.from_prisma_event(prisma_event=db_event) for db_event in db_events
        ]

    async def get_event_by_event_id(self, event_id: str) -> Event:
        """
        Get events by event id.

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
            No events was found for given event id.

        """
        db_event: Optional[PrismaEvent] = await self._db_client.db.event.find_first(
            where={"id": event_id}
        )
        if db_event is None:
            raise ValueNotFoundError("Event not found")
        return Event.from_prisma_event(prisma_event=db_event)

    async def get_events_by_events_ids(
        self, events_ids: ListOfEventsIds
    ) -> List[Event]:
        """
        Get events by events ids.

        Parameters
        ----------
        events_ids : ListOfEventsIds
            Event's ids.

        Returns
        -------
        List[Event]
            List of events that matches by event id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No events was found for given events ids.

        """
        db_events: Optional[
            List[PrismaEvent]
        ] = await self._db_client.db.event.find_many(
            where={"id": {"in": [event_id for event_id in events_ids.ids]}}
        )
        if db_events is None or len(db_events) == 0:
            raise ValueNotFoundError("Events not found")
        return [
            Event.from_prisma_event(prisma_event=db_event) for db_event in db_events
        ]

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
        await self._db_client.db.event.create(data=event.to_dict())

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
        await self._db_client.db.event.update(
            where={"id": event.id}, data=event.to_dict()
        )

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
        await self._db_client.db.event.update(
            where={"id": event_id}, data={"deleted_at": datetime.now()}
        )
