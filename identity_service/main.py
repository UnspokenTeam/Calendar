from asyncio.exceptions import CancelledError
import asyncio
import logging
import sys

import grpc

from db.postgres_client import PostgresClient
from src.identity_service_impl import IdentityServiceImpl
from utils.custom_interceptor import CustomInterceptor
from utils.jwt_controller import JwtController

from repository.token_repository_impl import TokenRepositoryImpl
from repository.user_repository_impl import UserRepositoryImpl
import dotenv
import generated.identity_service_pb2_grpc as identity_service_grpc


async def serve() -> None:
    """Start an async server"""
    server = grpc.aio.server(interceptors=[CustomInterceptor()])
    dotenv.load_dotenv()
    await PostgresClient().connect()
    identity_service_grpc.add_IdentityServiceServicer_to_server(
        IdentityServiceImpl(
            user_repository=UserRepositoryImpl(),
            token_repository=TokenRepositoryImpl(),
        ),
        server,
    )
    server.add_insecure_port("0.0.0.0:8080")
    JwtController()
    await server.start()
    logging.info("Server started on http://localhost:8080")
    await server.wait_for_termination()


async def handle_serve_error() -> None:
    """Handle server stop"""
    try:
        await serve()
    except CancelledError:
        logging.info("Server stopped")
    finally:
        await PostgresClient().disconnect()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)]
    )
    asyncio.run(handle_serve_error())
