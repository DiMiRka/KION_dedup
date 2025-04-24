import xxhash
import json
from sqlalchemy.future import select

from core import db_dependency
from models import ProductEvent
from core import r
from core import bf


async def dedup_redis(key: str):
    """First stage of deduplication. Redis hash"""
    dkey = xxhash.xxh3_64(key).hexdigest()
    if not await r.exists(dkey):
        await r.set(name=dkey, value=dkey, ex=36288000)
        return True
    else:
        return False


async def dedup_bloom(key: str):
    """The second stage of deduplication. Bloom filter"""
    if not await bf.check(key):
        await bf.add(key)
        return True
    else:
        return False


async def db_create_event(db: db_dependency, event: dict):
    """Add event to database"""
    event_type = event["event_name"]
    client_id = event["client_id"]
    event_data = json.dumps(event)
    db_event = ProductEvent(event_type=event_type, client_id=client_id, event_data=event_data)
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


async def db_get_events(db: db_dependency):
    """Get last 25 events from the database"""
    result = await db.execute(select(ProductEvent).order_by(ProductEvent.id.desc()).limit(10))
    return result.scalars().all()
