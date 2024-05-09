"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fidentity_service/get_user.proto\x1a\x0fuser/user.proto""\n\x0fUserByIdRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t"&\n\x15GetUserByEmailRequest\x12\r\n\x05email\x18\x01 \x01(\t"&\n\nListOfUser\x12\x18\n\x05users\x18\x01 \x03(\x0b2\t.GrpcUser"D\n\x10UsersByIdRequest\x12\x0c\n\x04page\x18\x01 \x01(\x04\x12\x16\n\x0eitems_per_page\x18\x02 \x01(\x03\x12\n\n\x02id\x18\x03 \x03(\t"]\n\x12GetAllUsersRequest\x12\x0c\n\x04page\x18\x01 \x01(\x04\x12\x16\n\x0eitems_per_page\x18\x02 \x01(\x03\x12!\n\x0erequested_user\x18\x03 \x01(\x0b2\t.GrpcUserb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'identity_service.get_user_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_USERBYIDREQUEST']._serialized_start = 52
    _globals['_USERBYIDREQUEST']._serialized_end = 86
    _globals['_GETUSERBYEMAILREQUEST']._serialized_start = 88
    _globals['_GETUSERBYEMAILREQUEST']._serialized_end = 126
    _globals['_LISTOFUSER']._serialized_start = 128
    _globals['_LISTOFUSER']._serialized_end = 166
    _globals['_USERSBYIDREQUEST']._serialized_start = 168
    _globals['_USERSBYIDREQUEST']._serialized_end = 236
    _globals['_GETALLUSERSREQUEST']._serialized_start = 238
    _globals['_GETALLUSERSREQUEST']._serialized_end = 331
