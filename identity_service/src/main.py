import asyncio
import logging
import os
import sys

import grpc

from db import PostgresClient
from src.identity_service_impl import IdentityServiceImpl
from src.repository import MockTokenRepositoryImpl, MockUserRepositoryImpl, TokenRepositoryImpl, UserRepositoryImpl
from src.utilities import CustomInterceptor, JwtController
import src.generated.identity_service.identity_service_pb2_grpc as identity_service_grpc

import dotenv


async def serve() -> None:
    """Start an async server"""
    server = grpc.aio.server(interceptors=[CustomInterceptor()])
    dotenv.load_dotenv()
    if os.environ["ENVIRONMENT"] == "PRODUCTION":
        await PostgresClient().connect()
    identity_service_grpc.add_IdentityServiceServicer_to_server(
        IdentityServiceImpl(
            user_repository=UserRepositoryImpl()
            if os.environ["ENVIRONMENT"] == "PRODUCTION"
            else MockUserRepositoryImpl(),
            token_repository=TokenRepositoryImpl()
            if os.environ["ENVIRONMENT"] == "PRODUCTION"
            else MockTokenRepositoryImpl(),
        ),
        server,
    )
    server.add_insecure_port("0.0.0.0:8080")
    JwtController()
    await server.start()
    logging.info(
        f"Server started on http://localhost:8080 with environment {os.environ['ENVIRONMENT']}"
    )
    await server.wait_for_termination()


async def handle_serve_error() -> None:
    """Handle server stop"""
    try:
        await serve()
    except asyncio.CancelledError:
        logging.info("Server stopped")
    finally:
        await PostgresClient().disconnect()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)]
    )
    asyncio.run(handle_serve_error())
