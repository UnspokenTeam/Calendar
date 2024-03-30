"""Jwt controller"""
from enum import Enum
from typing import Tuple
import datetime
import logging
import os

from errors.InvalidTokenError import InvalidTokenError
from utils.singleton import singleton

from jwt import decode, encode


class TokenType(Enum):
    """Token type enum"""

    ACCESS_TOKEN = 1
    REFRESH_TOKEN = 2


@singleton
class JwtController:
    """
    Class to work with jwt

    Attributes
    ----------
    _access_key : str
        Key to generate access token
    _refresh_key : str
        Key to generate refresh token

    Methods
    -------
    generate(user_id)
        Generate access and refresh tokens for user with provided id
    decode(token, token_type)
        Decode token with provided type or throw an error

    """

    _access_key: str
    _refresh_key: str

    def __init__(self) -> None:
        self._access_key = os.environ["ACCESS_SECRET"]
        self._refresh_key = os.environ["REFRESH_SECRET"]

    def generate(self, user_id: str) -> Tuple[str, str]:
        """
        Generate access and refresh tokens for user with provided id

        Parameters
        ----------
        user_id: str
            User's id

        Returns
        -------
        Tuple[str, str]
            Access and refresh tokens

        """
        access_token = encode(
            {
                "user_id": user_id,
                "exp": datetime.datetime.now() + datetime.timedelta(days=3),
            },
            self._access_key,
            algorithm="HS256",
        )
        refresh_token = encode(
            {
                "user_id": user_id,
                "exp": datetime.datetime.now() + datetime.timedelta(days=3),
            },
            self._refresh_key,
            algorithm="HS256",
        )
        return access_token, refresh_token

    def decode(self, token: str, token_type: TokenType) -> dict[str, str]:
        """
        Decode token with provided type or throw an error

        Parameters
        ----------
        token: str
            Token to decode
        token_type: TokenType
            Token type

        Returns
        -------
        dict[str, str]
            Decoded data inside token

        Raises
        ------
        InvalidTokenError
            Token is invalid

        """
        key = (
            self._access_key
            if token_type == TokenType.ACCESS_TOKEN
            else self._refresh_key
        )
        try:
            return dict(
                decode(
                    jwt=token,
                    key=key,
                    algorithms=[
                        "HS256",
                    ],
                )
            )
        except Exception as e:
            logging.info(e)
            raise InvalidTokenError("Invalid token")
