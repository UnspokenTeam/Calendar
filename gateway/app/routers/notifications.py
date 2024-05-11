"""Notification route"""
from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID, uuid4

from app.generated.notification_service.notification_service_pb2 import (
    DeleteNotificationByIdRequest as GrpcDeleteNotificationByIdRequest,
)
from app.generated.notification_service.notification_service_pb2 import (
    GetAllNotificationsRequest as GrpcGetAllNotificationsRequest,
)
from app.generated.notification_service.notification_service_pb2 import GrpcNotification
from app.generated.notification_service.notification_service_pb2 import ListOfNotifications as GrpcListOfNotifications
from app.generated.notification_service.notification_service_pb2 import (
    NotificationRequest as GrpcNotificationRequest,
)
from app.generated.notification_service.notification_service_pb2 import (
    NotificationRequestByNotificationId as GrpcGetNotificationByNotificationIdRequest,
)
from app.generated.notification_service.notification_service_pb2 import (
    NotificationsRequestByAuthorId as GrpcGetNotificationsByAuthorIdRequest,
)
from app.generated.user.user_pb2 import GrpcUser
from app.middleware import auth
from app.models import Notification, UserType
from app.models.Interval import Interval
from app.params import GrpcClientParams
from app.utils import check_permission_for_event, convert_event_start_to_notification_start
from app.validators.int_validators import int_not_equal_zero_validator

from errors import PermissionDeniedError

from fastapi import APIRouter, Depends
from pydantic import UUID4, AfterValidator, BaseModel, Field
from pytz import utc

router = APIRouter(prefix="/notifications", tags=["notifications"])


class ModifyNotificationRequest(BaseModel):
    """
    Modify notification request.

    Attributes
    ----------
    id : UUID4 | str
        Notification id
    event_id : UUID4 | str
        Event id
    author_id : UUID4 | str
        Author id
    enabled : bool
        Flag which is true if notification is enabled and false if disabled
    created_at : datetime
        Timestamp when notification was created
    deleted_at : Optional[datetime]
        Timestamp when notification was deleted
    delay : Interval
        Delay before event

    """
    id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    event_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    author_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    enabled: Annotated[bool, Field(True)]
    delay: Optional[Interval]
    created_at: datetime
    deleted_at: Optional[datetime] = None


