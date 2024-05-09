from user import user_pb2 as _user_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class DeleteUserRequest(_message.Message):
    __slots__ = ('user_id', 'requesting_user')
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTING_USER_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    requesting_user: _user_pb2.GrpcUser

    def __init__(self, user_id: _Optional[str]=..., requesting_user: _Optional[_Union[_user_pb2.GrpcUser, _Mapping]]=...) -> None:
        ...