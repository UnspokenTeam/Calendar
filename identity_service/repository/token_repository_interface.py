"""Token repository interface"""
# mypy: ignore-errors


class TokenRepositoryInterface:
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
        pass

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
        pass

    async def delete_refresh_token(self, user_id: str) -> None:
        """
        Delete user's refresh token

        Parameters
        ----------
        user_id : str
            User's id

        """
        pass
