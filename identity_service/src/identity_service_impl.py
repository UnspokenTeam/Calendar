"""Identity Service Controller"""
from typing import Tuple
from uuid import uuid4

import grpc

from errors.permission_denied import PermissionDeniedError
from errors.value_not_found_error import ValueNotFoundError
from src.models.user import User, UserType
from utils.encoder import Encoder
from utils.jwt_controller import JwtController, TokenType

from generated.identity_service.identity_service_pb2_grpc import IdentityServiceServicer as GrpcServicer
from google.protobuf.empty_pb2 import Empty
from repository.token_repository_interface import TokenRepositoryInterface
from repository.user_repository_interface import UserRepositoryInterface
import generated.identity_service.auth_pb2 as auth_proto
import generated.identity_service.delete_user_pb2 as delete_user_proto
import generated.identity_service.get_access_token_pb2 as get_access_token_proto
import generated.identity_service.get_user_pb2 as get_user_proto
import generated.identity_service.update_user_pb2 as update_user_proto


class IdentityServiceImpl(GrpcServicer):
    """
    Implementation of the Identity Service.

    Methods
    -------
    async login(request, context)
        Function that need to be bind to the server that returns access and
        refresh tokens for user if user data matches
    async register(request, context)
        Function that need to be bind to the server that creates user and returns access and refresh tokens for user
    async auth(request, context)
        Function that need to be bind to the server that returns user_id of
        currently signed in user by user access token
    async get_new_access_token(request, context)
        Function that need to be bind to the server that returns new access token for user if refresh token matches
    async get_user_by_id(request, context)
        Function that need to be bind to the server that returns user by its user_id
    async get_users_by_id(request, context)
        Function that need to be bind to the server that returns users that match provided user ids
    async update_user(request, context)
        Function that need to be bind to the server that updates user information
    async delete_user(request, context)
        Function that need to be bind to the server that deletes user with given user_id
    async logout(request, context)
        Function that need to be bind to the server that deletes refresh_token from database and logs the user off
    async get_all_users(request, context)
        Function that need to be bind to the server that returns all existing users
    async _generate_tokens(session_id, user_id)
        Generate access and refresh tokens

    """

    _user_repository: UserRepositoryInterface
    _token_repository: TokenRepositoryInterface
    _jwt_controller: JwtController
    _encoder: Encoder

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        token_repository: TokenRepositoryInterface,
    ) -> None:
        self._user_repository = user_repository
        self._token_repository = token_repository
        self._jwt_controller = JwtController()
        self._encoder = Encoder()

    async def login(
        self, request: auth_proto.LoginRequest, context: grpc.ServicerContext
    ) -> auth_proto.CredentialsResponse:
        """
        Log the user in and return credentials if user data matches

        Parameters
        ----------
        request : auth_proto.LoginRequest
            Login data
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        auth_proto.CredentialsResponse
            Response object with credentials

        """
        user = await self._user_repository.get_user_by_email(request.email)

        if not self._encoder.compare(
            password=request.password, hashed_password=user.password
        ):
            raise ValueNotFoundError("Invalid password")

        session_id = str(uuid4())
        access_token, refresh_token = self._generate_tokens(
            session_id=session_id, user_id=user.id
        )
        await self._token_repository.store_refresh_token(
            refresh_token=refresh_token, session_id=session_id, user_id=user.id
        )

        context.set_code(grpc.StatusCode.OK)
        return auth_proto.CredentialsResponse(
            data=auth_proto.LoginData(
                access_token=access_token, refresh_token=refresh_token
            ),
        )

    async def register(
        self, request: auth_proto.RegisterRequest, context: grpc.ServicerContext
    ) -> auth_proto.CredentialsResponse:
        """
        Creates user if user does not already exist

        Parameters
        ----------
        request : auth_proto.RegisterRequest
            Registration data
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        auth_proto.CredentialsResponse
            Response object with credentials

        """
        user = User.from_register_request(request)
        user.password = self._encoder.encode(user.password)

        user = await self._user_repository.create_user(user=user)

        session_id = str(uuid4())
        access_token, refresh_token = self._generate_tokens(
            session_id=session_id, user_id=user.id
        )
        await self._token_repository.store_refresh_token(
            refresh_token=refresh_token, session_id=session_id, user_id=user.id
        )

        context.set_code(grpc.StatusCode.OK)
        return auth_proto.CredentialsResponse(
            data=auth_proto.LoginData(
                access_token=access_token, refresh_token=refresh_token
            ),
        )

    async def auth(
        self, request: auth_proto.AccessToken, context: grpc.ServicerContext
    ) -> get_user_proto.UserResponse:
        """
        Authenticates user by his token and returns his ID

        Parameters
        ----------
        request : auth_proto.AccessToken
            Access token
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        get_user_proto.UserResponse
            Response object with user object

        """
        _, session_id = self._jwt_controller.decode(
            request.access_token, TokenType.ACCESS_TOKEN
        )
        user = await self._user_repository.get_user_by_session_id(session_id)
        context.set_code(grpc.StatusCode.OK)
        return get_user_proto.UserResponse(user=user.to_grpc_user())

    async def get_new_access_token(
        self,
        request: get_access_token_proto.GetNewAccessTokenRequest,
        context: grpc.ServicerContext,
    ) -> get_access_token_proto.GetNewAccessTokenResponse:
        """
        Generates new access_token for user to authenticate with

        Parameters
        ----------
        request : get_access_token_proto.GetNewAccessTokenRequest
            Refresh token
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        get_access_token_proto.GetNewAccessTokenResponse
            Response object with new access token

        """
        user_id, session_id = self._jwt_controller.decode(
            request.refresh_token, TokenType.REFRESH_TOKEN
        )
        await self._user_repository.get_user_by_session_id(session_id=session_id)
        access_token = self._jwt_controller.generate_access_token(
            user_id=user_id, session_id=session_id
        )
        context.set_code(grpc.StatusCode.OK)
        return get_access_token_proto.GetNewAccessTokenResponse(
            access_token=access_token
        )

    async def get_user_by_id(
        self, request: get_user_proto.UserByIdRequest, context: grpc.ServicerContext
    ) -> get_user_proto.UserResponse:
        """
        Gets user object that matches given ID

        Parameters
        ----------
        request : get_user_proto.UserByIdRequest
            User ID
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        get_user_proto.UserResponse
            Response object with public user data

        """
        user = await self._user_repository.get_user_by_id(request.user_id)
        context.set_code(grpc.StatusCode.OK)
        return get_user_proto.UserResponse(user=user.to_dict(exclude=["password"]))

    async def get_users_by_id(
        self, request: get_user_proto.UsersByIdRequest, context: grpc.ServicerContext
    ) -> get_user_proto.UsersResponse:
        """
        Gets user objects that matches given ids

        Parameters
        ----------
        request : get_user_proto.UsersByIdRequest
            User ids
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        get_user_proto.UsersResponse
            Response object with array of user data

        """
        users = await self._user_repository.get_users_by_ids(
            user_ids=list(request.id),
            page=request.page,
            items_per_page=request.items_per_page,
        )
        context.set_code(grpc.StatusCode.OK)
        return get_user_proto.UsersResponse(
            users=get_user_proto.ListOfUser(
                users=[user.to_grpc_user() for user in users]
            ),
        )

    async def get_all_users(
        self, request: get_user_proto.GetAllUsersRequest, context: grpc.ServicerContext
    ) -> get_user_proto.UsersResponse:
        """
        Get all existing users

        Parameters
        ----------
        request : get_user_proto.GetAllUsersRequest
            Requesting user's data
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        get_user_proto.UsersResponse
            Response object with array of user data4

        Raises
        ------
        PermissionDeniedError
            Permission denied

        """
        requesting_user = User.from_grpc_user(request.requested_user)
        if requesting_user.type != UserType.ADMIN:
            raise PermissionDeniedError("Permission denied")
        users = await self._user_repository.get_all_users(
            page=request.page, items_per_page=request.items_per_page
        )
        context.set_code(grpc.StatusCode.OK)
        return get_user_proto.UsersResponse(
            users=get_user_proto.ListOfUser(
                users=[user.to_grpc_user() for user in users]
            )
        )

    async def update_user(
        self,
        request: update_user_proto.UpdateUserRequest,
        context: grpc.ServicerContext,
    ) -> auth_proto.CredentialsResponse:
        """
        Updates user data

        Parameters
        ----------
        request : update_user_proto.UpdateUserRequest
            User data to be updated and current user data
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        auth_proto.CredentialsResponse
            Response with credentials for user

        Raises
        ------
        PermissionDeniedError
            Permission denied

        """
        user = User.from_update_grpc_user(grpc_user=request.new_user)
        requesting_user = User.from_grpc_user(request.requesting_user)
        db_user = await self._user_repository.get_user_by_id(user_id=requesting_user.id)

        if requesting_user.type != UserType.ADMIN and user.id != requesting_user.id:
            raise PermissionDeniedError("Permission denied")

        if self._encoder.compare(user.password, db_user.password):
            user.password = db_user.password
        else:
            user.password = self._encoder.encode(password=user.password)

        await self._user_repository.update_user(user=user)
        await self._token_repository.delete_all_refresh_tokens(user_id=user.id)

        session_id = str(uuid4())
        access_token, refresh_token = self._generate_tokens(
            session_id=session_id, user_id=user.id
        )
        await self._token_repository.store_refresh_token(
            refresh_token=refresh_token, session_id=session_id, user_id=user.id
        )

        context.set_code(grpc.StatusCode.OK)
        return auth_proto.CredentialsResponse(
            data=auth_proto.LoginData(
                access_token=access_token, refresh_token=refresh_token
            ),
        )

    async def delete_user(
        self,
        request: delete_user_proto.DeleteUserRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        """
        Deletes user with matching ID

        Parameters
        ----------
        request : delete_user_proto.DeleteUserRequest
            ID of user to be deleted and current user data
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        Empty
            Empty response

        Raises
        ------
        PermissionDeniedError
            Permission denied

        """
        requesting_user = User.from_grpc_user(request.requesting_user)
        user = await self._user_repository.get_user_by_id(request.user_id)
        if requesting_user.type != UserType.ADMIN and requesting_user.id != user.id:
            raise PermissionDeniedError("Permission denied")
        await self._token_repository.delete_all_refresh_tokens(user_id=request.user_id)
        await self._user_repository.delete_user(user_id=request.user_id)
        context.set_code(grpc.StatusCode.OK)
        return Empty()

    async def logout(
        self, request: auth_proto.AccessToken, context: grpc.ServicerContext
    ) -> Empty:
        """
        Logs out and deletes user's access token from database

        Parameters
        ----------
        request : auth_proto.AccessToken
            ID of user to be deleted
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        Empty
            Empty response

        """
        _, session_id = self._jwt_controller.decode(
            token=request.access_token, token_type=TokenType.ACCESS_TOKEN
        )
        await self._token_repository.delete_refresh_token(session_id=session_id)
        context.set_code(grpc.StatusCode.OK)
        return Empty()

    def _generate_tokens(self, session_id: str, user_id: str) -> Tuple[str, str]:
        """
        Generate access and refresh tokens

        Parameters
        ----------
        session_id : str
            Id of the session
        user_id : str
            Id of the user

        Returns
        -------
        Tuple[str, str]
            Access and refresh tokens

        """
        access_token = self._jwt_controller.generate_access_token(
            user_id=user_id, session_id=session_id
        )
        refresh_token = self._jwt_controller.generate_refresh_token(
            user_id=user_id, session_id=session_id
        )
        return access_token, refresh_token
