import asyncio
import logging
import sys

import grpc

from src.invite_service_impl import InviteServiceImpl

import generated.invite_service.invite_service_pb2_grpc as invite_service_grpc


async def serve() -> None:
    """Start an async server"""
    server = grpc.aio.server()
    invite_service_grpc.add_InviteServiceServicer_to_server(InviteServiceImpl(), server)
    server.add_insecure_port("0.0.0.0:8082")
    await server.start()
    logging.info("Server started on http://localhost:8082")
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)]
    )
    asyncio.run(serve())
