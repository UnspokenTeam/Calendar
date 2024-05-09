import asyncio
import logging
import os
import sys

import grpc

from src.event_service_impl import EventServiceImpl
from utilities.custom_interceptor import CustomInterceptor

from db_package.db import PostgresClient
from repository.event_repository_impl import EventRepositoryImpl
from repository.mock_event_repository import MockEventRepositoryImpl
import generated.event_service.event_service_pb2_grpc as event_service_grpc


async def serve() -> None:
    """Start an async server."""
    server = grpc.aio.server(interceptors=[CustomInterceptor()])
    if os.environ["ENVIRONMENT"] == "PRODUCTION":
        await PostgresClient().connect()
    event_service_grpc.add_EventServiceServicer_to_server(
        EventServiceImpl(
            event_repository=EventRepositoryImpl()
            if os.environ["ENVIRONMENT"] == "PRODUCTION"
            else MockEventRepositoryImpl()
        ),
        server=server,
    )
    server.add_insecure_port("0.0.0.0:8081")
    await server.start()
    logging.info(
        "Server started on http://localhost:8081 with environment "
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
