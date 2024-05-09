"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ..user import user_pb2 as user_dot_user__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"identity_service/delete_user.proto\x1a\x0fuser/user.proto"H\n\x11DeleteUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12"\n\x0frequesting_user\x18\x02 \x01(\x0b2\t.GrpcUserb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'identity_service.delete_user_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_DELETEUSERREQUEST']._serialized_start = 55
    _globals['_DELETEUSERREQUEST']._serialized_end = 127