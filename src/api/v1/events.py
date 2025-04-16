from fastapi import APIRouter, HTTPException

from src.database import db_dependency
from src.events.schemas import Event
from src.events.services import dedup_redis, db_create_event, db_get_events, dedup_bloom

events_router = APIRouter(prefix="/events", tags=['events'])


@events_router.post("/event_post", responses={
    201: {"model": Event},
    400: {"description": "Incorrect request"},
    404: {"description": "Not found"},
    500: {"description": "Eternal error"}
})
async def post_event(db: db_dependency, event: Event):
    event = event.dict()
    key = f"{event['client_id']} | {event['event_datetime']} | {event['event_name']} | {event['product_id']} | {event['sid']} | {event['r']}"
    if await dedup_redis(key):
        if await dedup_bloom(key):
            await db_create_event(db, event)
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
