from typing import Generic, TypeVar

from grpc import Channel, insecure_channel

T = TypeVar('T')


class GrpcClient(Generic[T]):
    host: str
    port: int
    channel: Channel
    stub: T

    def __init__(self, host: str, port: int, stub: T) -> None:
        self.host = host
        self.port = port
        self.channel = insecure_channel(f"{host}:{port}")
        self.stub = stub(self.channel)

    def request(self) -> T:
        return self.stub
