import asyncio
import logging
import sys

import grpc

from db.postgres_client import PostgresClient
from db.redis_client import RedisClient
from src.identity_service_impl import IdentityServiceImpl
from utils.jwt_controller import JwtController

import dotenv
import generated.identity_service_pb2_grpc as identity_service_grpc


async def serve() -> None:
    """Start an async server"""
    server = grpc.aio.server()
    identity_service_grpc.add_IdentityServiceServicer_to_server(
        IdentityServiceImpl(), server
    )
    server.add_insecure_port("0.0.0.0:8080")
    await PostgresClient().connect()
    await RedisClient().connect()
    dotenv.load_dotenv()
    JwtController()
    await server.start()
    logging.info("Server started on http://localhost:8080")
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)]
    )
    asyncio.run(serve())
