"""Grpc client"""
# mypy: ignore-errors
from typing import Generic, TypeVar

from grpc import Channel, insecure_channel

T = TypeVar("T")


class GrpcClient(Generic[T]):
    """
    Grpc client

    Attributes
    ----------
    _host : str
        Server host
    _port: int
        Server port
    _channel : Channel
        Grpc channel
    _stub : T
        Generated grpc stub

    Methods
    -------
    request()
        Returns client to work with

    """

    _host: str
    _port: int
    _channel: Channel
    _stub: T

    def __init__(self, host: str, port: int, stub: type[T]) -> None:
        self._host = host
        self._port = port
        self._channel = insecure_channel(f"{host}:{port}")
        self._stub = stub(self._channel)

    def request(self) -> T:
        """
        Get request client

        Returns
        -------
        T
            Request client

        """
        return self._stub
