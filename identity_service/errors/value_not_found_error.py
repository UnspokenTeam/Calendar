"""Value not found error type"""


class ValueNotFoundError(Exception):
    """Exception raised when value was not found in the database"""

    def __init__(self, message: str) -> None:
        super().__init__(f"ValueNotFound error: {message}")
