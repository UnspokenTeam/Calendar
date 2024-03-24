"""Unique error type"""


class UniqueError(Exception):
    """Exception raised when the new values violates a unique constraint"""

    def __init__(self, message: str) -> None:
        super().__init__(f"Unique error: {message}")
