import asyncio
import logging
import os
import sys

import grpc

from db.postgres_client import PostgresClient
from src.notification_service_impl import NotificationServiceImpl
from utils.custom_interceptor import CustomInterceptor

from repository.mock_notification_repository import MockNotificationRepositoryImpl
from repository.notification_repository_impl import NotificationRepositoryImpl
import generated.notification_service.notification_service_pb2_grpc as notification_service_grpc


async def serve() -> None:
    """Start an async server."""
    server = grpc.aio.server(interceptors=[CustomInterceptor()])
    if os.environ["ENVIRONMENT"] == "PRODUCTION":
        await PostgresClient().connect()
    notification_service_grpc.add_NotificationServiceServicer_to_server(
        NotificationServiceImpl(
            notification_repository=(
                NotificationRepositoryImpl()
                if os.environ["ENVIRONMENT"] == "PRODUCTION"
                else MockNotificationRepositoryImpl()
            ),
        ),
        server=server,
    )
    server.add_insecure_port("0.0.0.0:8083")
    await server.start()
    logging.info(
        "Server started on http://localhost:8083 with environment "
        + os.environ["ENVIRONMENT"]
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
