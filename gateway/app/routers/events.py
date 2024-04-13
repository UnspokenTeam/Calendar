from fastapi import APIRouter

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.get("/{event_id}")
async def get_event_by_event_id(event_id: int):
    # TODO some grpc logic here
    return {"event_id": event_id}

@router.get("/my")
async def get_my_events():
    return {"my_events": 331232}
