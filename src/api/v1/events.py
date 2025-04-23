from fastapi import APIRouter, HTTPException

from src.core import db_dependency
from src.schemas import Event
from src.services import dedup_redis, db_create_event, db_get_events, dedup_bloom

events_router = APIRouter(prefix="/events", tags=['events'])


@events_router.post("/event_post", responses={
    201: {"model": Event},
    400: {"description": "Incorrect request"},
    404: {"description": "Not found"},
    500: {"description": "Eternal error"}
})
async def post_event(db: db_dependency, event: Event):
    event = event.dict()

    # Take unique event fields for deduplication
    key = f"{event['client_id']} | {event['event_datetime']} | {event['event_name']} | {event['product_id']} | {event['sid']} | {event['r']}"

    if await dedup_redis(key):  # Check hash in redis
        if await dedup_bloom(key):  # Check event in bloom filter
            await db_create_event(db, event)  # Add Event to Database
            return f"Event added {event}"
        else:
            return "Duplicate filtered out"
    else:
        return "Duplicate filtered out"


@events_router.get("/get_events", responses={
    200: {"model": list},
    404: {"description": "Event not found"},
    400: {"description": "Invalid request"},
})
async def get_events(db: db_dependency):
    events = await db_get_events(db)
    if events is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return events
