"""Mock token repository"""

from components.errors import ValueNotFoundError
from components.utils import singleton
from repository.token_repository_interface import TokenRepositoryInterface


@singleton
class MockTokenRepositoryImpl(TokenRepositoryInterface):
    """
    Mock class for manipulating with token data

    Attributes
    ----------
    _tokens: dict[str, dict[str, str]]
        Dictionary with pairs of [user_id, dict[session_id, refresh_token]]

    Methods
    -------
    async get_refresh_token(session_id)
        Returns refresh token for provided session_id
    async store_refresh_token(refresh_token, session_id, user_id)
        Stores refresh token
    async delete_refresh_token(session_id)
        Deletes refresh token corresponding to provided session_id
    async delete_all_refresh_tokens(user_id)
        Deletes all user's refresh tokens

    """

    _tokens: dict[str, dict[str, str]]

    def __init__(self) -> None:
        self._tokens = {}

    async def store_refresh_token(
        self, refresh_token: str, session_id: str, user_id: str
    ) -> None:
        """
        Create refresh token with provided data

        Parameters
        ----------
        refresh_token : str
            User's refresh token
        session_id : str
            Id of the current session
        user_id : str
            Id of the current user

        """
        value = self._tokens.get(user_id)
        if value is None:
            self._tokens[user_id] = {}
        self._tokens[user_id][session_id] = refresh_token

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
        try:
            return next(
                user[session_id] for user in self._tokens.values() if session_id in user
            )
        except StopIteration:
            raise ValueNotFoundError("Token not found")

    async def delete_refresh_token(self, session_id: str) -> None:
        """
        Delete user's refresh token

        Parameters
        ----------
        session_id : str
            Id of the current session

        Raises
        ------
        ValueNotFoundError
            Refresh token does not exist

        """
        for user_id, user_tokens in self._tokens.items():
            if session_id in user_tokens:
                self._tokens[user_id].pop(session_id)
                return

        raise ValueNotFoundError("Token not found")

    async def delete_all_refresh_tokens(self, user_id: str) -> None:
        """
        Delete all user's refresh tokens

        Parameters
        ----------
        user_id : str
            Id of the current user

        Raises
        ------
        ValueNotFoundError
            User does not exist or does not have any refresh tokens

        """
        try:
            self._tokens.pop(user_id)
        except KeyError:
            raise ValueNotFoundError("User not found")
