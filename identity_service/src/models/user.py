"""User Model"""
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, List, Optional, Self

from prisma.models import User as PrismaUser

from generated.auth_pb2 import RegisterRequest
from generated.get_user_pb2 import GrpcUser, GrpcUserType
from generated.update_user_pb2 import UserToUpdate as GrpcUserToUpdate


class UserType(StrEnum):
    """
    Enum of user types

    Methods
    -------
    from_grpc_user_type(grpc_user_type)
        Get user type from grpc user type
    """

    USER = "USER"
    """Standard user type"""
    ADMIN = "ADMIN"
    """Admin user type"""

    @classmethod
    def from_grpc_user_type(cls, grpc_user_type: GrpcUserType) -> Self:
        """
        Get user type from grpc user type

        Parameters
        ----------
        grpc_user_type
            Grpc user type

        Returns
        -------
        UserType
            UserType enum instance

        """
        return cls("USER") if grpc_user_type == GrpcUserType.USER else cls("ADMIN")


@dataclass
class User:
    """
    Data class that stores user information

    Attributes
    ----------
    id : str
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
    to_grpc_user()
        Returns user's information as a GrpcUser class instance
    from_prisma_user(prisma_user)
        Returns user class instance from PrismaUser
    to_dict()
        Returns user's data represented in dictionary
    from_update_grpc_user(grpc_user)
        Get user instance from update user request data
    from_register_request(request)
        Get user instance from registration request

    """

    id: str
    username: str
    email: str
    password: str
    type: UserType
    created_at: datetime
    suspended_at: datetime | None

    def to_grpc_user(self) -> GrpcUser:
        """
        Converts user information to GrpcUser

        Returns
        -------
        GrpcUser
            User data in GrpcUser instance

        """
        user = GrpcUser(
            id=self.id,
            username=self.username,
            email=self.email,
            type=GrpcUserType.USER
            if self.type == UserType.USER
            else GrpcUserType.ADMIN,
            suspended_at=None,
        )
        user.created_at.FromDatetime(self.created_at)
        if self.suspended_at is not None:
            user.suspended_at.FromDatetime(self.suspended_at)
        return user

    @classmethod
    def from_prisma_user(cls, prisma_user: PrismaUser) -> Self:
        """
        Returns user class instance from PrismaUser

        Parameters
        ----------
        prisma_user : PrismaUser
            Prisma user

        Returns
        -------
        User
            User class instance

        """
        return cls(
            id=prisma_user.id,
            username=prisma_user.username,
            email=prisma_user.email,
            password=prisma_user.password,
            type=UserType(prisma_user.role),
            created_at=prisma_user.created_at,
            suspended_at=prisma_user.suspended_at,
        )

    def to_dict(self, exclude: Optional[List[str]] = None) -> dict[str, Any]:
        """
        Get user data represented in dictionary

        Parameters
        ----------
        exclude : Optional[List[str]]
            Fields to exclude. All field names should be exactly the same as class attribute name

        Returns
        -------
        dict[str, Any]
            User data represented in dictionary

        """
        exclude_set = set(exclude if exclude is not None else [])
        attrs = vars(self)
        return {
            attr.lstrip("_"): value
            for attr, value in attrs.items()
            if attr not in exclude_set
        }

    @classmethod
    def from_register_request(cls, request: RegisterRequest) -> Self:
        """
        Get user instance from registration request

        Parameters
        ----------
        request
            Registration request


        Returns
        -------
        User
            User class instance

        """
        return cls(
            id="",
            username=request.username,
            email=request.email,
            password=request.password,
            type=UserType.USER,
            created_at=datetime.now(),
            suspended_at=None,
        )

    @classmethod
    def from_update_grpc_user(cls, grpc_user: GrpcUserToUpdate) -> Self:
        """
        Get user instance from update user request data

        Parameters
        ----------
        grpc_user
            Update user request data

        Returns
        -------
        User
            User class instance

        """
        return cls(
            id=grpc_user.id,
            username=grpc_user.username,
            password=grpc_user.password,
            email=grpc_user.email,
            type=UserType.from_grpc_user_type(grpc_user.type),
            created_at=datetime.fromtimestamp(
                grpc_user.created_at.seconds + grpc_user.created_at.nanos / 1e9
            ),
            suspended_at=datetime.fromtimestamp(
                grpc_user.suspended_at.seconds + grpc_user.suspended_at.nanos / 1e9
            ),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id

    def __repr__(self) -> str:
        return f"{vars(self)}"
