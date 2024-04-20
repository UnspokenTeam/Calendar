from datetime import datetime
from enum import StrEnum
from typing import Optional, Self

from app.generated.user.user_pb2 import GrpcUser, GrpcUserType

from pydantic import BaseModel, EmailStr


class UserType(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"

    @classmethod
    def from_proto(cls, proto: GrpcUserType) -> Self:
        if proto == GrpcUserType.USER:
            return cls.USER
        return cls.ADMIN

    def to_proto(self) -> GrpcUserType:
        if self == GrpcUserType.USER:
            return GrpcUserType.USER
        return GrpcUserType.ADMIN


class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    password: str
    created_at: datetime
    suspended_at: Optional[datetime]
    type: UserType

    @classmethod
    def from_proto(cls, proto: GrpcUser) -> Self:
        return cls(
            id=proto.id,
            username=proto.username,
            email=proto.email,
            password="",
            created_at=datetime.fromtimestamp(
                proto.created_at.seconds + proto.created_at.nanos / 1e9
            ),
            suspended_at=None if proto.suspended_at is None else datetime.fromtimestamp(
                proto.suspended_at.seconds + proto.suspended_at.nanos / 1e9
            ),
            type=UserType.from_proto(proto.type)
        )
