"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"identity_service/update_user.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x0fuser/user.proto\x1a\x1cgoogle/protobuf/struct.proto"X\n\x11UpdateUserRequest\x12\x1f\n\x08new_user\x18\x01 \x01(\x0b2\r.UserToModify\x12"\n\x0frequesting_user\x18\x02 \x01(\x0b2\t.GrpcUser"\xa0\x02\n\x0cUserToModify\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05email\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\x12.\n\ncreated_at\x18\x05 \x01(\x0b2\x1a.google.protobuf.Timestamp\x127\n\x11suspended_at_null\x18\x06 \x01(\x0e2\x1a.google.protobuf.NullValueH\x00\x122\n\x0csuspended_at\x18\x07 \x01(\x0b2\x1a.google.protobuf.TimestampH\x00\x12\x1b\n\x04type\x18\x08 \x01(\x0e2\r.GrpcUserTypeB\x17\n\x15optional_suspended_atb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'identity_service.update_user_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_UPDATEUSERREQUEST']._serialized_start = 118
    _globals['_UPDATEUSERREQUEST']._serialized_end = 206
    _globals['_USERTOMODIFY']._serialized_start = 209
    _globals['_USERTOMODIFY']._serialized_end = 497
