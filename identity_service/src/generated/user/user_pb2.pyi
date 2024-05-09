from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GrpcUserType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER: _ClassVar[GrpcUserType]
    ADMIN: _ClassVar[GrpcUserType]
USER: GrpcUserType
ADMIN: GrpcUserType

class GrpcUser(_message.Message):
    __slots__ = ('id', 'username', 'email', 'created_at', 'suspended_at_null', 'suspended_at', 'type')
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_AT_NULL_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_AT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    username: str
    email: str
    created_at: _timestamp_pb2.Timestamp
    suspended_at_null: _struct_pb2.NullValue
    suspended_at: _timestamp_pb2.Timestamp
    type: GrpcUserType

    def __init__(self, id: _Optional[str]=..., username: _Optional[str]=..., email: _Optional[str]=..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., suspended_at_null: _Optional[_Union[_struct_pb2.NullValue, str]]=..., suspended_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., type: _Optional[_Union[GrpcUserType, str]]=...) -> None:
        ...