"""Jwt controller"""

from enum import Enum
from typing import Tuple
import datetime
import os

from errors import InvalidTokenError
from utils import singleton

from jwt import decode, encode
from jwt.exceptions import DecodeError, ExpiredSignatureError


class TokenType(Enum):
    """Token type enum"""

    ACCESS_TOKEN = 1
    """Access token type"""
    REFRESH_TOKEN = 2
    """Refresh token type"""


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
    generate_access_token(user_id, session_id)
        Generate access token for provided user id and session id
    generate_refresh_token(user_id, session_id)
        Generate refresh token for provided user id and session id
    decode(token, token_type)
        Decode token with provided type or throw an error

    """

    _access_key: str
    _refresh_key: str

    def __init__(self) -> None:
        self._access_key = os.environ["ACCESS_SECRET"]
        self._refresh_key = os.environ["REFRESH_SECRET"]

    def generate_access_token(self, user_id: str, session_id: str) -> str:
        """
        Generate access token for provided user id and session id

        Parameters
        ----------
        user_id: str
            User's id
        session_id : str
            Id of the current session

        Returns
        -------
        str
            Access token

        """
        access_token: str = encode(
            {
                "user_id": user_id,
                "session_id": session_id,
                "exp": datetime.datetime.now()
                + datetime.timedelta(
                    minutes=int(os.environ["ACCESS_TOKEN_EXPIRATION"])
                ),
            },
            self._access_key,
            algorithm="HS256",
        )
        return access_token

    def generate_refresh_token(self, user_id: str, session_id: str) -> str:
        """
        Generate refresh token for provided user id and session id

        Parameters
        ----------
        user_id: str
            User's id
        session_id : str
            Id of the current session

        Returns
        -------
        str
            Refresh token

        """
        refresh_token: str = encode(
            {
                "user_id": user_id,
                "session_id": session_id,
                "exp": datetime.datetime.now()
                + datetime.timedelta(days=int(os.environ["REFRESH_TOKEN_EXPIRATION"])),
            },
            self._refresh_key,
            algorithm="HS256",
        )
        return refresh_token

    def decode(self, token: str, token_type: TokenType) -> Tuple[str, str]:
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
        Tuple[str, str]
            User's id and session id

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
            data = dict(
                decode(
                    jwt=token,
                    key=key,
                    algorithms=[
                        "HS256",
                    ],
                )
            )
            return str(data["user_id"]), str(data["session_id"])
        except DecodeError:
            raise InvalidTokenError("Invalid token")
        except ExpiredSignatureError:
            raise InvalidTokenError("Invalid token")
