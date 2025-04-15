from fastapi import APIRouter, HTTPException

from src.database import db_dependency
from src.events.schemas import Event
from src.events.services import create_dedup_key_redis, dedup_redis, db_create_event, db_get_events

events_router = APIRouter(prefix="/events", tags=['events'])


@events_router.post("/event_post")
async def post_event(db: db_dependency, event: Event):
    event = event.dict()
    key = await create_dedup_key_redis(event)
    if await dedup_redis(key):
        await db_create_event(db, event)
    return event


@events_router.get("/get_events", responses={
    200: {"model": list},
    404: {"description": "Response not found"},
    400: {"description": "Invalid request"},
})
async def get_events(db: db_dependency):
    events = await db_get_events(db)
    if events is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return events
