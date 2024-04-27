"""Mock User Repository"""
from datetime import datetime
from typing import List
from uuid import uuid4

from errors.unique_error import UniqueError
from errors.value_not_found_error import ValueNotFoundError
from src.models.user import User
from utils.jwt_controller import JwtController, TokenType
from utils.singleton import singleton

from repository.mock_token_repository import MockTokenRepositoryImpl
from repository.user_repository_interface import UserRepositoryInterface


@singleton
class MockUserRepositoryImpl(UserRepositoryInterface):
    """
    Mock class for manipulating with user data

    Attributes
    ----------
    _users : List[User]
        List of users

    Methods
    -------
    async get_user_by_email(email)
        Returns user that has matching email from database
    async get_user_by_id(user_id)
        Returns user that has matching id from database
    async get_users_by_ids(user_ids)
        Returns users that has matching ids from database
    async create_user(user)
        Creates new user inside db or throws an exception
    async update_user(user)
        Updates user that has the same id as provided user object inside db
    async delete_user(user_id)
        Deletes user that has matching id from database
    async get_all_users()
        Returns all existing users
    async get_user_by_session_id(session_id)
        Get user with matching session id

    """

    _users: List[User]

    def __init__(self) -> None:
        self._users = []

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
        ValueNotFoundError
            User does not exist

        """
        try:
            return next(
                user
                for user in self._users
                if user.email == email and user.suspended_at is None
            )
        except StopIteration:
            raise ValueNotFoundError("No user found for this id")

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
        ValueNotFoundError
            User does not exist

        """
        try:
            return next(
                user
                for user in self._users
                if user.id == user_id and user.suspended_at is None
            )
        except StopIteration:
            raise ValueNotFoundError("No user found for this id")

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
        ValueNotFoundError
            Users does not exist

        """
        values = [
            user
            for user in self._users
            if user.id in user_ids and user.suspended_at is None
        ]
        values = (
            values[(page - 1) * items_per_page : page * items_per_page]
            if items_per_page != -1
            else values
        )
        if len(values) == 0:
            raise ValueNotFoundError("Users with these ids not exist")
        return values

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
        UniqueError
            Another user with this data already exists

        """
        if (
            len(
                [
                    True
                    for userdb in self._users
                    if (userdb.username == user.username or user.email == userdb.email)
                    and user.suspended_at is None
                ]
            )
            != 0
        ):
            raise UniqueError("User with this data already exists")

        user.id = str(uuid4())
        self._users.append(user)
        return user

    async def update_user(self, user: User) -> None:
        """
        Updates user with matching id or throws an exception

        Parameters
        ----------
        user : User
            User data

        Raises
        ------
        ValueNotFoundError
            Can't update user with provided data

        """
        try:
            index: int = self._users.index(user)
            self._users[index] = user
        except ValueError:
            raise ValueNotFoundError("No user found")

    async def delete_user(self, user_id: str) -> None:
        """
        Deletes user with matching id or throws an exception

        Parameters
        ----------
        user_id : str
            User's id

        Raises
        ------
        ValueNotFoundError
            Can't delete user with provided data

        """
        try:
            index = next(
                i
                for i in range(len(self._users))
                if self._users[i].id == user_id and self._users[i].suspended_at is None
            )
            self._users[index].suspended_at = datetime.now()
        except StopIteration:
            raise ValueNotFoundError("No user found")

    async def get_all_users(self, page: int, items_per_page: int) -> List[User]:
        """
        Returns all existing users

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

        """
        result = (
            self._users[(page - 1) * items_per_page : page * items_per_page]
            if items_per_page != -1
            else self._users
        )
        if len(result) == 0:
            raise ValueNotFoundError("No users found")
        return result

    async def get_user_by_session_id(self, session_id: str) -> User:
        """
        Get user with matching session id

        Parameters
        ----------
        session_id : str
            Id of the session

        Returns
        -------
        User
            User that has provided session_id

        Raises
        ------
        ValueNotFoundError
            User or token does not exist
        InvalidTokenError
            Refresh token is invalid

        """
        token = await MockTokenRepositoryImpl().get_refresh_token(session_id)
        user_id, _ = JwtController().decode(token, TokenType.REFRESH_TOKEN)
        return await self.get_user_by_id(user_id)
