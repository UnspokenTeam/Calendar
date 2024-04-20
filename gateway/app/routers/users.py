from typing import Annotated, Any

from app.generated.user.user_pb2 import GrpcUser
from app.middleware.auth import auth

from fastapi import APIRouter, Security

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me")
async def get_user_info(_: Annotated[GrpcUser, Security(auth)]) -> dict[str, Any]:
    return {"user_id": 331232}
