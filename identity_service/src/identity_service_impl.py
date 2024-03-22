"""Identity Service Controller"""
import grpc

from generated.identity_service_pb2_grpc import IdentityServiceServicer as GrpcServicer
import generated.identity_service_pb2 as requests_proto
import generated.auth_pb2 as auth_proto
import generated.get_access_token_pb2 as get_access_token_proto
import generated.get_user_pb2 as get_user_proto
import generated.update_user_pb2 as update_user_proto
import generated.delete_user_pb2 as delete_user_proto


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

    def login(
        self, request: auth_proto.LoginRequest, context: grpc.ServicerContext
    ) -> auth_proto.CredentialsResponse:
        """
        Log the user in and return credentials if user data matches

        Parameters
        ----------
        request: LoginRequest
            Login data
        context: grpc.ServicerContext
            Request context

        Returns
        -------
        CredentialsResponse
            Response object with credentials
        """
        if request.username == "username" and request.password == "password":
            return auth_proto.CredentialsResponse(
                status_code=200,
                data=auth_proto.LoginData(
                    refresh_token="refresh", access_token="access"
                ),
            )

        return auth_proto.CredentialsResponse(
            status_code=200,
        )

    def register(
        self, request: auth_proto.RegisterRequest, context: grpc.ServicerContext
    ) -> auth_proto.CredentialsResponse:
        """
        Creates user if user does not already exist

        Parameters
        ----------
        request: RegisterRequest
            Registration data
        context: grpc.ServicerContext
            Request context

        Returns
        -------
        CredentialsResponse
            Response object with credentials
        """
        pass

    def auth(
        self, request: auth_proto.AccessToken, context: grpc.ServicerContext
    ) -> auth_proto.AuthResponse:
        """
        Authenticates user by his token and returns his ID

        Parameters
        ----------
        request: AccessToken
            Access token
        context: grpc.ServicerContext
            Request context

        Returns
        -------
        AuthResponse
            Response object with ID of currently signed in user
        """
        pass

    def get_new_access_token(
        self,
        request: get_access_token_proto.GetNewAccessTokenRequest,
        context: grpc.ServicerContext,
    ) -> get_access_token_proto.GetNewAccessTokenResponse:
        """
        Generates new access_token for user to authenticate with

        Parameters
        ----------
        request: GetNewAccessTokenRequest
            Refresh token
        context: grpc.ServicerContext
            Request context

        Returns
        -------
        GetNewAccessTokenResponse
            Response object with new access token
        """
        pass

    def get_user_by_id(
        self, request: get_user_proto.UserByIdRequest, context: grpc.ServicerContext
    ) -> get_user_proto.UserByIdResponse:
        """
        Gets user object that matches given ID

        Parameters
        ----------
        request: UserByIdRequest
            User ID
        context: grpc.ServicerContext
            Request context

        Returns
        -------
        UserByIdResponse
            Response object with public user data
        """
        pass

    def get_users_by_id(
        self, request: get_user_proto.UsersByIdRequest, context: grpc.ServicerContext
    ) -> get_user_proto.UsersByIdResponse:
        """
        Gets user objects that matches given ids

        Parameters
        ----------
        request: UsersByIdRequest
            User ids
        context: grpc.ServicerContext
            Request context

        Returns
        -------
        UsersByIdResponse
            Response object with array of public user data
        """
        pass

    def update_user(
        self,
        request: update_user_proto.UpdateUserRequest,
        context: grpc.ServicerContext,
    ) -> requests_proto.BaseResponse:
        """
        Updates user data

        Parameters
        ----------
        request: UpdateUserRequest
            User data to be updated and current user id
        context: grpc.ServicerContext
            Request context

        Returns
        -------
        BaseResponse
            Base response with status code and optional message
        """
        pass

    def delete_user(
        self,
        request: delete_user_proto.DeleteUserRequest,
        context: grpc.ServicerContext,
    ) -> requests_proto.BaseResponse:
        """
        Deletes user with matching ID

        Parameters
        ----------
        request: DeleteUserRequest
            ID of user to be deleted
        context: grpc.ServicerContext
            Request context

        Returns
        -------
        BaseResponse
            Base response with status code and optional message
        """
        pass

    def logout(
        self, request: auth_proto.AccessToken, context: grpc.ServicerContext
    ) -> requests_proto.BaseResponse:
        """
        Logs out and deletes user's access token from database

        Parameters
        ----------
        request: AccessToken
            ID of user to be deleted
        context: grpc.ServicerContext
            Request context

        Returns
        -------
        BaseResponse
            Base response with status code and optional message
        """
        pass
