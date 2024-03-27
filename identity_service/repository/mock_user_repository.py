from typing import List
from uuid import uuid4

from errors.unique_error import UniqueError
from repository.user_repository_interface import UserRepositoryInterface
from src.models.user import User


class MockUserRepositoryImpl(UserRepositoryInterface):
    """
    Data class that stores user information

    Attributes
    ----------
    users: List[User]
        List of users

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

    users: List[User]

    def __init__(self):
        self.users = []

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
        ValueError
            User does not exist
        """
        return [user for user in self.users if user.email == email][0]

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
        ValueError
            User does not exist

        """
        return [user for user in self.users if user.id == user_id][0]

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

        """
        return [user for user in self.users if user.id in user_ids]

    async def create_user(self, user: User) -> None:
        """
        Creates user with matching data or throws an exception

        Parameters
        ----------
        user : User
            User data

        Raises
        ------
        UniqueError
            Another user with this data already exists

        """
        if (
            len(
                [
                    True
                    for userdb in self.users
                    if userdb.username == user.username and user.email == userdb.email
                ]
            )
            != 0
        ):
            raise UniqueError("User with this data already exists")

        user.id = uuid4()
        self.users.append(user)

    async def update_user(self, user: User) -> None:
        """
        Updates user with matching id or throws an exception

        Parameters
        ----------
        user : User
            User data

        Raises
        ------
        ValueError
            Can't update user with provided data

        """
        index: int = self.users.index(user)
        self.users[index] = user

    async def delete_user(self, user_id: str) -> None:
        """
        Deletes user with matching id or throws an exception

        Parameters
        ----------
        user_id : str
            User's id

        Raises
        ------
        ValueError
            Can't delete user with provided data

        """
        index: int = [i for i in range(len(self.users)) if self.users[i].id == user_id][
            0
        ]
        self.users.pop(index)
