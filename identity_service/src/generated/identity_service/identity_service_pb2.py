"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ..identity_service import auth_pb2 as identity__service_dot_auth__pb2
from ..identity_service import get_access_token_pb2 as identity__service_dot_get__access__token__pb2
from ..identity_service import get_user_pb2 as identity__service_dot_get__user__pb2
from ..identity_service import update_user_pb2 as identity__service_dot_update__user__pb2
from ..identity_service import delete_user_pb2 as identity__service_dot_delete__user__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ..user import user_pb2 as user_dot_user__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'identity_service/identity_service.proto\x1a\x1bidentity_service/auth.proto\x1a\'identity_service/get_access_token.proto\x1a\x1fidentity_service/get_user.proto\x1a"identity_service/update_user.proto\x1a"identity_service/delete_user.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x0fuser/user.proto2\xe7\x04\n\x0fIdentityService\x120\n\x06logout\x12\x0c.AccessToken\x1a\x16.google.protobuf.Empty"\x00\x12!\n\x04auth\x12\x0c.AccessToken\x1a\t.GrpcUser"\x00\x12.\n\x05login\x12\r.LoginRequest\x1a\x14.CredentialsResponse"\x00\x121\n\x08register\x12\r.UserToModify\x1a\x14.CredentialsResponse"\x00\x12O\n\x14get_new_access_token\x12\x19.GetNewAccessTokenRequest\x1a\x1a.GetNewAccessTokenResponse"\x00\x128\n\x11get_user_by_email\x12\x16.GetUserByEmailRequest\x1a\t.GrpcUser"\x00\x12/\n\x0eget_user_by_id\x12\x10.UserByIdRequest\x1a\t.GrpcUser"\x00\x123\n\x0fget_users_by_id\x12\x11.UsersByIdRequest\x1a\x0b.ListOfUser"\x00\x123\n\rget_all_users\x12\x13.GetAllUsersRequest\x1a\x0b.ListOfUser"\x00\x129\n\x0bupdate_user\x12\x12.UpdateUserRequest\x1a\x14.CredentialsResponse"\x00\x12;\n\x0bdelete_user\x12\x12.DeleteUserRequest\x1a\x16.google.protobuf.Empty"\x00b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'identity_service.identity_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_IDENTITYSERVICE']._serialized_start = 265
    _globals['_IDENTITYSERVICE']._serialized_end = 880