"""Tokens repository"""
import os
from datetime import timedelta
from typing import Optional

from db.redis_client import RedisClient
from errors.value_not_found_error import ValueNotFoundError
from utils.singleton import singleton


@singleton
class TokenRepository:
    """
    Data class that stores user information

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

    async def store_refresh_token(self, refresh_token: str, user_id: str) -> None:
        """
        Create refresh token with provided data

        Parameters
        ----------
        refresh_token : str
            User's refresh token
        user_id : str
            User's id

        """
        await self._redis_db.db.set(
            user_id,
            refresh_token,
            ex=timedelta(days=int(os.environ.get("REFRESH_TOKEN_EXPIRATION"))),
        )

    async def get_refresh_token(self, user_id: str) -> str:
        """
        Get user's refresh token

        Parameters
        ----------
        user_id : str
            User's id

        Returns
        -------
        str
            User's refresh token
        Raises
        ------
        ValueNotFoundError
            No refresh token found for provided user_id

        """
        result: Optional[bytes] = await self._redis_db.db.get(user_id)

        if result is None:
            raise ValueNotFoundError("Token not found")

        return result.decode()

    async def delete_refresh_token(self, user_id: str) -> None:
        """
        Delete user's refresh token

        Parameters
        ----------
        user_id : str
            User's id

        """
        await self._redis_db.db.delete(user_id)
