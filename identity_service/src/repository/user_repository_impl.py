"""User repository with data from database"""

from datetime import datetime
from typing import List, Optional

from prisma.models import User as PrismaUser

from db import PostgresClient
from errors import UniqueError, ValueNotFoundError
from src.models import User
from src.repository.user_repository_interface import UserRepositoryInterface
from utils import singleton


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
        Returns user that has matching email from database
    async get_user_by_id(user_id)
        Returns user that has matching id from database
    async get_users_by_ids(user_ids)
        Returns users that has matching ids from database
    async create_user(user)
        Creates new user inside database
    async update_user(user)
        Updates user that has the same id as provided user object inside db
    async delete_user(user_id)
        Deletes user that has matching id from database
    async get_all_users()
        Get all existing users from database
    async get_user_by_session_id(session_id)
        Get user by session id

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

    async def get_users_by_ids(
        self, user_ids: List[str], page: int, items_per_page: int
    ) -> List[User]:
        """
        Returns users that has matching ids from database or throws an exception

        Parameters
        ----------
        user_ids : List[str]
            User's ids
        page : int
            Non-Negative page index
        items_per_page : int
            Number of items per page

        Returns
        -------
        List[User]
            Users that has matching id

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        db_users = await self._db_client.db.user.find_many(
            where={"id": {"in": user_ids}, "suspended_at": None},
            skip=(page - 1) * items_per_page if items_per_page != -1 else None,
            take=items_per_page if items_per_page != -1 else None,
        )

        return [User.from_prisma_user(db_user) for db_user in db_users]

    async def create_user(self, user: User) -> User:
        """
        Creates user with matching data or throws an exception

        Parameters
        ----------
        user : User
            User data

        Returns
        -------
        User
            Created user

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
        prisma_user_data = await self._db_client.db.user.create(data=user.to_dict(exclude=["deleted_at", "created_at"]))
        return User.from_prisma_user(prisma_user_data)

    async def update_user(self, user: User) -> User:
        """
        Updates user with matching id or throws an exception

        Parameters
        ----------
        user : User
            User data

        Returns
        -------
        User
            Updated user object

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
        prisma_user_data = await self._db_client.db.user.update(
            where={"id": user.id},
            data=user.to_dict(),
        )
        if prisma_user_data is None:
            raise ValueNotFoundError("User not found")
        return User.from_prisma_user(prisma_user_data)

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
        await self._db_client.db.user.update_many(
            where={"id": user_id, "suspended_at": None},
            data={"suspended_at": datetime.utcnow()},
        )

    async def get_all_users(self, page: int, items_per_page: int) -> List[User]:
        """
        Get all existing users

        Parameters
        ----------
        page : int
            Non-Negative page index
        items_per_page : int
            Number of items per page

        Returns
        -------
        List[User]
            All existing users

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        users = await self._db_client.db.user.find_many(
            skip=(page - 1) * items_per_page if items_per_page != -1 else None,
            take=items_per_page if items_per_page != -1 else None,
        )
        return [User.from_prisma_user(user) for user in users]

    async def get_user_by_session_id(self, session_id: str) -> User:
        """
        Get user by session id

        Parameters
        ----------
        session_id : str
            Id of the session

        Returns
        -------
        User
            User with corresponding session

        Raises
        ------
        ValueNotFoundError
            User not found
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        token = await self._db_client.db.token.find_unique(
            where={
                "id": session_id,
            },
            include={"user": True},
        )
        if token is None or token.user is None:
            raise ValueNotFoundError("Session not found")
        return User.from_prisma_user(prisma_user=token.user)
