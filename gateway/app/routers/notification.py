"""Notification route"""
from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, Security
from pydantic import Field

from app.errors import PermissionDeniedError
from app.generated.event_service.event_service_pb2 import (
    EventRequestByEventId as GrpcGetEventByEventIdRequest,
)
from app.generated.notification_service.notification_service_pb2 import (
    DeleteNotificationByIdRequest as GrpcDeleteNotificationByIdRequest,
    NotificationRequest as GrpcNotificationRequest,
    NotificationRequestByNotificationId as GrpcGetNotificationByNotificationIdRequest,
    NotificationResponse as GrpcNotificationResponse,
    NotificationsRequestByAuthorId as GrpcGetNotificationsByAuthorIdRequest,
    NotificationsResponse as GrpcNotificationsResponse,
    GetAllNotificationsRequest as GrpcGetAllNotificationsRequest,
)
from app.generated.user.user_pb2 import GrpcUser
from app.middleware import auth
from app.models import Notification, UserType
from app.params import GrpcClientParams
from app.validators import str_special_characters_validator

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/{notification_id}")
async def get_notification_by_id(
        notification_id: Annotated[
            str, Field("", min_length=1), str_special_characters_validator
        ],
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> Notification:
    """
    \f
    Fast api route to get notification by id

    Parameters
    ----------
    notification_id : str
        Notification id
    user : Annotated[GrpcUser, Security(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    Returns
    -------
    Notification
        Notification object

    """
    notification_request: GrpcNotificationResponse = (
        grpc_clients
        .notification_service_client
        .request()
        .get_notification_by_notification_id(
            GrpcGetNotificationByNotificationIdRequest(
                notification_id=notification_id, requesting_user=user
            )
        )
    )

    return Notification.from_proto(notification_request.notification)


@router.get("/admin/all/")
async def get_all_notifications(
        page: int,
        items_per_page: int,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> List[Notification]:
    """
    \f
    Fast api route to get all notifications

    Parameters
    ----------
    page : int
        Page number
    items_per_page : int
        Number of items per page
    user : Annotated[GrpcUser, Security(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    Returns
    -------
    List[Notification]
        List of Notifications

    """
    if user.type != UserType.ADMIN:
        raise PermissionDeniedError("Permission denied")

    notifications_response: GrpcNotificationsResponse = await (
        grpc_clients.notification_service_client.request().get_all_notifications(
            GrpcGetAllNotificationsRequest(
                page_number=page,
                items_per_page=items_per_page,
                requesting_user=user,
            )
        )
    )

    return [Notification.from_proto(notification) for notification in
            notifications_response.notifications.notifications]


@router.get("/my/")
async def get_my_notifications(
        page: int,
        items_per_page: int,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> List[Notification]:
    """
    \f
    Fast api route to get all user's notifications
    Parameters
    ----------
    page : int
        Page number
    items_per_page : int
        Amount of numbers per page
    user : Annotated[GrpcUser, Security(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    Returns
    -------
    List[Notification]
        User's notifications

    """
    notifications_request: GrpcNotificationsResponse = (
        grpc_clients
        .notification_service_client
        .request()
        .get_notifications_by_author_id(
            GrpcGetNotificationsByAuthorIdRequest(
                author_id=user.id,
                requesting_user=user,
                items_per_page=items_per_page,
                page_number=page,
            )
        )
    )

    return [
        Notification.from_proto(notification)
        for notification in notifications_request.notifications.notifications
    ]


@router.post("/")
async def create_notification(
        event_id: Annotated[str, Field("", min_length=1), str_special_characters_validator],
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f
    Fast api route to create notification

    Parameters
    ----------
    event_id : str
        Event id
    user : Annotated[GrpcUser, Security(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    """

    _ = grpc_clients.event_service_client.request().get_event_by_event_id(
        GrpcGetEventByEventIdRequest(
            event_id=event_id,
            requesting_user=user
        )
    )

    notification = Notification(
        id="",
        event_id=event_id,
        author_id=user.id,
        created_at=datetime.now(),
        deleted_at=None,
        enabled=True,
    )

    grpc_clients.notification_service_client.request().create_notification(
        GrpcNotificationRequest(
            notification=notification.to_proto(), requesting_user=user
        )
    )


@router.put("/")
async def update_notification_as_author(
        notification: Notification,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f
    Fast api route to update notification as author of notification

    Parameters
    ----------
    notification : Notification
        New notification data
    user : Annotated[GrpcUser, Security(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    Raises
    ------
    PermissionDeniedError
        Permission denied

    """
    if notification.author_id != user.id:
        raise PermissionDeniedError

    stored_notification_response: GrpcNotificationResponse = (
        grpc_clients.notification_service_client.request().get_notification_by_notification_id(
            GrpcGetNotificationByNotificationIdRequest(
                notification_id=notification.id,
                requesting_user=user,
            )
        )
    )
    stored_notification = Notification.from_proto(stored_notification_response.notification)

    _ = grpc_clients.event_service_client.request().get_event_by_event_id(
        GrpcGetEventByEventIdRequest(
            event_id=notification.event_id,
            requesting_user=user
        )
    )

    notification.created_at = stored_notification.created_at
    notification.deleted_at = stored_notification.deleted_at

    grpc_clients.notification_service_client.request().update_notification(
        GrpcNotificationRequest(
            notification=notification.to_proto(), requesting_user=user
        )
    )


@router.put("/admin/")
async def update_notification(
        notification: Notification,
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f
    Fast api route to update notification as admin

    Parameters
    ----------
    notification : Notification
        New notification data
    user : Annotated[GrpcUser, Security(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    Raises
    ------
    PermissionDeniedError
        Permission denied

    """
    if user.type != UserType.ADMIN:
        raise PermissionDeniedError

    _ = grpc_clients.event_service_client.request().get_event_by_event_id(
        GrpcGetEventByEventIdRequest(
            event_id=notification.event_id,
            requesting_user=user
        )
    )

    grpc_clients.notification_service_client.request().update_notification(
        GrpcNotificationRequest(
            notification=notification.to_proto(), requesting_user=user
        )
    )


@router.delete("/")
async def delete_notification(
        notification_id: Annotated[
            str, Field("", min_length=1), str_special_characters_validator
        ],
        user: Annotated[GrpcUser, Security(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f
    Fast api route to delete notification

    Parameters
    ----------
    notification_id : str
        Notification id
    user : Annotated[GrpcUser, Security(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    """
    grpc_clients.notification_service_client.request().delete_notification_by_id(
        GrpcDeleteNotificationByIdRequest(
            notification_id=notification_id, requesting_user=user
        )
    )
