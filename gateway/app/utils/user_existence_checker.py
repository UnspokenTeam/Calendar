"""User existence checker"""
from typing import Annotated
from uuid import UUID

from app.generated.identity_service.get_user_pb2 import (
    UserByIdRequest as GrpcGetUserByIdRequest,
)
from app.params import GrpcClientParams

from pydantic import UUID4, AfterValidator


def check_user_existence(
        user_id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))],
        grpc_clients: GrpcClientParams
) -> None:
    """
    \f

    Check if user with given id exists

    Parameters
    ----------
    user_id : UUID4 | str
        User's id
    grpc_clients : GrpcClientParams
        Grpc clients

    """
    _ = grpc_clients.identity_service_client.request().get_user_by_id(
        GrpcGetUserByIdRequest(user_id=str(user_id))
    )
