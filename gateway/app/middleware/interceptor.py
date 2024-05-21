"""Interceptor middleware"""
import logging

from grpc import RpcError, StatusCode

from errors import PermissionDeniedError, RateLimitError, UnauthenticatedError

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from starlette.types import ASGIApp


class InterceptorMiddleware(BaseHTTPMiddleware):
    """Interceptor middleware"""

    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Handle errors

        Parameters
        ----------
        request : Request
            Request object
        call_next : RequestResponseEndpoint
            Next function to call

        Returns
        -------
        Response
            Response

        """
        try:
            return await call_next(request)
        except RpcError as e:
            logging.error(f"Code - {e.code()}. Details - {e.details()}")
            match (e.code()):
                case StatusCode.ALREADY_EXISTS:
                    return JSONResponse(
                        status_code=400, content={"message": "Already exists"}
                    )
                case StatusCode.PERMISSION_DENIED:
                    return JSONResponse(
                        status_code=403, content={"message": "Permission denied"}
                    )
                case StatusCode.UNKNOWN | StatusCode.INTERNAL | StatusCode.UNAVAILABLE:
                    return JSONResponse(
                        status_code=500, content={"message": "Internal server error"}
                    )
                case StatusCode.UNAUTHENTICATED:
                    return JSONResponse(
                        status_code=401, content={"message": "Unauthorized"}
                    )
                case StatusCode.NOT_FOUND:
                    return JSONResponse(
                        status_code=404, content={"message": "Not found"}
                    )
                case StatusCode.CANCELLED:
                    return JSONResponse(
                        status_code=400, content={"message": "Request was cancelled"}
                    )
                case _:
                    return JSONResponse(
                        status_code=500, content={"message": "Internal server error"}
                    )
        except UnauthenticatedError as unauthenticated_error:
            logging.error(unauthenticated_error)
            return JSONResponse(
                status_code=401,
                content={"message": "Unauthenticated"},
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*"
                }
            )
        except PermissionDeniedError as permission_denied_error:
            logging.error(permission_denied_error)
            return JSONResponse(
                status_code=403, content={"message": "Permission denied"}
            )
        except RateLimitError as rate_limit_error:
            return JSONResponse(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                content={"message": "Too Many Requests"},
                headers={
                    "Retry-After": str(rate_limit_error.retry_after),
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*"
                },
            )
        except ValueError as value_error:
            logging.error(value_error)
            return JSONResponse(
                status_code=422, content={"message": f"Bad Request {value_error}"}
            )
