import grpc

from proto.identity_service_pb2_grpc import IdentityServiceServicer as GrpcServicer
from proto.identity_service_pb2 import (
    LoginRequest,
    CredentialsResponse,
    LoginData,
    RegisterRequest,
    AccessToken,
    AuthResponse,
    GetNewAccessTokenRequest,
    GetNewAccessTokenResponse,
    UsersByIdRequest,
    UsersByIdResponse,
    UserByIdResponse,
    UserByIdRequest,
    User as GrpcUser,
    BaseResponse,
    DeleteUserRequest,
)


class IdentityServiceImpl(GrpcServicer):
    def login(
        self, request: LoginRequest, context: grpc.ServicerContext
    ) -> CredentialsResponse:
        if request.username == "username" and request.password == "password":
            return CredentialsResponse(
                status_code=200,
                data=LoginData(refresh_token="refresh", access_token="access"),
            )

    def register(
        self, request: RegisterRequest, context: grpc.ServicerContext
    ) -> CredentialsResponse:
        pass

    def auth(self, request: AccessToken, context: grpc.ServicerContext) -> AuthResponse:
        pass

    def get_new_access_token(
        self, request: GetNewAccessTokenRequest, context: grpc.ServicerContext
    ) -> GetNewAccessTokenResponse:
        pass

    def get_user_by_id(
        self, request: UserByIdRequest, context: grpc.ServicerContext
    ) -> UserByIdResponse:
        pass

    def get_users_by_id(
        self, request: UsersByIdRequest, context: grpc.ServicerContext
    ) -> UsersByIdResponse:
        pass

    def update_user(
        self, request: GrpcUser, context: grpc.ServicerContext
    ) -> BaseResponse:
        pass

    def delete_user(
        self, request: DeleteUserRequest, context: grpc.ServicerContext
    ) -> BaseResponse:
        pass

    def logout(self, request: AccessToken, context: grpc.ServicerContext):
        pass
