"""User Model"""
from dataclasses import dataclass
from typing import Any, List, Optional, Self

from prisma.models import User as PrismaUser

from generated.get_user_pb2 import User as GrpcUser


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
    _password : str
        Hashed password of the user

    Methods
    -------
    to_grpc_user()
        Returns user's information as a GrpcUser class instance
    from_prisma_user(prisma_user)
        Returns user class instance from PrismaUser
    to_dict()
        Returns user's data represented in dictionary

    """

    id: str
    username: str
    email: str
    _password: str

    def to_grpc_user(self) -> GrpcUser:
        """
        Converts user information to GrpcUser

        Returns
        -------
        GrpcUser
            User data in GrpcUser instance

        """
        return GrpcUser(
            id=self.id,
            username=self.username,
            email=self.email,
        )

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
            _password=prisma_user.password,
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
        exclude_set = set(exclude if exclude is not None else []) | {"id"}
        attrs = vars(self)
        return {
            attr.lstrip("_"): value
            for attr, value in attrs.items()
            if attr not in exclude_set
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id

    def __repr__(self) -> str:
        return f"{vars(self)}"
