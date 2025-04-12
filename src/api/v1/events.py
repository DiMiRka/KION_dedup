from fastapi import APIRouter

from src.database import db_dependency
from src.events.schemas import Event
from src.events.services import create_dedup_key_redis, dedup_redis, db_create_event

events_router = APIRouter(prefix="/events", tags=['events'])


@events_router.post("/event")
async def post_event(db: db_dependency, event: Event):
    event = event.dict()
    key = await create_dedup_key_redis(event)
    if await dedup_redis(key):
        await db_create_event(db, event)
    return event
