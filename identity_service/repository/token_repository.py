"""Tokens repository"""
import os
from datetime import timedelta
from typing import Optional

from db.redis_client import RedisClient


class TokenRepository:
    """
    Data class that stores user information

    Attributes
    ----------
    _redis_db : RedisClient
        Redis client instance

    Methods
    -------
    get_refresh_token(user_id)
        Returns refresh token for provided user_id
    store_refresh_token(refresh_token)
        Stores refresh token in Redis database
    delete_refresh_token(user_id)
        Deletes refresh token corresponding to provided user_id
    """

    _redis_db: RedisClient

    def __init__(self) -> None:
        self._redis_db = RedisClient()

    def store_refresh_token(self, refresh_token: str, user_id: str) -> None:
        """
        Create refresh token with provided data

        Parameters
        ----------
        refresh_token : str
            User's refresh token
        user_id : str
            User's id
        """
        self._redis_db.db.set(
            user_id,
            refresh_token,
            ex=timedelta(days=int(os.environ.get("REFRESH_TOKEN_EXPIRATION"))),
        )

    def get_refresh_token(self, user_id: str) -> str:
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
        """
        result: Optional[bytes] = self._redis_db.db.get(user_id)

        if result is None:
            raise ValueError("Token not found")

        return result.decode()

    def delete_refresh_token(self, user_id: str) -> None:
        """
        Delete user's refresh token

        Parameters
        ----------
        user_id : str
            User's id
        """
        self._redis_db.db.delete(user_id)
