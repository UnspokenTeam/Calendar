"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bidentity_service/auth.proto\x1a\x0fuser/user.proto"#\n\x0bAccessToken\x12\x14\n\x0caccess_token\x18\x01 \x01(\t"/\n\x0cLoginRequest\x12\r\n\x05email\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t"H\n\x13CredentialsResponse\x12\x18\n\x04data\x18\x01 \x01(\x0b2\n.LoginData\x12\x17\n\x04user\x18\x02 \x01(\x0b2\t.GrpcUser"8\n\tLoginData\x12\x15\n\rrefresh_token\x18\x01 \x01(\t\x12\x14\n\x0caccess_token\x18\x02 \x01(\tb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'identity_service.auth_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_ACCESSTOKEN']._serialized_start = 48
    _globals['_ACCESSTOKEN']._serialized_end = 83
    _globals['_LOGINREQUEST']._serialized_start = 85
    _globals['_LOGINREQUEST']._serialized_end = 132
    _globals['_CREDENTIALSRESPONSE']._serialized_start = 134
    _globals['_CREDENTIALSRESPONSE']._serialized_end = 206
    _globals['_LOGINDATA']._serialized_start = 208
    _globals['_LOGINDATA']._serialized_end = 264
