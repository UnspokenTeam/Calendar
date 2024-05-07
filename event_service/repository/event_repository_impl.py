"""Event repository with data from database."""

from datetime import datetime
from typing import List, Optional

from prisma.models import PrismaEvent

from db.postgres_client import PostgresClient
from errors.value_not_found_error import ValueNotFoundError
from errors.wrong_interval_error import WrongIntervalError
from src.models.event import Event
from utils.singleton import singleton

from constants import (
    GET_ALL_EVENTS_QUERY,
    GET_EVENTS_BY_AUTHOR_ID_QUERY,
    GET_EVENTS_BY_EVENT_IDS_QUERY,
)
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
    async get_events_by_events_ids(events_ids, page_number, items_per_page, start, end)
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
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        if start is not None and end is not None and start > end:
            raise WrongIntervalError("Request failed. Wrong time interval.")
        start_date, end_date = None, None
        # fmt: off
        if start is not None:
            start_date = (
                f"\'{start.day:02d}/{start.month:02d}/{start.year:04d} "
                f"{start.hour:02d}:{start.minute:02d}:{start.second:02d}\'"
            )
        if end is not None:
            end_date = (
                f"\'{end.day:02d}/{end.month:02d}/{end.year:04d} "
                f"{end.hour:02d}:{end.minute:02d}:{end.second:02d}\'"
            )
        time_interval = (
            f"{end_date}::timestamp"
            if end is not None
            else (
                f"{start_date}::timestamp + \'1 MONTH\'::interval"
                if start_date is not None
                else "event.start::timestamp + \'1 MONTH\'::interval"
            )
        )
        author_id_for_query = f"'{author_id}'"
        repeating_event_start_condition = (
            f"\n\tAND {start_date}::timestamp <= pattern.\"event_start\""
            if start is not None
            else ""
        )
        repeating_event_end_condition = (
            f"\n\tAND pattern.\"event_start\" <= {end_date}::timestamp" if end is not None else ""
        )
        # fmt: on
        pagination_parameters = (
            f"\nLIMIT {items_per_page}\nOFFSET {items_per_page * (page_number - 1)}"
            if items_per_page != -1
            else ""
        )
        await self._db_client.db.execute_raw("SET datestyle = DMY;")
        db_events = await self._db_client.db.query_raw(
            GET_EVENTS_BY_AUTHOR_ID_QUERY.format(
                time_interval,
                author_id_for_query,
                repeating_event_start_condition,
                repeating_event_end_condition,
                pagination_parameters,
            ),
            model=PrismaEvent,
        )
        return [
            Event.from_prisma_event(prisma_event=db_event)
            for db_event in db_events
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
        db_event: Optional[
            PrismaEvent
        ] = await self._db_client.db.prismaevent.find_first(
            where={"id": event_id, "deleted_at": None}
        )
        if db_event is None:
            raise ValueNotFoundError("Event not found")
        return Event.from_prisma_event(prisma_event=db_event)

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
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        if start is not None and end is not None and start > end:
            raise WrongIntervalError("Request failed. Wrong time interval.")
        start_date, end_date = None, None
        # fmt: off
        if start is not None:
            start_date = (
                f"\'{start.day:02d}/{start.month:02d}/{start.year:04d} "
                f"{start.hour:02d}:{start.minute:02d}:{start.second:02d}\'"
            )
        if end is not None:
            end_date = (
                f"\'{end.day:02d}/{end.month:02d}/{end.year:04d} "
                f"{end.hour:02d}:{end.minute:02d}:{end.second:02d}\'"
            )
        time_interval = (
            f"{end_date}::timestamp"
            if end is not None
            else (
                f"{start_date}::timestamp + \'1 MONTH\'::interval"
                if start_date is not None
                else "event.start::timestamp + \'1 MONTH\'::interval"
            )
        )
        events_ids_for_query = ", ".join(f"'{event_id}'" for event_id in events_ids)
        repeating_event_start_condition = (
            f"\n\tAND {start_date}::timestamp <= pattern.\"event_start\""
            if start is not None
            else ""
        )
        repeating_event_end_condition = (
            f"\n\tAND pattern.\"event_start\" <= {end_date}::timestamp" if end is not None else ""
        )
        # fmt: on
        pagination_parameters = (
            f"\nLIMIT {items_per_page}\nOFFSET {items_per_page * (page_number - 1)}"
            if items_per_page != -1
            else ""
        )
        await self._db_client.db.execute_raw("SET datestyle = DMY;")
        db_events = await self._db_client.db.query_raw(
            GET_EVENTS_BY_EVENT_IDS_QUERY.format(
                time_interval,
                events_ids_for_query,
                repeating_event_start_condition,
                repeating_event_end_condition,
                pagination_parameters,
            ),
            model=PrismaEvent,
        )
        return [
            Event.from_prisma_event(prisma_event=db_event)
            for db_event in db_events
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
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        if start is not None and end is not None and start > end:
            raise WrongIntervalError("Request failed. Wrong time interval.")
        start_date, end_date = None, None
        # fmt: off
        if start is not None:
            start_date = (
                f"\'{start.day:02d}/{start.month:02d}/{start.year:04d} "
                f"{start.hour:02d}:{start.minute:02d}:{start.second:02d}\'"
            )
        if end is not None:
            end_date = (
                f"\'{end.day:02d}/{end.month:02d}/{end.year:04d} "
                f"{end.hour:02d}:{end.minute:02d}:{end.second:02d}\'"
            )
        time_interval = (
            f"{end_date}::timestamp"
            if end is not None
            else (
                f"{start_date}::timestamp + \'1 MONTH\'::interval"
                if start_date is not None
                else "event.start::timestamp + \'1 MONTH\'::interval"
            )
        )
        where_condition_for_repeating_events = (
            (
                "\nWHERE\n\t"
                + (
                    f"{start_date}::timestamp <= pattern.\"event_start\""
                    if start is not None
                    else ""
                )
                + ("\n\tAND " if start is not None and end is not None else "")
                + (f"pattern.\"event_start\" <= {end_date}::timestamp" if end is not None else "")
            )
            if start is not None or end is not None
            else ""
        )
        # fmt: on
        pagination_parameters = (
            f"\nLIMIT {items_per_page}\nOFFSET {items_per_page * (page_number - 1)}"
            if items_per_page != -1
            else ""
        )
        await self._db_client.db.execute_raw("SET datestyle = DMY;")
        db_events = await self._db_client.db.query_raw(
            GET_ALL_EVENTS_QUERY.format(
                time_interval,
                where_condition_for_repeating_events,
                pagination_parameters,
            ),
            model=PrismaEvent,
        )
        return [
            Event.from_prisma_event(prisma_event=db_event)
            for db_event in db_events
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
        return Event.from_prisma_event(
            await self._db_client.db.prismaevent.create(
                data=event.to_dict(exclude=["created_at", "deleted_at"])
            )
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
        return Event.from_prisma_event(
            await self._db_client.db.prismaevent.update(
                where={"id": event.id}, data=event.to_dict()
            )
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
        await self._db_client.db.prismaevent.update_many(
            where={"id": event_id, "deleted_at": None},
            data={"deleted_at": datetime.utcnow()},
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
        await self._db_client.db.prismaevent.update_many(
            where={"author_id": author_id, "deleted_at": None},
            data={"deleted_at": datetime.utcnow()},
        )
