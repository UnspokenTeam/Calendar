"""User repository with data from database"""
from datetime import datetime
from typing import Optional, List

from prisma.models import User as PrismaUser

from db.postgres_client import PostgresClient
from errors.unique_error import UniqueError
from errors.value_not_found_error import ValueNotFoundError
from repository.user_repository_interface import UserRepositoryInterface
from src.models.user import User
from utils.singleton import singleton


@singleton
class UserRepositoryImpl(UserRepositoryInterface):
    """
    Class for manipulating with user data

    Attributes
    ----------
    _db_client : prisma.Client
        Postgres db client

    Methods
    -------
    async get_user_by_email(email)
        Returns user that has matching email from database or throws an exception
    async get_user_by_id(user_id)
        Returns user that has matching id from database or throws an exception
    async get_users_by_ids(user_ids)
        Returns users that has matching ids from database or throws an exception
    async create_user(user)
        Creates new user inside db or throws an exception
    async update_user(user)
        Updates user that has the same id as provided user object inside db or throws an exception
    async delete_user(user_id)
        Deletes user that has matching id from database or throws an exception

    """

    _db_client: PostgresClient

    def __init__(self) -> None:
        self._db_client = PostgresClient()

    async def get_user_by_email(self, email: str) -> User:
        """
        Returns user that has matching email from database or throws an exception

        Parameters
        ----------
        email : str
            User's email

        Returns
        -------
        User
            User that has matching email

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python
        ValueNotFoundError
            No user was found for given email

        """
        db_user: Optional[PrismaUser] = await self._db_client.db.user.find_first(
            where={"email": email, "suspended_at": None}
        )
        if db_user is None:
            raise ValueNotFoundError("User not found")
        return User.from_prisma_user(db_user)

    async def get_user_by_id(self, user_id: str) -> User:
        """
        Returns user that has matching id from database or throws an exception

        Parameters
        ----------
        user_id : str
            User's id

        Returns
        -------
        User
            User that has matching id

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python
        ValueNotFoundError
            No user was found for given email

        """
        db_user: Optional[PrismaUser] = await self._db_client.db.user.find_first(
            where={"id": user_id, "suspended_at": None}
        )
        if db_user is None:
            raise ValueNotFoundError("User not found")
        return User.from_prisma_user(db_user)

    async def get_users_by_ids(self, user_ids: List[str]) -> List[User]:
        """
        Returns users that has matching ids from database or throws an exception

        Parameters
        ----------
        user_ids : List[str]
            User's ids

        Returns
        -------
        List[User]
            Users that has matching id

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python
        ValueNotFoundError
            No users was found for given email

        """
        db_users: Optional[List[PrismaUser]] = await self._db_client.db.user.find_many(
            where={"id": {"in": user_ids}, "suspended_at": None}
        )

        if db_users is None:
            raise ValueNotFoundError("Value is None")

        if len(db_users) == 0:
            raise ValueNotFoundError("No users not found")

        return [User.from_prisma_user(db_user) for db_user in db_users]

    async def create_user(self, user: User) -> None:
        """
        Creates user with matching data or throws an exception

        Parameters
        ----------
        user : User
            User data

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python
        UniqueError
            Another user with this data already exists

        """
        db_user_counter = await self._db_client.db.user.count(
            where={
                "OR": [
                    {"username": user.username},
                    {"email": user.email},
                ],
                "NOT": [{"id": user.id}],
                "suspended_at": None,
            }
        )
        if db_user_counter != 0:
            raise UniqueError("User with this email or username already exists")
        await self._db_client.db.user.create(data=user.to_dict())

    async def update_user(self, user: User) -> None:
        """
        Updates user with matching id or throws an exception

        Parameters
        ----------
        user : User
            User data

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python
        UniqueError
            Another user with this data already exists

        """
        db_user_counter = await self._db_client.db.user.count(
            where={
                "OR": [
                    {"username": user.username},
                    {"email": user.email},
                ],
                "suspended_at": None,
                "NOT": [{"id": user.id}],
            }
        )
        if db_user_counter != 0:
            raise UniqueError("User with this email or username already exists")
        await self._db_client.db.user.update(where={"id": user.id}, data=user.to_dict())

    async def delete_user(self, user_id: str) -> None:
        """
        Deletes user with matching id or throws an exception

        Parameters
        ----------
        user_id : str
            User's id

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        await self._db_client.db.user.update(
            where={"id": user_id}, data={"suspended_at": datetime.now()}
        )
