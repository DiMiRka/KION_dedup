import xxhash
from dotenv import load_dotenv
import json
from sqlalchemy.future import select

from src.database import db_dependency
from src.models.models import ProductEvent
from src.redisconf import r
from src.bloomfilter import bf

load_dotenv()


async def dedup_redis(key: str):
    dkey = xxhash.xxh3_64(key).hexdigest()
    if not await r.exists(dkey):
        await r.set(name=dkey, value=dkey, ex=36288000)
        return True
    else:
        return False


async def dedup_bloom(key: str):
    if not await bf.check(key):
        await bf.add(key)
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


async def db_get_events(db: db_dependency):
    result = await db.execute(select(ProductEvent))
    return result.scalars().all()
