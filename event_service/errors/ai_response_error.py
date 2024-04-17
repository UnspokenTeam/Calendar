"""AI response error class."""


class AiResponseError(Exception):
    """Exception raised when AI didn't send normal response."""

    def __init__(self, message: str) -> None:
        super().__init__(f"AI Response error: {message}.")
