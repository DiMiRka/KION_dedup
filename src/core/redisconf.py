import redis.asyncio as redis
from core import app_settings


POOL = redis.ConnectionPool.from_url(app_settings.redis_dsn.unicode_string())

r = redis.StrictRedis(connection_pool=POOL)
