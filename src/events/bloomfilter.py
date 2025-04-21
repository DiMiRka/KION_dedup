import math
import mmh3
from bitarray import bitarray

from core.redisconf import r


class BloomFilter(object):
    def __init__(self, items_count, fp_prob):

        self.fp_prob = fp_prob
        self.size = self.get_size(items_count, fp_prob)
        self.hash_count = self.get_hash_count(self.size, items_count)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    async def add(self, item):
        digests = []
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)

            self.bit_array[digest] = True
        data = self.bit_array.tobytes()
        await r.set(name=item, value=data, ex=36288000)

    async def check(self, item):
        data = await r.get(item)
        if data:
            arr = bitarray()
            arr.frombytes(data)

            for i in range(self.hash_count):
                digest = mmh3.hash(item, i) % self.size

                if not arr[digest]:
                    return False
            return True
        return False

    @classmethod
    def get_size(cls, n, p):
        m = -(n * math.log(p))/(math.log(2)**2)
        return int(m)

    @classmethod
    def get_hash_count(cls, m, n):
        k = (m/n) * math.log(2)
        return int(k)


bf = BloomFilter(10000, 0.01)
