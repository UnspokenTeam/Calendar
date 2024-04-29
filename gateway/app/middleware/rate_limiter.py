from math import ceil

from app.errors import RateLimitError

from starlette.requests import Request
from starlette.responses import Response


async def handler(_: Request, __: Response, pexpire: int) -> None:
    """
    Handle rate limiting error.

    Parameters
    ----------
    _ : Request
        The request object.
    __ : Response
        The response object.
    pexpire : int
        The remaining milliseconds.

    """
    expire = ceil(pexpire / 1000)

    raise RateLimitError(message="Too Many Requests", retry_after=expire)
