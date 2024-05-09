"""Mock notification repository"""

from calendar import monthrange
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4

from errors.unique_error import UniqueError
from errors.value_not_found_error import ValueNotFoundError
from errors.wrong_inerval_error import WrongIntervalError
from src.models.notification import Notification
from utils.singleton import singleton

from repository.notification_repository_interface import NotificationRepositoryInterface


@singleton
class MockNotificationRepositoryImpl(NotificationRepositoryInterface):
    """
    Mock class for manipulating with notification data.

    Attributes
    ----------
    _notifications: List[Notification]
        List of notifications.

    Methods
    -------
    async get_notifications_by_author_id(author_id, page_number, items_per_page, start, end)
        Returns page with notifications that have matches with given author id.
    async get_notifications_by_event_id(event_id, page_number, items_per_page)
        Returns page with notifications that have matches with given event id.
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

    _notifications: List[Notification]

    def __init__(self) -> None:
        self._notifications = []

    async def get_notifications_by_author_id(
        self,
        author_id: str,
        page_number: int,
        items_per_page: int,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
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
        start : Optional[datetime]
            Start of time interval for search.
        end : Optional[datetime]
            End of time interval for search.

        Returns
        -------
        List[Notification]
            List of notifications that match by author id.

        Raises
        ------
        WrongIntervalError
            Start of time interval is later than end of time interval.

        """
        if start is not None and end is not None and start > end:
            raise WrongIntervalError("Request failed. Wrong time interval.")
        notifications = [
            notification
            for notification in self._notifications
            if notification.author_id == author_id
            and notification.enabled
            and notification.deleted_at is None
        ]
        if notifications is None or len(notifications) == 0:
            return []
        if start is not None and end is None:
            end = start + timedelta(
                days=current_month_len - start.day + next_month_len
                if (current_month_len := monthrange(start.year, start.month)[1])
                > (
                    next_month_len := monthrange(
                        start.year + start.month // 12, start.month % 12 + 1
                    )[1]
                )
                and start.day > next_month_len
                else current_month_len
            )
        for notification in notifications[:]:
            if notification.repeating_delay is not None:
                amount_of_repeats = 1
                repeating_notification = notification.__copy__()
                while True:
                    repeating_notification.start += (
                        Notification.delay_string_to_timedelta(
                            notification.repeating_delay
                        )
                        * amount_of_repeats
                    )
                    if repeating_notification.start > end:
                        break
                    if (
                        start <= repeating_notification.start
                        if start is not None
                        else True
                    ) and (
                        repeating_notification.start <= end if end is not None else True
                    ):
                        notifications.append(repeating_notification)
                    amount_of_repeats += 1
                    repeating_notification = notification.__copy__()
        notifications = sorted(
            notifications, key=lambda notification_sort: notification_sort.start
        )
        return (
            notifications[
                items_per_page * (page_number - 1) : items_per_page * page_number
            ]
            if items_per_page != -1
            else notifications
        )

    async def get_notifications_by_event_id(
        self, event_id: str, page_number: int, items_per_page: int
    ) -> List[Notification]:
        """
        Get notifications by author id.

        Parameters
        ----------
        event_id : str
            Event's id.
        page_number : int
            Number of page to get.
        items_per_page : int
            Number of items per page to load.

        Returns
        -------
        List[Notification]
            List of notifications that match by event id.

        """
        notifications = [
            notification
            for notification in self._notifications
            if notification.event_id == event_id
            and notification.enabled
            and notification.deleted_at is None
        ]
        return (
            notifications[
                items_per_page * (page_number - 1) : items_per_page * page_number
            ]
            if items_per_page != -1
            else notifications
        )

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
        try:
            return next(
                notification
                for notification in self._notifications
                if notification.author_id == author_id
                and notification.event_id == event_id
                and notification.enabled
                and notification.deleted_at is None
            )
        except StopIteration:
            raise ValueNotFoundError("Notification not found")

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
            Notification that matches by notification id.

        Raises
        ------
        ValueNotFoundError
            No notification was found for given notification id.

        """
        try:
            return next(
                notification
                for notification in self._notifications
                if notification.id == notification_id
                and notification.enabled
                and notification.deleted_at is None
            )
        except StopIteration:
            raise ValueNotFoundError("Notification not found")

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
            List of notifications that match by notification id.

        """
        notifications = [
            notification
            for notification in self._notifications
            if notification.id in notifications_ids
            and notification.enabled
            and notification.deleted_at is None
        ]
        return (
            notifications[
                items_per_page * (page_number - 1) : items_per_page * page_number
            ]
            if items_per_page != -1
            else notifications
        )

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

        """
        return (
            self._notifications[
                items_per_page * (page_number - 1) : items_per_page * page_number
            ]
            if items_per_page != -1
            else self._notifications
        )

    async def create_notification(self, notification: Notification) -> Notification:
        """
        Creates notification with matching data or throws an exception.

        Parameters
        ----------
        notification : Notification
            Notification data.

        Returns
        -------
        Notification
            Created notification.

        Raises
        ------
        UniqueError
            Raises if the notification already exists.

        """
        try:
            index = next(
                i
                for i in range(len(self._notifications))
                if (
                    self._notifications[i].event_id == notification.event_id
                    and self._notifications[i].author_id == notification.author_id
                )
            )
            if self._notifications[index].enabled:
                raise UniqueError("Notifications already exists")
            self._notifications[index].enabled = True
            if self._notifications[index].deleted_at is not None:
                self._notifications[index].created_at = datetime.utcnow()
                self._notifications[index].deleted_at = None
            return self._notifications[index]
        except StopIteration:
            notification.id = str(uuid4())
            notification.created_at = datetime.utcnow()
            notification.deleted_at = None
            notification.enabled = True
            self._notifications.append(notification)
            return notification

    async def update_notification(self, notification: Notification) -> Notification:
        """
        Updates notification with matching id or throws an exception.

        Parameters
        ----------
        notification : Notification
            Notification data.

        Returns
        -------
        Notification
            Notification with updated data.

        Raises
        ------
        ValueNotFoundError
            Can't update notification with provided data.

        """
        try:
            index = next(
                i
                for i in range(len(self._notifications))
                if self._notifications[i].id == notification.id
            )
            if self._notifications[index].author_id == notification.author_id:
                self._notifications[index] = notification
                return notification
            raise ValueNotFoundError("Notifications authors must be same")
        except StopIteration:
            raise ValueNotFoundError("Notification not found")

    async def delete_notification_by_id(self, notification_id: str) -> None:
        """
        Deletes notification with matching id or throws an exception.

        Parameters
        ----------
        notification_id : str
            Notification's id.

        Raises
        ------
        ValueNotFoundError
            Can't delete notification with provided data.

        """
        try:
            index = next(
                i
                for i in range(len(self._notifications))
                if self._notifications[i].id == notification_id
                and self._notifications[i].deleted_at is None
            )
            self._notifications[index].enabled = False
            self._notifications[index].deleted_at = datetime.utcnow()
        except StopIteration:
            raise ValueNotFoundError("Notification not found")

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
        ValueNotFoundError
            Can't delete notification with provided data.

        """
        indexes = tuple(
            i
            for i in range(len(self._notifications))
            if self._notifications[i].author_id == author_id
            and self._notifications[i].event_id in event_ids
            and self._notifications[i].deleted_at is None
        )
        if len(indexes) == 0:
            raise ValueNotFoundError("Notifications not found")
        for index in indexes:
            self._notifications[index].enabled = False
            self._notifications[index].deleted_at = datetime.utcnow()

    async def delete_notifications_by_author_id(self, author_id: str) -> None:
        """
        Delete notifications by author id.

        Parameters
        ----------
        author_id : str
            Event id.

        Raises
        ------
        ValueNotFoundError
            Can't delete notification with provided data.

        """
        indexes = tuple(
            i
            for i in range(len(self._notifications))
            if self._notifications[i].author_id == author_id
            and self._notifications[i].deleted_at is None
        )
        if len(indexes) == 0:
            raise ValueNotFoundError("Notifications not found")
        for index in indexes:
            self._notifications[index].enabled = False
            self._notifications[index].deleted_at = datetime.utcnow()

    async def delete_notifications_by_event_id(self, event_id: str) -> None:
        """
        Delete notifications by event id.

        Parameters
        ----------
        event_id : str
            Event id.

        Raises
        ------
        ValueNotFoundError
            Can't delete notification with provided data.

        """
        indexes = tuple(
            i
            for i in range(len(self._notifications))
            if self._notifications[i].event_id == event_id
            and self._notifications[i].deleted_at is None
        )
        if len(indexes) == 0:
            raise ValueNotFoundError("Notifications not found")
        for index in indexes:
            self._notifications[index].enabled = False
            self._notifications[index].deleted_at = datetime.utcnow()
