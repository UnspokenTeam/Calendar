"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'identity_service/get_access_token.proto"1\n\x18GetNewAccessTokenRequest\x12\x15\n\rrefresh_token\x18\x01 \x01(\t"1\n\x19GetNewAccessTokenResponse\x12\x14\n\x0caccess_token\x18\x01 \x01(\tb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'identity_service.get_access_token_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_GETNEWACCESSTOKENREQUEST']._serialized_start = 43
    _globals['_GETNEWACCESSTOKENREQUEST']._serialized_end = 92
    _globals['_GETNEWACCESSTOKENRESPONSE']._serialized_start = 94
    _globals['_GETNEWACCESSTOKENRESPONSE']._serialized_end = 143