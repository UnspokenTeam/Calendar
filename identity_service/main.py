import logging
import asyncio
import grpc

import generated.identity_service_pb2_grpc as identity_service_grpc
from src.identity_service_impl import IdentityServiceImpl


async def serve():
    """Start an async server"""
    server = grpc.aio.server()
    identity_service_grpc.add_IdentityServiceServicer_to_server(
        IdentityServiceImpl(), server
    )
    server.add_insecure_port("0.0.0.0:8080")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(serve())
