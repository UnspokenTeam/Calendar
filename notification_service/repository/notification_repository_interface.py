"""Notification repository interface"""

from abc import ABC, abstractmethod
from typing import List

from src.models.notification import Notification


class NotificationRepositoryInterface(ABC):
    """
    Interface for class for manipulating with notification data.

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
    async delete_notification_by_id(notification_id)
        Deletes notification that has matching id from database or throws an exception.

    """

    @abstractmethod
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
        pass

    @abstractmethod
    async def get_notification_by_notification_id(
        self, notification_id: str
    ) -> Notification:
        """
        Get notification by notification id.

        Parameters
        ----------
        notification_id : str
            Notification's id.

        Returns
        -------
        Notification
            Notifications that matches by notification id.

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python.
        ValueNotFoundError
            No notifications were found for given notification id.

        """
        pass

    @abstractmethod
    async def get_notifications_by_notifications_ids(
        self, notifications_ids: List[str], page_number: int, items_per_page: int
    ) -> List[Notification]:
        """
        Get notifications by notifications ids.

        Parameters
        ----------
        notifications_ids : List[str]
            List of notifications ids.
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
            No notifications were found for given notification ids.

        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
