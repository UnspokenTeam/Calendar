"""Users route"""
from datetime import datetime
from typing import Annotated, List
from uuid import uuid4

from app.constants import MIN_PASSWORD_LENGTH, MIN_USERNAME_LENGTH
from app.errors import PermissionDeniedError
from app.generated.event_service.event_service_pb2 import (
    DeleteEventsByAuthorIdRequest as GrpcDeleteEventsByAuthorIdRequest,
)
from app.generated.identity_service.auth_pb2 import AccessToken as GrpcAccessToken
from app.generated.identity_service.auth_pb2 import (
    CredentialsResponse as GrpcCredentialsResponse,
)
from app.generated.identity_service.auth_pb2 import LoginRequest as GrpcLoginRequest
from app.generated.identity_service.delete_user_pb2 import (
    DeleteUserRequest as GrpcDeleteUserRequest,
)
from app.generated.identity_service.get_access_token_pb2 import (
    GetNewAccessTokenRequest as GrpcGetNewAccessTokenRequest,
)
from app.generated.identity_service.get_access_token_pb2 import (
    GetNewAccessTokenResponse as GrpcGetNewAccessTokenResponse,
)
from app.generated.identity_service.get_user_pb2 import (
    GetAllUsersRequest as GrpcGetAllUsersRequest,
)
from app.generated.identity_service.get_user_pb2 import ListOfUser as GrpcListOfUser
from app.generated.identity_service.get_user_pb2 import (
    UserByIdRequest as GrpcGetUserByIdRequest,
)
from app.generated.identity_service.update_user_pb2 import (
    UpdateUserRequest as GrpcUpdateUserRequest,
)
from app.generated.invite_service.invite_service_pb2 import (
    DeleteInvitesByAuthorIdRequest as GrpcDeleteInvitesByAuthorId,
)
from app.generated.notification_service.notification_service_pb2 import (
    DeleteNotificationsByAuthorIdRequest as GrpcDeleteNotificationsByAuthorIdRequest,
)
from app.generated.user.user_pb2 import GrpcUser, GrpcUserType
from app.middleware.auth import api_key_header, auth
from app.models import User, UserType
from app.params import GrpcClientParams
from app.validators import str_special_characters_validator

from fastapi import APIRouter, Depends, Security
from pydantic import AfterValidator, BaseModel, EmailStr, Field

router = APIRouter(prefix="/users", tags=["users"])


class RegisterRequest(BaseModel):
    """
    Register request model

    Attributes
    ----------
    username : str
        User's username
    email : EmailStr
        User's email
    password : str
        User's password

    """

    username: Annotated[
        str,
        Field("", min_length=MIN_USERNAME_LENGTH),
        AfterValidator(str_special_characters_validator),
    ]
    email: EmailStr
    password: Annotated[
        str,
        Field("", min_length=MIN_PASSWORD_LENGTH),
        AfterValidator(str_special_characters_validator),
    ]


class LoginRequest(BaseModel):
    """
    Login request model

    Attributes
    ----------
    email : EmailStr
        User's email
    password : str
        User's password

    """

    email: EmailStr
    password: Annotated[
        str,
        Field("", min_length=MIN_PASSWORD_LENGTH),
        AfterValidator(str_special_characters_validator),
    ]


class CredentialsResponse(BaseModel):
    """
    Credentials response model

    Attributes
    ----------
    access_token : str
        User's access token
    refresh_token : str
        User's refresh token

    """

    access_token: str
    refresh_token: str
    user: User


@router.get("/me", response_model_exclude={"password"})
async def get_current_user_info(user: Annotated[GrpcUser, Security(auth)]) -> User:
    """
    Fast api route to get current user info

    Parameters
    ----------
    user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format

    Returns
    -------
    User
        Current user's data

    """
    return User.from_proto(user)


