from typing import Annotated

import grpc

from app.generated.identity_service.auth_pb2 import AccessToken
from app.generated.user.user_pb2 import GrpcUser
from app.params import GrpcClientParams

from fastapi import Depends
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="Authorization")


async def auth(
    grpc_client_params: Annotated[GrpcClientParams, Depends(GrpcClientParams)],
    access_token: Annotated[str, api_key_header]
) -> GrpcUser:
    try:
        user: GrpcUser = await grpc_client_params.identity_service_client.request().auth(
            AccessToken(access_token=access_token)
        )
        return user
    except grpc.RpcError:
        raise ValueError
