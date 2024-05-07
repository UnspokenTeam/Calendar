"""Notification repository with data from database."""

from datetime import datetime
from typing import List, Optional

from prisma.models import PrismaNotification

from db.postgres_client import PostgresClient
from errors.unique_error import UniqueError
from errors.value_not_found_error import ValueNotFoundError
from src.models.notification import Notification
from utils.singleton import singleton

from repository.notification_repository_interface import NotificationRepositoryInterface


@singleton
class NotificationRepositoryImpl(NotificationRepositoryInterface):
    """
    Class for manipulating with notification data.

    Attributes
    ----------
    _db_client : prisma.Client
        Postgres db client.

    Methods
    -------
    async get_notifications_by_author_id(author_id, page_number, items_per_page)
        Returns page with notifications that have matches with given author id.
    async get_notification_by_event_and_author_ids(event_id, author_id)
        Returns notification that has matches with given event and author ids.
    async get_notification_by_notification_id(notification_id)
        Returns notification that has matches with given notification id.
    async get_notifications_by_notifications_ids(notifications_ids, page_number, items_per_page)
        Returns page of notifications that have matches with given list of notification ids.
    async get_all_notifications(page_number, items_per_page)
        Returns page that contains part of all notifications.
    async create_notification(notification)
        Creates new notification inside db or throws an exception.
    async update_notification(notification)
        Updates notification that has the same id as provided notification object inside db or throws an exception.
    async delete_notification_by_id(notification_id)
        Deletes notification that has matching id from database or throws an exception.
    async delete_notifications_by_events_and_author_ids(event_ids, author_id)
        Deletes notifications that have matching event ids and author id from database or throws an exception.
    async delete_notifications_by_event_id(event_id)
        Deletes notifications that have matching event id from database or throws an exception.
    async delete_notifications_by_author_id(author_id)
        Deletes notifications that have matching author id from database or throws an exception.

    """

    _db_client: PostgresClient

    def __init__(self) -> None:
        self._db_client = PostgresClient()

    async def get_notifications_by_author_id(
        self, author_id: str, page_number: int, items_per_page: int
    ) -> List[Notification]:
        """
        Get notifications by author id.

        Parameters
        ----------
        author_id : str
            Author's id.
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.

        Returns
        -------
        List[Notification]
            List of notifications that match by author id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        db_notifications = await self._db_client.db.prismanotification.find_many(
            where={"author_id": author_id, "deleted_at": None},
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
        return [
            Notification.from_prisma_notification(prisma_notification=db_notification)
            for db_notification in db_notifications
        ]

    async def get_notification_by_event_and_author_ids(
        self, event_id: str, author_id: str
    ) -> Notification:
        """
        Get notification by event and author ids.

        Parameters
        ----------
        event_id : str
            Event's id.
        author_id : str
            Author's id.

        Returns
        -------
        Notification
            Notification that matches by event and author ids.

        Raises
        ------
        ValueNotFoundError
            No notification was found for given event and author ids.

        """
        db_notification: Optional[
            PrismaNotification
        ] = await self._db_client.db.prismanotification.find_first(
            where={"event_id": event_id, "author_id": author_id, "deleted_at": None}
        )
        if db_notification is None:
            raise ValueNotFoundError("Notification not found")
        return Notification.from_prisma_notification(
            prisma_notification=db_notification
        )

    async def get_notification_by_notification_id(
        self, notification_id: str
    ) -> Notification:
        """
        Get notifications by notification id.

        Parameters
        ----------
        notification_id : str
            Notification's id.

        Returns
        -------
        Notification
            Notification that matches by notification id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No notification was found for given notification id.

        """
        db_notification: Optional[
            PrismaNotification
        ] = await self._db_client.db.prismanotification.find_first(
            where={"id": notification_id, "deleted_at": None}
        )
        if db_notification is None:
            raise ValueNotFoundError("Notification not found")
        return Notification.from_prisma_notification(
            prisma_notification=db_notification
        )

    async def get_notifications_by_notifications_ids(
        self, notifications_ids: List[str], page_number: int, items_per_page: int
    ) -> List[Notification]:
        """
        Get notifications by notifications ids.

        Parameters
        ----------
        notifications_ids : List[str]
            Notification's ids.
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.

        Returns
        -------
        List[Notification]
            List of notifications that match by notification id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        db_notifications = await self._db_client.db.prismanotification.find_many(
            where={
                "id": {"in": notifications_ids},
                "deleted_at": None,
            },
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
        return [
            Notification.from_prisma_notification(prisma_notification=db_notification)
            for db_notification in db_notifications
        ]

    async def get_all_notifications(
        self, page_number: int, items_per_page: int
    ) -> List[Notification]:
        """
        Get all notifications.

        Parameters
        ----------
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.

        Returns
        -------
        List[Notification]
            List of notifications.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        db_notifications = await self._db_client.db.prismanotification.find_many(
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
        return [
            Notification.from_prisma_notification(prisma_notification=db_notification)
            for db_notification in db_notifications
        ]

    async def create_notification(self, notification: Notification) -> Notification:
        """
        Create an notification.

        Parameters
        ----------
        notification : Notification
            Notification object.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        UniqueError
            Raises if the notification already exists.

        """
        async with self._db_client.db.tx() as transaction:
            db_notification = await transaction.prismanotification.find_first(
                where={
                    "event_id": notification.event_id,
                    "author_id": notification.author_id,
                }
            )
            if db_notification is not None:
                if db_notification.enabled:
                    raise UniqueError("Notification already exists")
                await transaction.prismanotification.update_many(
                    where={
                        "event_id": notification.event_id,
                        "author_id": notification.author_id,
                    },
                    data={"enabled": True}
                    | (
                        {"created_at": datetime.now(), "deleted_at": None}
                        if db_notification.deleted_at is not None
                        else {}
                    ),
                )
                return Notification.from_prisma_notification(
                    await transaction.prismanotification.find_first(
                        where={
                            "event_id": notification.event_id,
                            "author_id": notification.author_id,
                        },
                    )
                )
            return Notification.from_prisma_notification(
                await transaction.prismanotification.create(
                    data=notification.to_dict(
                        exclude=["enabled", "created_at", "deleted_at"]
                    )
                )
            )

    async def update_notification(self, notification: Notification) -> Notification:
        """
        Update notification data.

        Parameters
        ----------
        notification : Notification
            Notification object.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        return Notification.from_prisma_notification(
            await self._db_client.db.prismanotification.update(
                where={"id": notification.id}, data=notification.to_dict()
            )
        )

    async def delete_notification_by_id(self, notification_id: str) -> None:
        """
        Delete the notification.

        Parameters
        ----------
        notification_id : str
            Notification id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        await self._db_client.db.prismanotification.update_many(
            where={"id": notification_id, "deleted_at": None},
            data={"enabled": False, "deleted_at": datetime.now()},
        )

    async def delete_notifications_by_events_and_author_ids(
        self, event_ids: List[str], author_id: str
    ) -> None:
        """
        Delete notifications by events and author ids.

        Parameters
        ----------
        event_ids : List[str]
            Event ids.
        author_id : str
            Author id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        await self._db_client.db.prismanotification.update_many(
            where={
                "event_id": {"in": event_ids},
                "author_id": author_id,
                "deleted_at": None,
            },
            data={"enabled": False, "deleted_at": datetime.now()},
        )

    async def delete_notifications_by_author_id(self, author_id: str) -> None:
        """
        Delete notifications by author id.

        Parameters
        ----------
        author_id : str
            Author id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        await self._db_client.db.prismanotification.update_many(
            where={"author_id": author_id, "deleted_at": None},
            data={"enabled": False, "deleted_at": datetime.now()},
        )

    async def delete_notifications_by_event_id(self, event_id: str) -> None:
        """
        Delete notifications by event id.

        Parameters
        ----------
        event_id : str
            Event id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.

        """
        await self._db_client.db.prismanotification.update_many(
            where={"event_id": event_id, "deleted_at": None},
            data={"enabled": False, "deleted_at": datetime.now()},
        )
