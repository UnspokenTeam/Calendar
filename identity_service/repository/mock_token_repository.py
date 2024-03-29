"""Mock token repository"""
from errors.value_not_found_error import ValueNotFoundError
from repository.token_repository_interface import TokenRepositoryInterface


class MockTokenRepositoryImpl(TokenRepositoryInterface):
    """
    Mock class for manipulating with token data

    Attributes
    ----------
    _tokens: dict[str, str]
        Dictionary with pairs of [user_id, refresh_token]

    Methods
    -------
    async get_refresh_token(user_id)
        Returns refresh token for provided user_id
    async store_refresh_token(refresh_token)
        Stores refresh token in Redis database
    async delete_refresh_token(user_id)
        Deletes refresh token corresponding to provided user_id

    """

    _tokens: dict[str, str]

    def __init__(self) -> None:
        self._tokens = {}

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
        self._tokens[session_id] = refresh_token

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
        result = self._tokens.get(session_id)

        if result is None:
            raise ValueNotFoundError("Token not found")

        return result

    async def delete_refresh_token(self, session_id: str) -> None:
        """
        Delete user's refresh token

        Parameters
        ----------
        session_id : str
            Id of the current session

        """
        if session_id in self._tokens:
            self._tokens.pop(session_id)