@router.get("/{notification_id}")
async def get_notification_by_id(
        notification_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> Notification:
    """
    \f

    Fast api route to get notification by id

    Parameters
    ----------
    notification_id : UUID4 | str
        Notification id
    user : Annotated[GrpcUser, Depends(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    Returns
    -------
    Notification
        Notification object

    """
    notification_request: GrpcNotification = (
        grpc_clients
        .notification_service_client
        .request()
        .get_notification_by_notification_id(
            GrpcGetNotificationByNotificationIdRequest(
                notification_id=str(notification_id), requesting_user=user
            )
        )
    )

    return Notification.from_proto(notification_request)


@router.get("/admin/all/")
async def get_all_notifications(
        page: Annotated[int, Field(1, ge=1)],
        items_per_page: Annotated[int, Field(-1, ge=-1), AfterValidator(int_not_equal_zero_validator)],
        user: Annotated[GrpcUser, Depends(auth)],
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
    user : Annotated[GrpcUser, Depends(auth)]
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

    notifications_response: GrpcListOfNotifications = await (
        grpc_clients.notification_service_client.request().get_all_notifications(
            GrpcGetAllNotificationsRequest(
                page_number=page,
                items_per_page=items_per_page,
                requesting_user=user,
            )
        )
    )

    return [Notification.from_proto(notification) for notification in
            notifications_response.notifications]


@router.get("/my/")
async def get_my_notifications(
        page: Annotated[int, Field(1, ge=1)],
        items_per_page: Annotated[int, Field(-1, ge=-1), AfterValidator(int_not_equal_zero_validator)],
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
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
    user : Annotated[GrpcUser, Depends(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI
    start : Optional[datetime]
        Start date and time of the interval.
    end : Optional[datetime]
        End date and time of the interval.

    Returns
    -------
    List[Notification]
        User's notifications

    """
    request = GrpcGetNotificationsByAuthorIdRequest(
        author_id=user.id,
        requesting_user=user,
        items_per_page=items_per_page,
        page_number=page,
    )

    if start is not None:
        request.start.FromDatetime(start.astimezone(utc))

    if end is not None:
        request.end.FromDatetime(end.astimezone(utc))

    notifications_request: GrpcListOfNotifications = (
        grpc_clients
        .notification_service_client
        .request()
        .get_notifications_by_author_id(
            request
        )
    )

    return [
        Notification.from_proto(notification)
        for notification in notifications_request.notifications
    ]


@router.post("/")
async def create_notification(
        event_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
        delay: Optional[Interval],
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> Notification:
    """
    \f

    Fast api route to create notification

    Parameters
    ----------
    event_id : UUID4 | str
        Event id
    delay : Optional[Interval]
        Interval to calculate notification start
    user : Annotated[GrpcUser, Depends(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    Returns
    -------
    Notification
        New notification

    """
    event = check_permission_for_event(grpc_user=user, event_id=event_id, grpc_clients=grpc_clients)

    notification = Notification(
        id=uuid4(),
        event_id=event_id,
        author_id=user.id,
        created_at=datetime.now(),
        start=convert_event_start_to_notification_start(event.start.astimezone(tz=utc), delay),
        delay=delay,
        repeating_delay=event.repeating_delay,
        deleted_at=None,
        enabled=True,
    )

    notification_proto: GrpcNotification = grpc_clients.notification_service_client.request().create_notification(
        GrpcNotificationRequest(
            notification=notification.to_proto(), requesting_user=user
        )
    )

    return Notification.from_proto(notification_proto)


@router.put("/")
async def update_notification_as_author(
        modify_notification_request: ModifyNotificationRequest,
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> Notification:
    """
    \f

    Fast api route to update notification as author of notification

    Parameters
    ----------
    modify_notification_request : ModifyNotificationRequest
        New notification data
    user : Annotated[GrpcUser, Depends(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    Raises
    ------
    PermissionDeniedError
        Permission denied

    Returns
    -------
    Notification
        Updated notification

    """
    if str(modify_notification_request.author_id) != user.id:
        raise PermissionDeniedError("Permission denied")

    stored_notification_response: GrpcNotification = (
        grpc_clients.notification_service_client.request().get_notification_by_notification_id(
            GrpcGetNotificationByNotificationIdRequest(
                notification_id=str(modify_notification_request.id),
                requesting_user=user,
            )
        )
    )
    stored_notification = Notification.from_proto(stored_notification_response)

    event = check_permission_for_event(
        grpc_user=user,
        event_id=modify_notification_request.event_id,
        grpc_clients=grpc_clients
    )

    stored_notification.start = stored_notification.start.astimezone(tz=utc)

    if modify_notification_request.event_id != stored_notification.event_id:
        stored_notification.start = event.start.astimezone(tz=utc)

    stored_notification.start = convert_event_start_to_notification_start(
        stored_notification.start,
        modify_notification_request.delay
    )

    stored_notification.delay = modify_notification_request.delay
    stored_notification.event_id = modify_notification_request.event_id
    stored_notification.enabled = modify_notification_request.enabled

    notification_proto: GrpcNotification = grpc_clients.notification_service_client.request().update_notification(
        GrpcNotificationRequest(
            notification=stored_notification.to_proto(), requesting_user=user
        )
    )

    return Notification.from_proto(notification_proto)


@router.put("/admin/")
async def update_notification_as_admin(
        notification: Notification,
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> Notification:
    """
    \f

    Fast api route to update notification as admin

    Parameters
    ----------
    notification : Notification
        New notification data
    user : Annotated[GrpcUser, Depends(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    Raises
    ------
    PermissionDeniedError
        Permission denied

    Returns
    -------
    Notification
        Updated notification

    """
    if user.type != UserType.ADMIN:
        raise PermissionDeniedError("Permission denied")

    check_permission_for_event(grpc_user=user, event_id=notification.event_id, grpc_clients=grpc_clients)

    notification_proto: GrpcNotification = grpc_clients.notification_service_client.request().update_notification(
        GrpcNotificationRequest(
            notification=notification.to_proto(), requesting_user=user
        )
    )

    return Notification.from_proto(notification_proto)


@router.delete("/")
async def delete_notification(
        notification_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
        user: Annotated[GrpcUser, Depends(auth)],
        grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    \f

    Fast api route to delete notification

    Parameters
    ----------
    notification_id : UUID4 | str
        Notification id
    user : Annotated[GrpcUser, Depends(auth)]
        Authenticated user data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients which are injected by DI

    """
    grpc_clients.notification_service_client.request().delete_notification_by_id(
        GrpcDeleteNotificationByIdRequest(
            notification_id=str(notification_id), requesting_user=user
        )
    )
