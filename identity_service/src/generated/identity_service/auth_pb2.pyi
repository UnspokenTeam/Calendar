from user import user_pb2 as _user_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class AccessToken(_message.Message):
    __slots__ = ('access_token',)
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str

    def __init__(self, access_token: _Optional[str]=...) -> None:
        ...

class LoginRequest(_message.Message):
    __slots__ = ('email', 'password')
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str

    def __init__(self, email: _Optional[str]=..., password: _Optional[str]=...) -> None:
        ...

class CredentialsResponse(_message.Message):
    __slots__ = ('data', 'user')
    DATA_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    data: LoginData
    user: _user_pb2.GrpcUser

    def __init__(self, data: _Optional[_Union[LoginData, _Mapping]]=..., user: _Optional[_Union[_user_pb2.GrpcUser, _Mapping]]=...) -> None:
        ...

class LoginData(_message.Message):
    __slots__ = ('refresh_token', 'access_token')
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    refresh_token: str
    access_token: str

    def __init__(self, refresh_token: _Optional[str]=..., access_token: _Optional[str]=...) -> None:
        ...