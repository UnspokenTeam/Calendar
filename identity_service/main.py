import logging
import asyncio
import sys

import grpc

import generated.identity_service_pb2_grpc as identity_service_grpc
from db.db import Db
from db.redis_client import RedisClient
from src.identity_service_impl import IdentityServiceImpl


async def serve():
    """Start an async server"""
    server = grpc.aio.server()
    identity_service_grpc.add_IdentityServiceServicer_to_server(
        IdentityServiceImpl(), server
    )
    server.add_insecure_port("0.0.0.0:8080")
    await Db().connect()
    RedisClient()
    await server.start()
    logging.info("Server started on http://localhost:8080")
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)]
    )
    asyncio.run(serve())
