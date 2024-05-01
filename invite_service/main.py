import asyncio
import logging
import os
import sys

import grpc

from db.postgres_client import PostgresClient
from src.invite_service_impl import InviteServiceImpl
from utils.custom_interceptor import CustomInterceptor

from repository.invite_repository_impl import InviteRepositoryImpl
from repository.mock_invite_repository import MockInviteRepositoryImpl
import generated.invite_service.invite_service_pb2_grpc as invite_service_grpc


async def serve() -> None:
    """Start an async server"""
    server = grpc.aio.server(interceptors=[CustomInterceptor()])
    if os.environ["ENVIRONMENT"] == "PRODUCTION":
        await PostgresClient().connect()
    invite_service_grpc.add_InviteServiceServicer_to_server(
        InviteServiceImpl(
            invite_repository=InviteRepositoryImpl()
            if os.environ["ENVIRONMENT"] == "PRODUCTION"
            else MockInviteRepositoryImpl()
        ),
        server,
    )
    server.add_insecure_port("0.0.0.0:8082")
    await server.start()
    logging.info(f"Server started on http://localhost:8082 with environment ${os.environ['ENVIRONMENT']}")
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
