"""Mock token repository"""
from errors.value_not_found_error import ValueNotFoundError
from repository.token_repository_interface import TokenRepositoryInterface
from utils.singleton import singleton


@singleton
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
        user_id
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
        result = None

        for user in self._tokens.values():
            if session_id in user:
                result = user[session_id]
                break

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
        for user_id, user_tokens in self._tokens.items():
            if session_id in user_tokens:
                self._tokens[user_id].pop(session_id)
                break

    async def delete_all_refresh_tokens(self, user_id: str) -> None:
        try:
            self._tokens.pop(user_id)
        except KeyError:
            raise ValueNotFoundError("Token not found")
