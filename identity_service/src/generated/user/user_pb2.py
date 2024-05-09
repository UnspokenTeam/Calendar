"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fuser/user.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1cgoogle/protobuf/struct.proto"\x8a\x02\n\x08GrpcUser\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05email\x18\x03 \x01(\t\x12.\n\ncreated_at\x18\x04 \x01(\x0b2\x1a.google.protobuf.Timestamp\x127\n\x11suspended_at_null\x18\x05 \x01(\x0e2\x1a.google.protobuf.NullValueH\x00\x122\n\x0csuspended_at\x18\x06 \x01(\x0b2\x1a.google.protobuf.TimestampH\x00\x12\x1b\n\x04type\x18\x07 \x01(\x0e2\r.GrpcUserTypeB\x17\n\x15optional_suspended_at*#\n\x0cGrpcUserType\x12\x08\n\x04USER\x10\x00\x12\t\n\x05ADMIN\x10\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user.user_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_GRPCUSERTYPE']._serialized_start = 351
    _globals['_GRPCUSERTYPE']._serialized_end = 386
    _globals['_GRPCUSER']._serialized_start = 83
    _globals['_GRPCUSER']._serialized_end = 349
