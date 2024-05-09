from google.protobuf import timestamp_pb2 as _timestamp_pb2
from user import user_pb2 as _user_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class UpdateUserRequest(_message.Message):
    __slots__ = ('new_user', 'requesting_user')
    NEW_USER_FIELD_NUMBER: _ClassVar[int]
    REQUESTING_USER_FIELD_NUMBER: _ClassVar[int]
    new_user: UserToModify
    requesting_user: _user_pb2.GrpcUser

    def __init__(self, new_user: _Optional[_Union[UserToModify, _Mapping]]=..., requesting_user: _Optional[_Union[_user_pb2.GrpcUser, _Mapping]]=...) -> None:
        ...

class UserToModify(_message.Message):
    __slots__ = ('id', 'username', 'email', 'password', 'created_at', 'suspended_at_null', 'suspended_at', 'type')
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_AT_NULL_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_AT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    username: str
    email: str
    password: str
    created_at: _timestamp_pb2.Timestamp
    suspended_at_null: _struct_pb2.NullValue
    suspended_at: _timestamp_pb2.Timestamp
    type: _user_pb2.GrpcUserType

    def __init__(self, id: _Optional[str]=..., username: _Optional[str]=..., email: _Optional[str]=..., password: _Optional[str]=..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., suspended_at_null: _Optional[_Union[_struct_pb2.NullValue, str]]=..., suspended_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., type: _Optional[_Union[_user_pb2.GrpcUserType, str]]=...) -> None:
        ...