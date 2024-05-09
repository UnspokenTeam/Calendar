from typing import ClassVar as _ClassVar
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from user import user_pb2 as _user_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteUserRequest(_message.Message):
    __slots__ = ('user_id', 'requesting_user')
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTING_USER_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    requesting_user: _user_pb2.GrpcUser

    def __init__(self, user_id: _Optional[str]=..., requesting_user: _Optional[_Union[_user_pb2.GrpcUser, _Mapping]]=...) -> None:
        ...
