from fastapi import APIRouter, Depends, HTTPException

from src.database import db_dependency
from src.events.schemas import Event
from src.events.services import dedup_key, dedup_redis, create_event

events_router = APIRouter(prefix="/events", tags=['events'])


@events_router.post("/event")
async def post_event(db: db_dependency, event: Event):
    event = event.dict()
    key = await dedup_key(event)
    if await dedup_redis(key):
        await create_event(db, event)
    return event
