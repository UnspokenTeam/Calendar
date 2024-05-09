"""Auth middleware"""
from typing import Annotated

from grpc import RpcError

from app.errors.unauthenticated_error import UnauthenticatedError
from app.generated.identity_service.auth_pb2 import AccessToken
from app.generated.user.user_pb2 import GrpcUser
from app.params import GrpcClientParams

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth_2 = OAuth2PasswordBearer(tokenUrl="users/login")


async def auth(
        grpc_client_params: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
        access_token: Annotated[str, Depends(oauth_2)],
) -> GrpcUser:
    """
    Authenticate user

    Parameters
    ----------
    grpc_client_params : Annotated[GrpcClientParams, Depends(GrpcClientParams)]
        Grpc clients injected by DI
    access_token: Annotated[str, api_key_header]
        The credentials injected by DI

    Returns
    -------
    GrpcUser
        The authenticated user

    """
    try:
        user: GrpcUser = grpc_client_params.identity_service_client.request().auth(
            AccessToken(access_token=access_token)
        )

        return user
    except RpcError as e:
        raise UnauthenticatedError(f"Wrong credentials - {e}")
