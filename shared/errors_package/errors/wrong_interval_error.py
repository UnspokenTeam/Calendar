"""Wrong interval error type"""


class WrongIntervalError(Exception):
    """Exception raised when user gives wrong time interval."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Wrong interval error: {message}")
