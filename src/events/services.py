from sqlalchemy.future import select
import os
import redis.asyncio as redis
import xxhash
from dotenv import load_dotenv
import json

from src.database import db_dependency

load_dotenv()


async def dedup_key(event: dict):
    key = f"{event['client_id']} | {event['event_datetime']} | {event['event_name']} | {event['product_id']} | {event['sid']} | {event['r']}"
    return xxhash.xxh3_64(key).hexdigest()


async def dedup_redis(dkey: str):
    r = redis.from_url(os.getenv("REDIS_URL"))
    if not await r.hexists(name='dedup', key=dkey):
        await r.hset(name='dedup', key=dkey, value=dkey)
        print("Добавили")
        return True
    else:
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("Событие есть")
        print(r.hgetall(dkey))
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return False
#  r.hset(key=key, mapping={"client_id": "0069613e121e47ed", "event_name": "card_show", "event_datetime": "2025-04-02 09:07:31+00:00", "product_id": "4c209d65-c988-4d58-99bf-1cb72db34784", "sid": "5522119441743559165", "r": "2408654471743563251"})
#  r.hset(name=dkey, mapping={"client_id": event['client_id'], "event_datetime": str(event['event_datetime']), "event_name": event['event_name'], "product_id": event['product_id'], "sid": event['sid'], "r": event['r']})


async def create_event(db: db_dependency, event: dict):
    event_type = event["event_name"]
    client_id = event["client_id"]
    event_data = json.dumps(event)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print(event_type)
    print(client_id)
    print(event_data)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")

