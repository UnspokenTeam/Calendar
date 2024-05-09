"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ..identity_service import auth_pb2 as identity__service_dot_auth__pb2
from ..identity_service import delete_user_pb2 as identity__service_dot_delete__user__pb2
from ..identity_service import get_access_token_pb2 as identity__service_dot_get__access__token__pb2
from ..identity_service import get_user_pb2 as identity__service_dot_get__user__pb2
from ..identity_service import update_user_pb2 as identity__service_dot_update__user__pb2
from ..user import user_pb2 as user_dot_user__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class IdentityServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.logout = channel.unary_unary('/IdentityService/logout', request_serializer=identity__service_dot_auth__pb2.AccessToken.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.auth = channel.unary_unary('/IdentityService/auth', request_serializer=identity__service_dot_auth__pb2.AccessToken.SerializeToString, response_deserializer=user_dot_user__pb2.GrpcUser.FromString)
        self.login = channel.unary_unary('/IdentityService/login', request_serializer=identity__service_dot_auth__pb2.LoginRequest.SerializeToString, response_deserializer=identity__service_dot_auth__pb2.CredentialsResponse.FromString)
        self.register = channel.unary_unary('/IdentityService/register', request_serializer=identity__service_dot_update__user__pb2.UserToModify.SerializeToString, response_deserializer=identity__service_dot_auth__pb2.CredentialsResponse.FromString)
        self.get_new_access_token = channel.unary_unary('/IdentityService/get_new_access_token', request_serializer=identity__service_dot_get__access__token__pb2.GetNewAccessTokenRequest.SerializeToString, response_deserializer=identity__service_dot_get__access__token__pb2.GetNewAccessTokenResponse.FromString)
        self.get_user_by_email = channel.unary_unary('/IdentityService/get_user_by_email', request_serializer=identity__service_dot_get__user__pb2.GetUserByEmailRequest.SerializeToString, response_deserializer=user_dot_user__pb2.GrpcUser.FromString)
        self.get_user_by_id = channel.unary_unary('/IdentityService/get_user_by_id', request_serializer=identity__service_dot_get__user__pb2.UserByIdRequest.SerializeToString, response_deserializer=user_dot_user__pb2.GrpcUser.FromString)
        self.get_users_by_id = channel.unary_unary('/IdentityService/get_users_by_id', request_serializer=identity__service_dot_get__user__pb2.UsersByIdRequest.SerializeToString, response_deserializer=identity__service_dot_get__user__pb2.ListOfUser.FromString)
        self.get_all_users = channel.unary_unary('/IdentityService/get_all_users', request_serializer=identity__service_dot_get__user__pb2.GetAllUsersRequest.SerializeToString, response_deserializer=identity__service_dot_get__user__pb2.ListOfUser.FromString)
        self.update_user = channel.unary_unary('/IdentityService/update_user', request_serializer=identity__service_dot_update__user__pb2.UpdateUserRequest.SerializeToString, response_deserializer=identity__service_dot_auth__pb2.CredentialsResponse.FromString)
        self.delete_user = channel.unary_unary('/IdentityService/delete_user', request_serializer=identity__service_dot_delete__user__pb2.DeleteUserRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)

class IdentityServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def logout(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def auth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def login(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_new_access_token(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_user_by_email(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_user_by_id(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_users_by_id(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_all_users(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_user(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_user(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_IdentityServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'logout': grpc.unary_unary_rpc_method_handler(servicer.logout, request_deserializer=identity__service_dot_auth__pb2.AccessToken.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'auth': grpc.unary_unary_rpc_method_handler(servicer.auth, request_deserializer=identity__service_dot_auth__pb2.AccessToken.FromString, response_serializer=user_dot_user__pb2.GrpcUser.SerializeToString), 'login': grpc.unary_unary_rpc_method_handler(servicer.login, request_deserializer=identity__service_dot_auth__pb2.LoginRequest.FromString, response_serializer=identity__service_dot_auth__pb2.CredentialsResponse.SerializeToString), 'register': grpc.unary_unary_rpc_method_handler(servicer.register, request_deserializer=identity__service_dot_update__user__pb2.UserToModify.FromString, response_serializer=identity__service_dot_auth__pb2.CredentialsResponse.SerializeToString), 'get_new_access_token': grpc.unary_unary_rpc_method_handler(servicer.get_new_access_token, request_deserializer=identity__service_dot_get__access__token__pb2.GetNewAccessTokenRequest.FromString, response_serializer=identity__service_dot_get__access__token__pb2.GetNewAccessTokenResponse.SerializeToString), 'get_user_by_email': grpc.unary_unary_rpc_method_handler(servicer.get_user_by_email, request_deserializer=identity__service_dot_get__user__pb2.GetUserByEmailRequest.FromString, response_serializer=user_dot_user__pb2.GrpcUser.SerializeToString), 'get_user_by_id': grpc.unary_unary_rpc_method_handler(servicer.get_user_by_id, request_deserializer=identity__service_dot_get__user__pb2.UserByIdRequest.FromString, response_serializer=user_dot_user__pb2.GrpcUser.SerializeToString), 'get_users_by_id': grpc.unary_unary_rpc_method_handler(servicer.get_users_by_id, request_deserializer=identity__service_dot_get__user__pb2.UsersByIdRequest.FromString, response_serializer=identity__service_dot_get__user__pb2.ListOfUser.SerializeToString), 'get_all_users': grpc.unary_unary_rpc_method_handler(servicer.get_all_users, request_deserializer=identity__service_dot_get__user__pb2.GetAllUsersRequest.FromString, response_serializer=identity__service_dot_get__user__pb2.ListOfUser.SerializeToString), 'update_user': grpc.unary_unary_rpc_method_handler(servicer.update_user, request_deserializer=identity__service_dot_update__user__pb2.UpdateUserRequest.FromString, response_serializer=identity__service_dot_auth__pb2.CredentialsResponse.SerializeToString), 'delete_user': grpc.unary_unary_rpc_method_handler(servicer.delete_user, request_deserializer=identity__service_dot_delete__user__pb2.DeleteUserRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('IdentityService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class IdentityService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def logout(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/logout', identity__service_dot_auth__pb2.AccessToken.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def auth(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/auth', identity__service_dot_auth__pb2.AccessToken.SerializeToString, user_dot_user__pb2.GrpcUser.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def login(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/login', identity__service_dot_auth__pb2.LoginRequest.SerializeToString, identity__service_dot_auth__pb2.CredentialsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def register(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/register', identity__service_dot_update__user__pb2.UserToModify.SerializeToString, identity__service_dot_auth__pb2.CredentialsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_new_access_token(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/get_new_access_token', identity__service_dot_get__access__token__pb2.GetNewAccessTokenRequest.SerializeToString, identity__service_dot_get__access__token__pb2.GetNewAccessTokenResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_user_by_email(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/get_user_by_email', identity__service_dot_get__user__pb2.GetUserByEmailRequest.SerializeToString, user_dot_user__pb2.GrpcUser.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_user_by_id(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/get_user_by_id', identity__service_dot_get__user__pb2.UserByIdRequest.SerializeToString, user_dot_user__pb2.GrpcUser.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_users_by_id(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/get_users_by_id', identity__service_dot_get__user__pb2.UsersByIdRequest.SerializeToString, identity__service_dot_get__user__pb2.ListOfUser.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_all_users(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/get_all_users', identity__service_dot_get__user__pb2.GetAllUsersRequest.SerializeToString, identity__service_dot_get__user__pb2.ListOfUser.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_user(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/update_user', identity__service_dot_update__user__pb2.UpdateUserRequest.SerializeToString, identity__service_dot_auth__pb2.CredentialsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_user(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IdentityService/delete_user', identity__service_dot_delete__user__pb2.DeleteUserRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
