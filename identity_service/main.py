import logging
from concurrent import futures

import grpc

import proto.identity_service_pb2_grpc as identity_service_grpc
from src.identity_service_impl import IdentityServiceImpl

if __name__ == '__main__':
    logging.basicConfig()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    identity_service_grpc.add_IdentityServiceServicer_to_server(IdentityServiceImpl(), server)
    server.add_insecure_port("0.0.0.0:8080")
    server.start()
    server.wait_for_termination()
