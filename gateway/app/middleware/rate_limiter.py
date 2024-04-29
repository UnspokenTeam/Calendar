from math import ceil

from starlette.requests import Request
from starlette.responses import Response

from app.errors import RateLimitError


async def handler(
        _: Request, __: Response, pexpire: int
):
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

    Returns
    -------

    """
    expire = ceil(pexpire / 1000)

    raise RateLimitError(message="Too Many Requests", retry_after=expire)
