import logging
import grpc
from concurrent import futures

import proto.event_service_pb2_grpc as event_service_grpc
from src.event_service_impl import EventServiceImpl

if __name__ == "__main__":
    logging.basicConfig()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    event_service_grpc.add_EventServiceServicer_to_server(EventServiceImpl(), server)
    server.add_insecure_port("0.0.0.0:8081")
    server.start()
    server.wait_for_termination()
