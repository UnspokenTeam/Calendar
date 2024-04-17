import os
from typing import Any

from fastapi import APIRouter

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.get("/{event_id}")
async def get_event_by_event_id(event_id: int) -> dict[str, Any]:
    return {"event_id": event_id}


@router.get("/my")
async def get_my_events() -> dict[str, Any]:
    return {"my_events": 331232}
