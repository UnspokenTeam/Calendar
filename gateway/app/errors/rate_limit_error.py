"""Rate limit error type"""


class RateLimitError(Exception):
    """
    Exception raised when the request is rate-limited

    Attributes
    ----------
    retry_after : int
        Time in seconds after which the rate limit has expired

    """
    retry_after: int

    def __init__(self, message: str, retry_after: int) -> None:
        super().__init__(f"Rate limit error: {message}")
        self.retry_after = retry_after
