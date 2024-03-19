from proto.identity_service_pb2_grpc import IdentityServiceServicer as GrpcServicer
from proto.identity_service_pb2 import LoginRequest, LoginResponse


class IdentityServiceImpl(GrpcServicer):
    def login(self, request: LoginRequest, context) -> LoginResponse:
        print(request.username, request.password)
        if request.username == "username" and request.password == "password":
            return LoginResponse(refreshToken="refresh", accessToken="access")
