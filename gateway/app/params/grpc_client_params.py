from os import environ

from app.identity_service_proto.identity_service_pb2_grpc import IdentityServiceStub

from ..grpc_client import GrpcClient


class GrpcClientParams:
    identity_service_client: GrpcClient[IdentityServiceStub]
    # event_service_client: GrpcClient
    # invite_service_client: GrpcClient

    def __init__(self) -> None:
        try:
            self.identity_service_client = GrpcClient[IdentityServiceStub](
                host=environ["IDENTITY_SERVICE_HOST"],
                port=int(environ["IDENTITY_SERVICE_PORT"]),
                stub=IdentityServiceStub,
            )
            # self.event_service_client = GrpcClient(
            #     host=environ["EVENT_SERVICE_HOST"],
            #     port=int(environ["EVENT_SERVICE_PORT"]),
            #     stub=EventServiceStub,
            # )
            # self.invite_service_client = GrpcClient(
            #     host=environ["INVITE_SERVICE_HOST"],
            #     port=int(environ["INVITE_SERVICE_PORT"]),
            #     stub=InviteServiceStub,
            # )
        except KeyError as e:
            raise Exception(f"Missing environment variable: {e}")
