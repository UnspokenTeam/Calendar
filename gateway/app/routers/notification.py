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
    NotificationRequestByNotificationId as GrpcNotificationByNotificationIdRequest,
    NotificationResponse as GrpcNotificationResponse,
    NotificationsRequestByAuthorId as GrpcNotificationsByAuthorIdRequest,
    NotificationsResponse as GrpcNotificationsResponse,
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
            GrpcNotificationByNotificationIdRequest(
                notification_id=notification_id, requesting_user=user
            )
        )
    )

    return Notification.from_proto(notification_request.notification)


@router.get("/my")
async def get_my_notifications(
    page: int,
    items_per_page: int,
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> List[Notification]:
    """
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
            GrpcNotificationsByAuthorIdRequest(
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
async def update_notification(
    notification: Notification,
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    Fast api route to update notification

    Parameters
    ----------
    notification : Notification
        New notification data
    user : Annotated[GrpcUser, Security(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    """
    if notification.author_id != user.id and user.type != UserType.ADMIN:
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
