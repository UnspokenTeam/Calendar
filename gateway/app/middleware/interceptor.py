from grpc import RpcError, StatusCode

from app.errors import PermissionDeniedError, RateLimitError

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from starlette.types import ASGIApp


class InterceptorMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except RpcError as e:
            match (e.code()):
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
                case _:
                    return JSONResponse(
                        status_code=500, content={"message": "Internal server error"}
                    )
        except PermissionDeniedError:
            return JSONResponse(
                status_code=403, content={"message": "Permission denied"}
            )
        except RateLimitError as rate_limit_error:
            return JSONResponse(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                content={"message": "Too Many Requests"},
                headers={"Retry-After": str(rate_limit_error.retry_after)},
            )
