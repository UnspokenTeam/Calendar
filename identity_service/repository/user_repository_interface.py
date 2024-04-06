"""User repository interface"""
from abc import ABC, abstractmethod
from typing import List

from src.models.user import User


class UserRepositoryInterface(ABC):
    """
    Interface for class for manipulating with user data

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
    async get_all_users()
        Get all existing users from database
    async get_user_by_session_id(session_id)
        Get user by session id

    """

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        ValueNotFoundError
            No users was found for given email

        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        ValueNotFoundError
            No users found
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        pass

    @abstractmethod
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
        pass
