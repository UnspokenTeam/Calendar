"""Unauthenticated error type"""


class UnauthenticatedError(Exception):
    """Exception raised when the credentials are invalid"""

    def __init__(self, message: str) -> None:
        super().__init__(f"Unauthenticated error: {message}")
