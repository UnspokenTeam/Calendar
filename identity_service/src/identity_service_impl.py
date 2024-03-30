"""Identity Service Controller"""
from typing import Tuple
from uuid import uuid4

import grpc

import prisma.errors

from errors.InvalidTokenError import InvalidTokenError
from errors.unique_error import UniqueError
from errors.value_not_found_error import ValueNotFoundError
from src.models.user import User
from utils.encoder import Encoder
from utils.jwt_controller import JwtController, TokenType

from generated.identity_service_pb2_grpc import IdentityServiceServicer as GrpcServicer
from google.protobuf.empty_pb2 import Empty
from repository.token_repository_interface import TokenRepositoryInterface
from repository.user_repository_interface import UserRepositoryInterface
import generated.auth_pb2 as auth_proto
import generated.delete_user_pb2 as delete_user_proto
import generated.get_access_token_pb2 as get_access_token_proto
import generated.get_user_pb2 as get_user_proto
import generated.identity_service_pb2 as requests_proto
import generated.update_user_pb2 as update_user_proto


class IdentityServiceImpl(GrpcServicer):
    """
    Implementation of the Identity Service.

    Methods
    -------
    login(request, context)
        Function that need to be bind to the server that returns access and
        refresh tokens for user if user data matches
    register(request, context)
        Function that need to be bind to the server that creates user and returns access and refresh tokens for user
    auth(request, context)
        Function that need to be bind to the server that returns user_id of
        currently signed in user by user access token
    get_new_access_token(request, context)
        Function that need to be bind to the server that returns new access token for user if refresh token matches
    get_user_by_id(request, context)
        Function that need to be bind to the server that returns user by its user_id
    get_users_by_id(request, context)
        Function that need to be bind to the server that returns users that match provided user ids
    update_user(request, context)
        Function that need to be bind to the server that updates user information
    delete_user(request, context)
        Function that need to be bind to the server that deletes user with given user_id
    logout(request, context)
        Function that need to be bind to the server that deletes refresh_token from database and logs the user off

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
        request : LoginRequest
            Login data
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        CredentialsResponse
            Response object with credentials

        """
        try:
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
                status_code=200,
                data=auth_proto.LoginData(
                    access_token=access_token, refresh_token=refresh_token
                ),
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return auth_proto.CredentialsResponse(
                status_code=403, message="Email or password are incorrect"
            )
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return auth_proto.CredentialsResponse(
                status_code=500, message="Internal server error"
            )

    async def register(
        self, request: auth_proto.RegisterRequest, context: grpc.ServicerContext
    ) -> auth_proto.CredentialsResponse:
        """
        Creates user if user does not already exist

        Parameters
        ----------
        request : RegisterRequest
            Registration data
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        CredentialsResponse
            Response object with credentials

        """
        try:
            user = User.from_register_request(request)
            user.password = self._encoder.encode(user.password)

            await self._user_repository.create_user(user=user)

            session_id = str(uuid4())
            access_token, refresh_token = self._generate_tokens(
                session_id=session_id, user_id=user.id
            )
            await self._token_repository.store_refresh_token(
                refresh_token=refresh_token, session_id=session_id, user_id=user.id
            )

            context.set_code(grpc.StatusCode.OK)
            return auth_proto.CredentialsResponse(
                status_code=200,
                data=auth_proto.LoginData(
                    access_token=access_token, refresh_token=refresh_token
                ),
            )
        except UniqueError:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return auth_proto.CredentialsResponse(
                status_code=400, message="User with this data already exists"
            )
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return auth_proto.CredentialsResponse(
                status_code=500, message="Internal server error"
            )

    async def auth(
        self, request: auth_proto.AccessToken, context: grpc.ServicerContext
    ) -> get_user_proto.UserResponse:
        """
        Authenticates user by his token and returns his ID

        Parameters
        ----------
        request : AccessToken
            Access token
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        AuthResponse
            Response object with ID of currently signed in user

        """
        try:
            _, session_id = self._jwt_controller.decode(
                request.access_token, TokenType.ACCESS_TOKEN
            )
            user = await self._user_repository.get_user_by_session_id(session_id)
            context.set_code(grpc.StatusCode.OK)
            return get_user_proto.UserResponse(
                status_code=200, user=user.to_grpc_user()
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return get_user_proto.UserResponse(status_code=403, message="Unauthorized")
        except InvalidTokenError:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return get_user_proto.UserResponse(status_code=403, message="Unauthorized")
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return get_user_proto.UserResponse(
                status_code=500, message="Internal server error"
            )

    async def get_new_access_token(
        self,
        request: get_access_token_proto.GetNewAccessTokenRequest,
        context: grpc.ServicerContext,
    ) -> get_access_token_proto.GetNewAccessTokenResponse:
        """
        Generates new access_token for user to authenticate with

        Parameters
        ----------
        request : GetNewAccessTokenRequest
            Refresh token
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        GetNewAccessTokenResponse
            Response object with new access token

        """
        try:
            user_id, session_id = self._jwt_controller.decode(
                request.refresh_token, TokenType.ACCESS_TOKEN
            )
            _ = await self._user_repository.get_user_by_session_id(session_id=session_id)
            access_token = self._jwt_controller.generate_access_token(
                user_id=user_id, session_id=session_id
            )
            context.set_code(grpc.StatusCode.OK)
            return get_access_token_proto.GetNewAccessTokenResponse(
                status_code=200, access_token=access_token
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return get_access_token_proto.GetNewAccessTokenResponse(
                status_code=403, message="Unauthorized"
            )
        except InvalidTokenError:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return get_access_token_proto.GetNewAccessTokenResponse(
                status_code=403, message="Unauthorized"
            )
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return get_access_token_proto.GetNewAccessTokenResponse(
                status_code=500, message="Internal server error"
            )

    async def get_user_by_id(
        self, request: get_user_proto.UserByIdRequest, context: grpc.ServicerContext
    ) -> get_user_proto.UserResponse:
        """
        Gets user object that matches given ID

        Parameters
        ----------
        request : UserByIdRequest
            User ID
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        UserResponse
            Response object with public user data

        """
        try:
            user = await self._user_repository.get_user_by_id(request.user_id)
            context.set_code(grpc.StatusCode.OK)
            return get_user_proto.UserResponse(
                status_code=200, user=user.to_dict(exclude=["password"])
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return get_user_proto.UserResponse(
                status_code=404, message="User not found"
            )
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return get_user_proto.UserResponse(
                status_code=500, message="Internal server error"
            )

    async def get_users_by_id(
        self, request: get_user_proto.UsersByIdRequest, context: grpc.ServicerContext
    ) -> get_user_proto.UsersResponse:
        """
        Gets user objects that matches given ids

        Parameters
        ----------
        request : UsersByIdRequest
            User ids
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        UsersResponse
            Response object with array of public user data

        """
        try:
            users = await self._user_repository.get_users_by_ids(list(request.id))
            context.set_code(grpc.StatusCode.OK)
            return get_user_proto.UsersResponse(
                status_code=200,
                users=get_user_proto.ListOfUser(
                    users=[user.to_grpc_user() for user in users]
                ),
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return get_user_proto.UsersResponse(
                status_code=404, message="Users not found"
            )
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return get_user_proto.UsersResponse(
                status_code=500, message="Internal server error"
            )

    async def get_all_users(self, _: Empty, context: grpc.ServicerContext) -> get_user_proto.UsersResponse:
        try:
            users = await self._user_repository.get_all_users()
            context.set_code(grpc.StatusCode.OK)
            return get_user_proto.UsersResponse(
                users=get_user_proto.ListOfUser(
                    users=[user.to_grpc_user() for user in users]
                )
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return get_user_proto.UsersResponse(
                status_code=404, message="Users not found"
            )
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return get_user_proto.UsersResponse(
                status_code=500, message="Internal server error"
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
        request : UpdateUserRequest
            User data to be updated and current user id
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        BaseResponse
            Base response with status code and optional message

        """
        try:
            user = User.from_update_grpc_user(grpc_user=request.new_user)
            db_user = await self._user_repository.get_user_by_id(user_id=user.id)

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
                status_code=200,
                data=auth_proto.LoginData(
                    access_token=access_token, refresh_token=refresh_token
                ),
            )
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return auth_proto.CredentialsResponse(
                status_code=404, message="User with provided id does not exist"
            )
        except UniqueError:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return auth_proto.CredentialsResponse(
                status_code=400, message="User with provided data already exists"
            )
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return auth_proto.CredentialsResponse(
                status_code=500, message="Internal server error"
            )

    async def delete_user(
        self,
        request: delete_user_proto.DeleteUserRequest,
        context: grpc.ServicerContext,
    ) -> requests_proto.BaseResponse:
        """
        Deletes user with matching ID

        Parameters
        ----------
        request : DeleteUserRequest
            ID of user to be deleted
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        BaseResponse
            Base response with status code and optional message

        """
        try:
            await self._token_repository.delete_all_refresh_tokens(
                user_id=request.user_id
            )
            await self._user_repository.delete_user(user_id=request.user_id)
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return requests_proto.BaseResponse(
                status_code=404, message="Users not found"
            )
        except prisma.errors.PrismaError:
            context.set_code(grpc.StatusCode.INTERNAL)
            return requests_proto.BaseResponse(
                status_code=500, message="Internal server error"
            )

        context.set_code(grpc.StatusCode.OK)
        return requests_proto.BaseResponse(status_code=200)

    async def logout(
        self, request: auth_proto.AccessToken, context: grpc.ServicerContext
    ) -> requests_proto.BaseResponse:
        """
        Logs out and deletes user's access token from database

        Parameters
        ----------
        request : AccessToken
            ID of user to be deleted
        context : grpc.ServicerContext
            Request context

        Returns
        -------
        BaseResponse
            Base response with status code and optional message

        """
        try:
            _, session_id = self._jwt_controller.decode(
                token=request.access_token, token_type=TokenType.ACCESS_TOKEN
            )
            await self._token_repository.delete_refresh_token(session_id=session_id)
            context.set_code(grpc.StatusCode.OK)
            return requests_proto.BaseResponse(status_code=200)
        except ValueNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return requests_proto.BaseResponse(
                status_code=404, message="Users not found"
            )

    def _generate_tokens(self, session_id: str, user_id: str) -> Tuple[str, str]:
        access_token = self._jwt_controller.generate_access_token(
            user_id=user_id, session_id=session_id
        )
        refresh_token = self._jwt_controller.generate_refresh_token(
            user_id=user_id, session_id=session_id
        )
        return access_token, refresh_token
