from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class GetNewAccessTokenRequest(_message.Message):
    __slots__ = ('refresh_token',)
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    refresh_token: str

    def __init__(self, refresh_token: _Optional[str]=...) -> None:
        ...

class GetNewAccessTokenResponse(_message.Message):
    __slots__ = ('access_token',)
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str

    def __init__(self, access_token: _Optional[str]=...) -> None:
        ...