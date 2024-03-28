"""Tokens repository"""
from datetime import timedelta
from typing import Optional
import os

from db.redis_client import RedisClient
from errors.value_not_found_error import ValueNotFoundError
from repository.token_repository_interface import TokenRepositoryInterface
from utils.singleton import singleton


@singleton
class TokenRepositoryImpl(TokenRepositoryInterface):
    """
    Class for manipulating with token data

    Attributes
    ----------
    _redis_db : RedisClient
        Redis client instance

    Methods
    -------
    async get_refresh_token(user_id)
        Returns refresh token for provided user_id
    async store_refresh_token(refresh_token)
        Stores refresh token in Redis database
    async delete_refresh_token(user_id)
        Deletes refresh token corresponding to provided user_id

    """

    _redis_db: RedisClient

    def __init__(self) -> None:
        self._redis_db = RedisClient()

    async def store_refresh_token(self, refresh_token: str, session_id: str) -> None:
        """
        Create refresh token with provided data

        Parameters
        ----------
        refresh_token : str
            User's refresh token
        session_id : str
            Id of the current session

        """
        await self._redis_db.db.set(
            session_id,
            refresh_token,
            ex=timedelta(days=int(os.environ["REFRESH_TOKEN_EXPIRATION"])),
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

        """
        result: Optional[bytes] = await self._redis_db.db.get(session_id)

        if result is None:
            raise ValueNotFoundError("Token not found")

        return result.decode()

    async def delete_refresh_token(self, session_id: str) -> None:
        """
        Delete user's refresh token

        Parameters
        ----------
        session_id : str
            Id of the current session

        """
        await self._redis_db.db.delete(session_id)
