import logging
import asyncio
import sys

import grpc

import proto.event_service_pb2_grpc as event_service_grpc
from db.postgres_client import PostgresClient
from src.event_service_impl import EventServiceImpl


async def serve() -> None:
    """Start an async server."""
    server = grpc.aio.server()
    event_service_grpc.add_EventServiceServicer_to_server(EventServiceImpl(), server)
    server.add_insecure_port("0.0.0.0:8081")
    await PostgresClient().connect()
    await server.start()
    logging.info("Server started on http://localhost:8081")
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)]
    )
    asyncio.run(serve())
