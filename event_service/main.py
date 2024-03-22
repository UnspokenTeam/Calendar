import logging
import asyncio
import grpc

import proto.event_service_pb2_grpc as event_service_grpc
from db.db import Db
from src.event_service_impl import EventServiceImpl


async def serve():
    """Start an async server"""
    server = grpc.aio.server()
    event_service_grpc.add_EventServiceServicer_to_server(EventServiceImpl(), server)
    server.add_insecure_port("0.0.0.0:8081")
    await Db().connect()
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(serve())
