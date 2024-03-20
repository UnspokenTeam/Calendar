import logging
import grpc
from concurrent import futures

import proto.invite_service_pb2_grpc as invite_service_grpc
from src.invite_service_impl import InviteServiceImpl

if __name__ == "__main__":
    logging.basicConfig()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    invite_service_grpc.add_InviteServiceServicer_to_server(InviteServiceImpl(), server)
    server.add_insecure_port("0.0.0.0:8082")
    server.start()
    server.wait_for_termination()