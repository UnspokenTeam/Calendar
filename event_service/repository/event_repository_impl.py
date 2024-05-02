"""Event repository with data from database."""

from datetime import datetime
from typing import List, Optional

from prisma.models import Event as PrismaEvent

from db.postgres_client import PostgresClient
from errors.value_not_found_error import ValueNotFoundError
from errors.wrong_interval_error import WrongIntervalError
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
        if start is not None and end is not None and start > end:
            raise WrongIntervalError("Request failed. Wrong time interval.")
        start_date, end_date = None, None
        if start is not None:
            start_date = (
                f"'{start.day:02d}/{start.month:02d}/{start.year:04d} "
                f"{start.hour:02d}:{start.minute:02d}:{start.second:02d}'"
            )
        if end is not None:
            end_date = (
                f"'{end.day:02d}/{end.month:02d}/{end.year:04d} "
                f"{end.hour:02d}:{end.minute:02d}:{end.second:02d}'"
            )
        await self._db_client.db.execute_raw("SET datestyle = DMY;")
        db_events: Optional[List[PrismaEvent]] = await self._db_client.db.query_raw(
            # fmt: off
            "SELECT *\nFROM \"Event\" as event\nWHERE\n\tevent.author_id = {}\n\tAND event.deleted_at IS NULL{}{}\n"
            "UNION\nSELECT DISTINCT pattern.\"id\", pattern.\"title\", pattern.\"description\", pattern.\"color\", "
            "pattern.\"start\", pattern.\"end\", pattern.\"repeating_delay\", pattern.\"author_id\", "
            "pattern.\"created_at\", pattern.\"deleted_at\"\nFROM (\n\tSELECT *\n\tFROM \"Event\" as event, "
            "GENERATE_SERIES(event.start, {}, event.repeating_delay::interval) as event_start_series\n\t"
            "WHERE event.repeating_delay IS NOT NULL\n) as pattern\nWHERE\n\tpattern.author_id = {}\n\t"
            "AND pattern.deleted_at IS NULL{}{}\nORDER BY start{};".format(
                # fmt: on
                f"\'{author_id}\'",
                f"\n\tAND {start_date}::timestamp <= event.start"
                if start is not None
                else "",
                f"\n\tAND event.start <= {end_date}::timestamp"
                if end is not None
                else "",
                f"timestamp {end_date}"
                if end is not None
                else f"{start_date}::timestamp + event.repeating_delay::interval",
                f"\'{author_id}\'",
                f"\n\tAND {start_date}::timestamp <= pattern.event_start_series"
                if start is not None
                else "",
                f"\n\tAND pattern.event_start_series <= {end_date}::timestamp"
                if end is not None
                else "",
                f"\nLIMIT {items_per_page}\nOFFSET {items_per_page * (page_number - 1)}"
                if items_per_page != -1
                else "",
            ),
            model=PrismaEvent,
        )
        if db_events is None or len(db_events) == 0:
            raise ValueNotFoundError("Events not found")
        return [
            Event.from_prisma_event(prisma_event=db_event) for db_event in db_events
        ]

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
            List of events that match by event id.

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
        if start is not None and end is not None and start > end:
            raise WrongIntervalError("Request failed. Wrong time interval.")
        start_date, end_date = None, None
        if start is not None:
            start_date = (
                f"'{start.day:02d}/{start.month:02d}/{start.year:04d} "
                f"{start.hour:02d}:{start.minute:02d}:{start.second:02d}'"
            )
        if end is not None:
            end_date = (
                f"'{end.day:02d}/{end.month:02d}/{end.year:04d} "
                f"{end.hour:02d}:{end.minute:02d}:{end.second:02d}'"
            )
        await self._db_client.db.execute_raw("SET datestyle = DMY;")
        db_events: Optional[List[PrismaEvent]] = await self._db_client.db.query_raw(
            # fmt: off
            "SELECT *\nFROM \"Event\" as event{}\nUNION\n"
            "SELECT DISTINCT pattern.\"id\", pattern.\"title\", pattern.\"description\", pattern.\"color\", "
            "pattern.\"start\", pattern.\"end\", pattern.\"repeating_delay\", pattern.\"author_id\", "
            "pattern.\"created_at\", pattern.\"deleted_at\"\nFROM (\n\tSELECT *\n\tFROM \"Event\" as event, "
            "GENERATE_SERIES(event.start, {}, event.repeating_delay::interval) as event_start_series\n"
            "\tWHERE event.repeating_delay IS NOT NULL\n) as pattern{}\nORDER BY start{};".format(
                # fmt: on
                "\nWHERE\n\t"
                + (
                    f"{start_date}::timestamp <= event.start"
                    if start is not None
                    else ""
                )
                + ("\n\tAND " if start is not None and end is not None else "")
                + (f"event.start <= {end_date}::timestamp" if end is not None else "")
                if start is not None or end is not None
                else "",
                f"timestamp {end_date}"
                if end is not None
                else f"{start_date}::timestamp + event.repeating_delay::interval",
                "\nWHERE\n\t"
                + (
                    f"{start_date}::timestamp <= pattern.event_start_series"
                    if start is not None
                    else ""
                )
                + ("\n\tAND " if start is not None and end is not None else "")
                + (
                    f"pattern.event_start_series <= {end_date}::timestamp"
                    if end is not None
                    else ""
                )
                if start is not None or end is not None
                else "",
                f"\nLIMIT {items_per_page}\nOFFSET {items_per_page * (page_number - 1)}"
                if items_per_page != -1
                else "",
            ),
            model=PrismaEvent,
        )
        if db_events is None or len(db_events) == 0:
            raise ValueNotFoundError("Events not found")
        return [
            Event.from_prisma_event(prisma_event=db_event) for db_event in db_events
        ]

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
        if event.start > event.end:
            raise WrongIntervalError(
                "Request failed. Can't create event with wrong time interval."
            )
        return await self._db_client.db.event.create(
            data=event.to_dict(exclude=["created_at", "deleted_at"])
        )

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
        if event.start > event.end:
            raise WrongIntervalError(
                "Request failed. Can't create event with wrong time interval."
            )
        return await self._db_client.db.event.update(
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
        Delete events.

        Parameters
        ----------
        author_id : str
            Author's id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        await self._db_client.db.event.update_many(
            where={"author_id": author_id, "deleted_at": None},
            data={"deleted_at": datetime.now()},
        )
