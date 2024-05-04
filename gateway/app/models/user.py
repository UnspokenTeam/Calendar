"""User model"""
from datetime import datetime
from enum import StrEnum
from typing import Annotated, Optional, Self
from uuid import UUID

from app.constants import MIN_USERNAME_LENGTH
from app.generated.identity_service.update_user_pb2 import UserToModify
from app.generated.user.user_pb2 import GrpcUser, GrpcUserType
from app.validators import str_special_characters_validator

from pydantic import UUID4, AfterValidator, BaseModel, EmailStr, Field


class UserType(StrEnum):
    """
    Enum of user types

    Methods
    -------
    from_proto(proto)
        Get user type from proto user type
    to_proto()
        Get proto user type from user type

    """

    USER = "USER"
    """Standard user type"""
    ADMIN = "ADMIN"
    """Admin user type"""

    @classmethod
    def from_proto(cls, proto: GrpcUserType) -> Self:
        """
        Get user type from proto user type

        Parameters
        ----------
        proto : GrpcUserType
            Proto user type

        Returns
        -------
        UserType
            User type

        """
        if proto == GrpcUserType.USER:
            return cls("USER")
        return cls("ADMIN")

    def to_proto(self) -> GrpcUserType:
        """
        Get proto user type from user type

        Returns
        -------
        GrpcUserType
            Proto user type

        """
        if self == UserType.USER:
            return GrpcUserType.USER
        return GrpcUserType.ADMIN


class User(BaseModel):
    """
    User model

    Attributes
    ----------
    id : UUID4 | str
        ID of the user
    username : str
        User's name
    email : str
        Email of the user
    password : str
        Hashed password of the user
    type: UserType
        Type of the user
    created_at: datetime
        Date and time when the user was created
    suspended_at: datetime
        Date and time when the user was suspended

    Methods
    -------
    from_proto(proto)
        Get a user instance from user proto
    to_update_proto()
        Convert object to update proto

    """

    id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    username: Annotated[str, Field("", min_length=MIN_USERNAME_LENGTH), AfterValidator(str_special_characters_validator)]
    email: EmailStr
    password: Annotated[str, AfterValidator(str_special_characters_validator)]
    created_at: datetime
    suspended_at: Optional[datetime]
    type: UserType

    @classmethod
    def from_proto(cls, proto: GrpcUser) -> Self:
        """
        Get a user instance from user proto

        Parameters
        ----------
        proto : GrpcUser
            User proto

        Returns
        -------
        User
            User instance

        """
        return cls(
            id=proto.id,
            username=proto.username,
            email=proto.email,
            password="",
            created_at=datetime.fromtimestamp(
                proto.created_at.seconds + proto.created_at.nanos / 1e9
            ),
            suspended_at=None
            if proto.WhichOneof("optional_suspended_at") is None
            else datetime.fromtimestamp(
                proto.suspended_at.seconds + proto.suspended_at.nanos / 1e9
            ),
            type=UserType.from_proto(proto.type),
        )

    def to_modify_proto(self) -> UserToModify:
        """
        Convert object to update proto

        Returns
        -------
        UserToUpdate
            Update proto

        """
        user = UserToModify(
            id=str(self.id),
            username=self.username,
            password=self.password,
            type=self.type.to_proto(),
            email=self.email,
        )
        user.created_at.FromDatetime(self.created_at)
        if self.suspended_at is not None:
            user.suspended_at.FromDatetime(self.suspended_at)
        return user
