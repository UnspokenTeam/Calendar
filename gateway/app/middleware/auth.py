from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.generated.identity_service.auth_pb2 import AccessToken
from app.generated.user.user_pb2 import GrpcUser
from app.params import GrpcClientParams

api_key_header = APIKeyHeader(name="Authorization")


async def auth(
    grpc_client_params: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
    access_token: Annotated[str, api_key_header],
) -> GrpcUser:
    """
    Authenticate user

    Parameters
    ----------
    grpc_client_params : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI
    access_token: Annotated[str, api_key_header]
        The access token injected by DI

    Returns
    -------
    GrpcUser
        The authenticated user

    """
    user: GrpcUser = grpc_client_params.identity_service_client.request().auth(
        AccessToken(access_token=access_token)
    )

    return user
