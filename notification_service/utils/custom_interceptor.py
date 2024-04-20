# mypy: ignore-errors
"""Interceptor decorator"""
from typing import Any, Callable
import logging

import grpc

from prisma.errors import PrismaError

from errors.permission_denied_error import PermissionDeniedError
from errors.value_not_found_error import ValueNotFoundError

from grpc_interceptor.server import AsyncServerInterceptor


class CustomInterceptor(AsyncServerInterceptor):
    """
    GRPC Interceptor class for Error Handling.

    Methods
    -------
    async intercept(method, request_or_iterator, context, _)
        Handles exceptions and returns method call.

    """

    async def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        context: grpc.ServicerContext,
        _: str,
    ) -> Any:
        """
        Custom interceptor

        Parameters
        ----------
        method: Either the RPC method implementation, or the next interceptor in
                the chain.
        request_or_iterator: The RPC request, as a protobuf message if it is a
            unary request, or an iterator of protobuf messages if it is a streaming
            request.
        context: The ServicerContext pass by gRPC to the service.
        _: A string of the form "/protobuf.package.Service/Method"

        Returns
        -------
        Returns the result of method(request_or_iterator)

        """
        try:
            return await method(request_or_iterator, context)
        except PrismaError as p_error:
            logging.error(f"Prisma error: {p_error}")
            await context.abort(
                grpc.StatusCode.UNKNOWN, "Prisma error: Unknown error happened"
            )
        except ValueNotFoundError as value_not_found_error:
            logging.error(value_not_found_error)
            await context.abort(grpc.StatusCode.NOT_FOUND, str(value_not_found_error))
        except PermissionDeniedError as permission_denied_error:
            logging.error(permission_denied_error)
            await context.abort(
                grpc.StatusCode.PERMISSION_DENIED, str(permission_denied_error)
            )
