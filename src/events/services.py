import os
import redis.asyncio as redis
import xxhash
from dotenv import load_dotenv
import json

from src.database import db_dependency
from src.models.models import ProductEvent
from src.redisconf import r

load_dotenv()


async def create_dedup_key_redis(event: dict):
    key = f"{event['client_id']} | {event['event_datetime']} | {event['event_name']} | {event['product_id']} | {event['sid']} | {event['r']}"
    return xxhash.xxh3_64(key).hexdigest()


async def dedup_redis(dkey: str):
    if not await r.hexists(name='dedup', key=dkey):
        await r.hset(name='dedup', key=dkey, value=dkey)
        return True
    else:
        return False


async def db_create_event(db: db_dependency, event: dict):
    event_type = event["event_name"]
    client_id = event["client_id"]
    event_data = json.dumps(event)
    db_event = ProductEvent(event_type=event_type, client_id=client_id, event_data=event_data)
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event
