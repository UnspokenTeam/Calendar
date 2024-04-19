"""Grpc client parameters"""
from os import environ

from app.generated.identity_service.identity_service_pb2_grpc import IdentityServiceStub

from ..generated.event_service.event_service_pb2_grpc import EventServiceStub
from ..generated.invite_service.invite_service_pb2_grpc import InviteServiceStub
from ..grpc_client import GrpcClient


class GrpcClientParams:
    """
    Grpc client handler

    Attributes
    ----------
    identity_service_client : GrpcClient[IdentityServiceStub]
        Grpc client for identity service
    event_service_client : GrpcClient[EventServiceStub]
        Grpc client for event service
    invite_service_client : GrpcClient[InviteServiceStub]
        Grpc client for invite service

    """

    identity_service_client: GrpcClient[IdentityServiceStub]
    event_service_client: GrpcClient[EventServiceStub]
    invite_service_client: GrpcClient[InviteServiceStub]

    def __init__(self) -> None:
        try:
            self.identity_service_client = GrpcClient[IdentityServiceStub](
                host=environ["IDENTITY_SERVICE_HOST"],
                port=int(environ["IDENTITY_SERVICE_PORT"]),
                stub=IdentityServiceStub,
            )
            self.event_service_client = GrpcClient[EventServiceStub](
                host=environ["EVENT_SERVICE_HOST"],
                port=int(environ["EVENT_SERVICE_PORT"]),
                stub=EventServiceStub,
            )
            self.invite_service_client = GrpcClient[InviteServiceStub](
                host=environ["INVITE_SERVICE_HOST"],
                port=int(environ["INVITE_SERVICE_PORT"]),
                stub=InviteServiceStub,
            )
        except KeyError as e:
            raise Exception(f"Missing environment variable: {e}")
