"""Notification Service Controller."""

from datetime import datetime

import grpc

from errors import PermissionDeniedError
from src.generated.notification_service.notification_service_pb2_grpc import (
    NotificationServiceServicer as GrpcServicer,
)
from src.generated.user.user_pb2 import GrpcUserType
from src.models.notification import Notification
from src.repository.notification_repository_interface import (
    NotificationRepositoryInterface,
)
import src.generated.notification_service.notification_service_pb2 as proto

from google.protobuf.empty_pb2 import Empty


class NotificationServiceImpl(GrpcServicer):
    """
    Implementation of the Notification Service.

    Attributes
    ----------
    _notification_repository : NotificationRepositoryInterface
        The notification repository interface attribute.

    Methods
    -------
    async get_notifications_by_author_id(request, context)
        Function that need to be bind to the server that returns notifications list.
    async get_notifications_by_event_id(request, context)
        Function that need to be bind to the server that returns notifications list.
    async get_notification_by_event_and_author_ids(request, context)
        Function that need to be bind to the server that returns notifications list.
    async get_notification_by_notification_id(request, context)
        Function that need to be bind to the server that returns notification.
    async get_notifications_by_notifications_ids(request, context)
        Function that need to be bind to the server that returns notifications list.
    async get_all_notifications(request, context)
        Function that need to be bind to the server that returns all notifications in list.
    async create_notification(request, context)
        Function that need to be bind to the server that creates the notification.
    async update_notification(request, context)
        Function that need to be bind to the server that updates the notification.
    async delete_notification_by_id(request, context)
        Function that need to be bind to the server that deletes the notification.
    async delete_notifications_by_events_and_author_ids(request, context)
        Function that need to be bind to the server that deletes notifications by events and author ids.
    async delete_notifications_by_author_id(request, context)
        Function that need to be bind to the server that deletes notifications by author id.
    async delete_notifications_by_event_id(request, context)
        Function that need to be bind to the server that deletes notifications by event id.

    """

    _notification_repository: NotificationRepositoryInterface

    def __init__(
        self,
        notification_repository: NotificationRepositoryInterface,
    ) -> None:
        self._notification_repository = notification_repository

    async def get_notifications_by_author_id(
        self,
        request: proto.NotificationsRequestByAuthorId,
        context: grpc.ServicerContext,
    ) -> proto.ListOfNotifications:
        """
        Get notifications by author id.

        Parameters
        ----------
        request : proto.NotificationsRequestByAuthorId
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.ListOfNotifications
            Response object for several notifications.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != request.author_id
        ):
            raise PermissionDeniedError("Permission denied")
        notifications = (
            await self._notification_repository.get_notifications_by_author_id(
                author_id=request.author_id,
                page_number=request.page_number,
                items_per_page=request.items_per_page,
                start=datetime.utcfromtimestamp(
                    request.start.seconds + request.start.nanos / 1e9
                )
                if request.WhichOneof("optional_start") is not None
                else None,
                end=datetime.utcfromtimestamp(
                    request.end.seconds + request.end.nanos / 1e9
                )
                if request.WhichOneof("optional_end") is not None
                else None,
            )
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfNotifications(
            notifications=[
                notification.to_grpc_notification() for notification in notifications
            ]
        )

    async def get_notifications_by_event_id(
        self,
        request: proto.NotificationsRequestByEventId,
        context: grpc.ServicerContext,
    ) -> proto.ListOfNotifications:
        """
        Get notifications by event id.

        Parameters
        ----------
        request : proto.NotificationsRequestByEventId
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.ListOfNotifications
            Response object for several notifications.

        """
        notifications = (
            await self._notification_repository.get_notifications_by_event_id(
                event_id=request.event_id,
                page_number=request.page_number,
                items_per_page=request.items_per_page,
            )
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfNotifications(
            notifications=[
                notification.to_grpc_notification() for notification in notifications
            ]
        )

    async def get_notification_by_event_and_author_ids(
        self,
        request: proto.NotificationRequestByEventAndAuthorIds,
        context: grpc.ServicerContext,
    ) -> proto.GrpcNotification:
        """
        Get notification by event and author ids.

        Parameters
        ----------
        request : proto.NotificationRequestByEventAndAuthorIds
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.GrpcNotification
            Response object for notification response.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != request.author_id
        ):
            raise PermissionDeniedError("Permission denied")
        notification = await self._notification_repository.get_notification_by_event_and_author_ids(
            event_id=request.event_id,
            author_id=request.author_id,
        )
        context.set_code(grpc.StatusCode.OK)
        return notification.to_grpc_notification()

    async def get_notification_by_notification_id(
        self,
        request: proto.NotificationRequestByNotificationId,
        context: grpc.ServicerContext,
    ) -> proto.GrpcNotification:
        """
        Get notification by notification id.

        Parameters
        ----------
        request : proto.NotificationRequestByNotificationId
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.GrpcNotification
            Response object for notification response.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        notification = (
            await self._notification_repository.get_notification_by_notification_id(
                notification_id=request.notification_id
            )
        )
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != notification.author_id
        ):
            raise PermissionDeniedError("Permission denied")
        context.set_code(grpc.StatusCode.OK)
        return notification.to_grpc_notification()

    async def get_notifications_by_notifications_ids(
        self,
        request: proto.NotificationsRequestByNotificationsIds,
        context: grpc.ServicerContext,
    ) -> proto.ListOfNotifications:
        """
        Get notifications by notifications ids.

        Parameters
        ----------
        request : proto.NotificationsRequestByNotificationsIds
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.ListOfNotifications
            Response object for several notifications.

        """
        notifications = (
            await self._notification_repository.get_notifications_by_notifications_ids(
                notifications_ids=list(request.notifications_ids.ids),
                page_number=request.page_number,
                items_per_page=request.items_per_page,
            )
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfNotifications(
            notifications=[
                notification.to_grpc_notification() for notification in notifications
            ]
        )

    async def get_all_notifications(
        self, request: proto.GetAllNotificationsRequest, context: grpc.ServicerContext
    ) -> proto.ListOfNotifications:
        """
        Get all notifications.

        Parameters
        ----------
        request : proto.RequestingUser
            Request data.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.ListOfNotifications
            Response object for several notifications.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if request.requesting_user.type != GrpcUserType.ADMIN:
            raise PermissionDeniedError("Permission denied")
        notifications = await self._notification_repository.get_all_notifications(
            page_number=request.page_number, items_per_page=request.items_per_page
        )
        context.set_code(grpc.StatusCode.OK)
        return proto.ListOfNotifications(
            notifications=[
                notification.to_grpc_notification() for notification in notifications
            ]
        )

    async def create_notification(
        self, request: proto.NotificationRequest, context: grpc.ServicerContext
    ) -> proto.GrpcNotification:
        """
        Create notification.

        Parameters
        ----------
        request : proto.NotificationRequest
            Request data containing GrpcNotification.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.GrpcNotification
            Response object for notification response.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        notification = Notification.from_grpc_notification(request.notification)
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != notification.author_id
        ):
            raise PermissionDeniedError("Permission denied")
        notification = await self._notification_repository.create_notification(
            notification=notification
        )
        context.set_code(grpc.StatusCode.OK)
        return notification.to_grpc_notification()

    async def update_notification(
        self, request: proto.NotificationRequest, context: grpc.ServicerContext
    ) -> proto.GrpcNotification:
        """
        Update notification.

        Parameters
        ----------
        request : proto.NotificationRequest
            Request data containing GrpcNotification.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        proto.GrpcNotification
            Response object for notification response.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != request.notification.author_id
        ):
            raise PermissionDeniedError("Permission denied")
        notification = Notification.from_grpc_notification(request.notification)
        notification = await self._notification_repository.update_notification(
            notification=notification
        )
        context.set_code(grpc.StatusCode.OK)
        return notification.to_grpc_notification()

    async def delete_notification_by_id(
        self,
        request: proto.DeleteNotificationByIdRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        """
        Delete notification.

        Parameters
        ----------
        request : proto.DeleteNotificationByIdRequest
            Request data containing notification ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        Empty
            Empty response object.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        notification = (
            await self._notification_repository.get_notification_by_notification_id(
                request.notification_id
            )
        )
        if (
            request.requesting_user.type != GrpcUserType.ADMIN
            and request.requesting_user.id != notification.author_id
        ):
            raise PermissionDeniedError("Permission denied")
        await self._notification_repository.delete_notification_by_id(
            notification_id=request.notification_id
        )
        context.set_code(grpc.StatusCode.OK)
        return Empty()

    async def delete_notifications_by_events_and_author_ids(
        self,
        request: proto.DeleteNotificationsByEventsAndAuthorIdsRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        """
        Delete notifications by events and author id.

        Parameters
        ----------
        request : proto.DeleteNotificationsByEventsAndAuthorIdsRequest
            Request data containing events IDs and author ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        Empty
            Empty response object.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if (
            request.requesting_user.id != request.author_id
            and request.requesting_user.type != GrpcUserType.ADMIN
        ):
            raise PermissionDeniedError("Permission denied")
        await self._notification_repository.delete_notifications_by_events_and_author_ids(
            event_ids=list(request.event_ids.ids), author_id=request.author_id
        )
        context.set_code(grpc.StatusCode.OK)
        return Empty()

    async def delete_notifications_by_author_id(
        self,
        request: proto.DeleteNotificationsByAuthorIdRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        """
        Delete notifications by author id.

        Parameters
        ----------
        request : proto.DeleteNotificationsByAuthorIdRequest
            Request data containing author ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        Empty
            Empty response object.

        Raises
        ------
        PermissionDeniedError
            Raises when user dont has enough access.

        """
        if (
            request.requesting_user.id != request.author_id
            and request.requesting_user.type != GrpcUserType.ADMIN
        ):
            raise PermissionDeniedError("Permission denied")
        await self._notification_repository.delete_notifications_by_author_id(
            author_id=request.author_id
        )
        context.set_code(grpc.StatusCode.OK)
        return Empty()

    async def delete_notifications_by_event_id(
        self,
        request: proto.DeleteNotificationsByEventIdRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        """
        Delete notifications by event id.

        Parameters
        ----------
        request : proto.DeleteNotificationsByAuthorIdRequest
            Request data containing event ID.
        context : grpc.ServicerContext
            Request context.

        Returns
        -------
        Empty
            Empty response object.

        """
        await self._notification_repository.delete_notifications_by_event_id(
            event_id=request.event_id
        )
        context.set_code(grpc.StatusCode.OK)
        return Empty()
