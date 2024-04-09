# mypy: ignore-errors
"""Interceptor decorator"""
from typing import Any, Callable
import logging

import grpc

from prisma.errors import PrismaError

from errors.invalid_token_error import InvalidTokenError
from errors.permission_denied import PermissionDeniedError
from errors.unique_error import UniqueError
from errors.value_not_found_error import ValueNotFoundError

from grpc_interceptor.server import AsyncServerInterceptor


class CustomInterceptor(AsyncServerInterceptor):
    async def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        context: grpc.ServicerContext,
        _: str,
    ) -> Any:
        try:
            return await method(request_or_iterator, context)
        except PrismaError as p_error:
            logging.error(f"Prisma error: {p_error}")
            await context.abort(grpc.StatusCode.UNKNOWN, "Prisma error: Unknown error happened")
        except ValueNotFoundError as value_not_found_error:
            logging.error(value_not_found_error)
            await context.abort(grpc.StatusCode.NOT_FOUND, str(value_not_found_error))
        except InvalidTokenError as invalid_token_error:
            logging.error(invalid_token_error)
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, str(invalid_token_error))
        except UniqueError as unique_error:
            logging.error(unique_error)
            await context.abort(grpc.StatusCode.ALREADY_EXISTS, str(unique_error))
        except PermissionDeniedError as permission_denied_error:
            logging.error(permission_denied_error)
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, str(permission_denied_error))
