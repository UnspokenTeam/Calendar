"""Permission denied error type"""


class PermissionDeniedError(Exception):
    """Exception raised when the permission is denied"""

    def __init__(self, message: str) -> None:
        super().__init__(f"Permission denied error: {message}")