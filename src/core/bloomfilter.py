import math
import mmh3
from redis.exceptions import WatchError


from .redisconf import r


class BloomFilter(object):
    def __init__(self, items_count, fp_prob, name="bloom"):
        self.fp_prob = fp_prob
        self.size = self.get_size(items_count, fp_prob)
        self.hash_count = self.get_hash_count(self.size, items_count)
        self.name = name
        self.lock_key = f"{name}:lock"

    async def init_filter(self):
        async with r.pipeline() as pipe:
            await pipe.setbit(self.name, self.size - 1, 0)
            await pipe.expire(self.name, 604800)
            await pipe.execute()

    async def add(self, item):
        max_retries = 3
        for _ in range(max_retries):
            try:
                async with r.pipeline() as pipe:
                    await pipe.watch(self.name)

                    digests = [mmh3.hash(item, i) % self.size for i in range(self.hash_count)]

                    pipe.multi()
                    for digest in digests:
                        pipe.setbit(self.name, digest, 1)
                    pipe.expire(self.name, 604800)

                    await pipe.execute()
                    return True
            except WatchError:
                continue
        return False

    async def check(self, item):
        async with r.pipeline() as pipe:
            for i in range(self.hash_count):
                digest = mmh3.hash(item, i) % self.size
                pipe.getbit(self.name, digest)
            bits = await pipe.execute()
            return all(bits)

    async def clear(self):
        await r.delete(self.name)

    @classmethod
    def get_size(cls, n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(cls, m, n):
        k = (m / n) * math.log(2)
        return int(k)


bf = BloomFilter(10000, 0.01)
