import os
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

POOL = redis.ConnectionPool.from_url(os.getenv("REDIS_URL"))

r = redis.StrictRedis(connection_pool=POOL)
