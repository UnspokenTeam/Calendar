"""Token repository interface"""
from abc import ABC, abstractmethod


class TokenRepositoryInterface(ABC):
    """
    Interface for class for manipulating with user data

    Methods
    -------
    async get_refresh_token(user_id)
        Returns refresh token for provided user_id
    async store_refresh_token(refresh_token)
        Stores refresh token in Redis database
    async delete_refresh_token(user_id)
        Deletes refresh token corresponding to provided user_id

    """

    @abstractmethod
    async def store_refresh_token(
        self, refresh_token: str, session_id: str, user_id: str
    ) -> None:
        """
        Create refresh token with provided data

        Parameters
        ----------
        user_id : str
            Id of the current user
        refresh_token : str
            User's refresh token
        session_id : str
            Id of the current session

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        pass

    @abstractmethod
    async def get_refresh_token(self, session_id: str) -> str:
        """
        Get user's refresh token

        Parameters
        ----------
        session_id : str
            Id of the current session

        Returns
        -------
        str
            User's refresh token

        Raises
        ------
        ValueNotFoundError
            No refresh token found for provided user_id
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        pass

    @abstractmethod
    async def delete_refresh_token(self, session_id: str) -> None:
        """
        Delete user's refresh token with provided session_id

        Parameters
        ----------
        session_id : str
            Id of the current session

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        pass

    @abstractmethod
    async def delete_all_refresh_tokens(self, user_id: str) -> None:
        """
        Delete all user's refresh tokens

        Parameters
        ----------
        user_id : str
            Id of the current user

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        pass
