"""Unauthorized error"""


class UnauthorizedError(Exception):
    """Exception raised when the user is unauthorized to access the page"""

    def __init__(self, message: str) -> None:
        super().__init__(f"Unauthorized error: {message}")
