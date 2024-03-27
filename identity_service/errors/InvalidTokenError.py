"""Invalid token error type"""


class InvalidTokenError(Exception):
    """Exception raised when the token is invalid"""

    def __init__(self, message: str) -> None:
        super().__init__(f"Invalid token error: {message}")
