"""Tokens repository"""
from db.postgres_client import PostgresClient
from errors.value_not_found_error import ValueNotFoundError
from utils.singleton import singleton

from repository.token_repository_interface import TokenRepositoryInterface


@singleton
class TokenRepositoryImpl(TokenRepositoryInterface):
    """
    Class for manipulating with token data

    Attributes
    ----------
    _postgres_client : PostgresClient
        Postgres client instance

    Methods
    -------
    async get_refresh_token(user_id)
        Returns refresh token for provided user_id
    async store_refresh_token(refresh_token)
        Stores refresh token in Redis database
    async delete_refresh_token(user_id)
        Deletes refresh token corresponding to provided user_id
    async delete_all_refresh_tokens(user_id)
        Delete all user's refresh tokens
    """

    _postgres_client: PostgresClient

    def __init__(self) -> None:
        self._postgres_client = PostgresClient()

    async def store_refresh_token(
        self, refresh_token: str, session_id: str, user_id: str
    ) -> None:
        """
        Create refresh token with provided data

        Parameters
        ----------
        user_id
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
        await self._postgres_client.db.token.create(
            data={"id": session_id, "token": refresh_token, "user_id": user_id}
        )

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
        result = await self._postgres_client.db.token.find_first(
            where={"id": session_id}
        )

        if result is None:
            raise ValueNotFoundError("Token not found")

        return str(result.token)

    async def delete_refresh_token(self, session_id: str) -> None:
        """
        Delete user's refresh token

        Parameters
        ----------
        session_id : str
            Id of the current session

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        await self._postgres_client.db.token.delete(where={"id": session_id})

    async def delete_all_refresh_tokens(self, user_id: str) -> None:
        """
        Delete all user's refresh tokens

        Parameters
        ----------
        user_id
            Id of the user

        Raises
        ------
        prisma.errors.PrismaError
            Catch all for every exception raised by Prisma Client Python

        """
        await self._postgres_client.db.token.delete_many(where={"user_id": user_id})
