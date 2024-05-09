from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from user import user_pb2 as _user_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class UserByIdRequest(_message.Message):
    __slots__ = ('user_id',)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str

    def __init__(self, user_id: _Optional[str]=...) -> None:
        ...

class GetUserByEmailRequest(_message.Message):
    __slots__ = ('email',)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str

    def __init__(self, email: _Optional[str]=...) -> None:
        ...

class ListOfUser(_message.Message):
    __slots__ = ('users',)
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[_user_pb2.GrpcUser]

    def __init__(self, users: _Optional[_Iterable[_Union[_user_pb2.GrpcUser, _Mapping]]]=...) -> None:
        ...

class UsersByIdRequest(_message.Message):
    __slots__ = ('page', 'items_per_page', 'id')
    PAGE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_PER_PAGE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    page: int
    items_per_page: int
    id: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, page: _Optional[int]=..., items_per_page: _Optional[int]=..., id: _Optional[_Iterable[str]]=...) -> None:
        ...

class GetAllUsersRequest(_message.Message):
    __slots__ = ('page', 'items_per_page', 'requested_user')
    PAGE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_PER_PAGE_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_USER_FIELD_NUMBER: _ClassVar[int]
    page: int
    items_per_page: int
    requested_user: _user_pb2.GrpcUser

    def __init__(self, page: _Optional[int]=..., items_per_page: _Optional[int]=..., requested_user: _Optional[_Union[_user_pb2.GrpcUser, _Mapping]]=...) -> None:
        ...