@router.get("/all", response_model_exclude={"password"})
async def get_all_users(
    items_per_page: int,
    page: int,
    user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> List[User]:
    """
    Fast api route to get all users

    Parameters
    ----------
    items_per_page : int
        Number of items per page
    page : int
        Page number
    user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Returns
    -------
    List[User]
        All users

    """
    if user.type != GrpcUserType.USER:
        raise PermissionDeniedError("Permission denied")

    response: GrpcListOfUser = (
        grpc_clients.identity_service_client.request().get_all_users(
            GrpcGetAllUsersRequest(
                page=page, items_per_page=items_per_page, requested_user=user
            )
        )
    )

    return [User.from_proto(grpc_user) for grpc_user in response.users]


@router.get("/{user_id}", response_model_exclude={"password", "email"})
async def get_user(
    user_id: Annotated[
        str,
        Field("", min_length=1),
        AfterValidator(str_special_characters_validator),
    ],
    _: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> User:
    """
    Fast api route to get user by id

    Parameters
    ----------
    user_id : str
        User's id
    _ : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients
        Grpc clients injected by DI

    Returns
    -------
    User
        User object

    """
    user: GrpcUser = (
        grpc_clients.identity_service_client.request().get_user_by_id(
            GrpcGetUserByIdRequest(user_id=user_id)
        )
    )
    return User.from_proto(user)


@router.post("/register")
async def register_user(
    register_request: RegisterRequest,
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> CredentialsResponse:
    """
    Fast api route to register user

    Parameters
    ----------
    register_request : RegisterRequest
        Register request data
    grpc_clients
        Grpc clients injected by DI

    Returns
    -------
    CredentialsResponse
        Access and refresh token

    """
    user = User(
        id=uuid4(),
        username=register_request.username,
        email=register_request.email,
        password=register_request.password,
        type=UserType.USER,
        created_at=datetime.now(),
        suspended_at=None,
    )

    credentials: GrpcCredentialsResponse = (
        grpc_clients.identity_service_client.request().register(
            user.to_modify_proto()
        )
    )

    return CredentialsResponse(
        access_token=credentials.data.access_token,
        refresh_token=credentials.data.refresh_token,
        user=User.from_proto(credentials.user)
    )


@router.post("/login")
async def login(
    login_request: LoginRequest,
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> CredentialsResponse:
    """
    Fast api route to log in user

    Parameters
    ----------
    login_request : LoginRequest
        Login request data
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Returns
    -------
    CredentialsResponse
        Access and refresh token

    """
    credentials: GrpcCredentialsResponse = (
        grpc_clients.identity_service_client.request().login(
            GrpcLoginRequest(email=login_request.email, password=login_request.password)
        )
    )
    return CredentialsResponse(
        access_token=credentials.data.access_token,
        refresh_token=credentials.data.refresh_token,
        user=User.from_proto(credentials.user)
    )


@router.post("/logout")
async def logout(
    _: Annotated[GrpcUser, Security(auth)],
    access_token: Annotated[str, api_key_header],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    Fast api route to log out user

    Parameters
    ----------
    _ : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    access_token : str
        Access token
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    """
    grpc_clients.identity_service_client.request().logout(
        GrpcAccessToken(access_token=access_token)
    )
    return


@router.get("/access_token/")
async def get_new_access_token(
    refresh_token: Annotated[
        str,
        Field("", min_length=1),
    ],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> str:
    """
    Fast api route to get new access token

    Parameters
    ----------
    refresh_token : str
        User's refresh token
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    Returns
    -------
    str
        New access token

    """
    access_token_request: GrpcGetNewAccessTokenResponse = (
        grpc_clients.identity_service_client.request().get_new_access_token(
            GrpcGetNewAccessTokenRequest(refresh_token=refresh_token)
        )
    )
    return str(access_token_request.access_token)


@router.put("/")
async def update_user(
    grpc_user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
    user_to_update: User,
) -> CredentialsResponse:
    """
    Fast api route to update user

    Parameters
    ----------
    grpc_user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI
    user_to_update
        New user data

    Returns
    -------
    User
        New user data

    """
    user = User.from_proto(grpc_user)

    if user.type == UserType.USER and (
        user_to_update.id != user.id
        or user_to_update.type == UserType.ADMIN
        or user_to_update.suspended_at != user.suspended_at
        or user_to_update.created_at != user.created_at
    ):
        raise ValueError

    response: GrpcCredentialsResponse = grpc_clients.identity_service_client.request().update_user(
        GrpcUpdateUserRequest(
            requesting_user=grpc_user,
            new_user=user_to_update.to_update_proto(),
        )
    )

    return CredentialsResponse(
        access_token=response.data.access_token,
        refresh_token=response.data.refresh_token,
        user=User.from_proto(response.user)
    )


@router.delete("/")
async def delete_user(
    grpc_user: Annotated[GrpcUser, Security(auth)],
    grpc_clients: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
) -> None:
    """
    Fast api route to delete user

    Parameters
    ----------
    grpc_user : Annotated[GrpcUser, Security(auth)]
        Authorized user's data in proto format
    grpc_clients : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI

    """
    grpc_clients.notification_service_client.request().delete_notifications_by_author_id(
        GrpcDeleteNotificationsByAuthorIdRequest(
            author_id=grpc_user.id,
            requesting_user=grpc_user
        )
    )

    grpc_clients.invite_service_client.request().delete_invites_by_author_id(
        GrpcDeleteInvitesByAuthorId(
            author_id=grpc_user.id,
            requesting_user=grpc_user
        )
    )

    grpc_clients.event_service_client.request().delete_events_by_author_id(
        GrpcDeleteEventsByAuthorIdRequest(
            author_id=grpc_user.id,
            requesting_user=grpc_user
        )
    )

    grpc_clients.identity_service_client.request().delete_user(
        GrpcDeleteUserRequest(user_id=grpc_user.id, requesting_user=grpc_user)
    )
