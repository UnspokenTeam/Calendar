"""Event repository with data from database."""

from datetime import datetime
from typing import List, Optional

from prisma.models import Event as PrismaEvent

from db.postgres_client import PostgresClient
from errors.value_not_found_error import ValueNotFoundError
from src.models.event import Event
from utils.singleton import singleton

from repository.event_repository_interface import EventRepositoryInterface


@singleton
class EventRepositoryImpl(EventRepositoryInterface):
    """
    Class for manipulating with event data.

    Attributes
    ----------
    _db_client : prisma.Client
        Postgres db client.

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
        Deletes events those have matches with given author id.

    """

    _db_client: PostgresClient

    def __init__(self) -> None:
        self._db_client = PostgresClient()

    async def get_events_by_author_id(
        self,
        author_id: str,
        page_number: int,
        items_per_page: int,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[Event]:
        """
        Get events by author id.

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
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No events were found for given author id.

        """
        db_events: Optional[
            List[PrismaEvent]
        ] = await self._db_client.db.event.find_many(
            where={
                "author_id": author_id,
                "deleted_at": None,
            }
            | (
                {}
                if not (
                    timestamp := ({} if start is None else {"_gte": start})
                    | ({} if end is None else {"_lte": end})
                )
                else {"start": timestamp}
            ),
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
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
            No event was found for given event id.

        """
        db_event: Optional[PrismaEvent] = await self._db_client.db.event.find_first(
            where={"id": event_id, "deleted_at": None}
        )
        if db_event is None:
            raise ValueNotFoundError("Event not found")
        return Event.from_prisma_event(prisma_event=db_event)

    async def get_events_by_events_ids(
        self, events_ids: List[str], page_number: int, items_per_page: int
    ) -> List[Event]:
        """
        Get events by events ids.

        Parameters
        ----------
        events_ids : List[str]
            Event's ids.
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
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No events were found for given events ids.

        """
        db_events: Optional[
            List[PrismaEvent]
        ] = await self._db_client.db.event.find_many(
            where={
                "id": {"in": events_ids},
                "deleted_at": None,
            },
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
        if db_events is None or len(db_events) == 0:
            raise ValueNotFoundError("Events not found")
        return [
            Event.from_prisma_event(prisma_event=db_event) for db_event in db_events
        ]

    async def get_all_events(
        self,
        page_number: int,
        items_per_page: int,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[Event]:
        """
        Get all events.

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

        """
        db_events: Optional[
            List[PrismaEvent]
        ] = await self._db_client.db.event.find_many(
            where={}
            if not (
                timestamp := ({} if start is None else {"_gte": start})
                | ({} if end is None else {"_lte": end})
            )
            else {"start": timestamp},
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
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
        await self._db_client.db.event.create(
            data=event.to_dict(exclude=["created_at", "deleted_at"])
        )

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
        await self._db_client.db.event.update_many(
            where={"id": event_id, "deleted_at": None},
            data={"deleted_at": datetime.now()},
        )

    async def delete_events_by_author_id(self, author_id: str) -> None:
        """
        Delete the event.

        Parameters
        ----------
        author_id : str
            Author id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        await self._db_client.db.event.update_many(
            where={"author_id": author_id, "deleted_at": None},
            data={"deleted_at": datetime.now()},
        )
