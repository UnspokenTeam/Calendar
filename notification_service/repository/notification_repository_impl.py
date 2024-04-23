"""Notification repository with data from database."""

from datetime import datetime
from typing import List, Optional

from prisma.models import Notification as PrismaNotification

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
        Returns page with notifications that has matches with given author id.
    async get_notification_by_notification_id(notification_id)
        Returns notification that has matches with given notification id.
    async get_notifications_by_notifications_ids(notifications_ids, page_number, items_per_page)
        Returns page of notifications that has matches with given list of notification ids.
    async get_all_notifications(page_number, items_per_page)
        Returns page that contains part of all notifications.
    async create_notification(notification)
        Creates new notification inside db or throws an exception.
    async update_notification(notification)
        Updates notification that has the same id as provided notification object inside db or throws an exception.
    async delete_notification(notification_id)
        Deletes notification that has matching id from database or throws an exception.

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
            List of notifications that matches by author id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No notifications were found for given author id.

        """
        db_notifications: Optional[
            List[PrismaNotification]
        ] = await self._db_client.db.notification.find_many(
            where={"author_id": author_id, "deleted_at": None},
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
        if db_notifications is None or len(db_notifications) == 0:
            raise ValueNotFoundError("Notifications not found")
        return [
            Notification.from_prisma_notification(prisma_notification=db_notification)
            for db_notification in db_notifications
        ]

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
            No notifications were found for given notification id.

        """
        db_notification: Optional[
            PrismaNotification
        ] = await self._db_client.db.notification.find_first(
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
            List of notifications that matches by notification id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No notifications were found for given notifications ids.

        """
        db_notifications: Optional[
            List[PrismaNotification]
        ] = await self._db_client.db.notification.find_many(
            where={
                "id": {"in": notifications_ids},
                "deleted_at": None,
            },
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
        if db_notifications is None or len(db_notifications) == 0:
            raise ValueNotFoundError("Notifications not found")
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
        ValueNotFoundError
            No notifications were found.

        """
        db_notifications: Optional[
            List[PrismaNotification]
        ] = await self._db_client.db.notification.find_many(
            skip=(items_per_page * (page_number - 1) if items_per_page != -1 else None),
            take=items_per_page if items_per_page != -1 else None,
        )
        if db_notifications is None or len(db_notifications) == 0:
            raise ValueNotFoundError("Notifications not found")
        return [
            Notification.from_prisma_notification(prisma_notification=db_notification)
            for db_notification in db_notifications
        ]

    async def create_notification(self, notification: Notification) -> None:
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
        db_notification: Optional[
            PrismaNotification
        ] = await self._db_client.db.notification.find_first(
            where={
                "event_id": notification.event_id,
                "author_id": notification.author_id,
                "deleted_at": None,
            }
        )
        if db_notification is None:
            await self._db_client.db.notification.create(
                data=notification.to_dict(exclude=["created_at", "deleted_at"])
            )
        else:
            raise UniqueError("Notification already exists")

    async def update_notification(self, notification: Notification) -> None:
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
        await self._db_client.db.notification.update(
            where={"id": notification.id}, data=notification.to_dict()
        )

    async def delete_notification(self, notification_id: str) -> None:
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
        await self._db_client.db.notification.update_many(
            where={"id": notification_id, "deleted_at": None},
            data={"deleted_at": datetime.now()},
        )
