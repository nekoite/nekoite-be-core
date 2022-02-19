import sys

sys.path.append("src")

from nekoite_be_core.cache import lru_cache, redis_func_cache
import redis
import time
import pickle

r = redis.Redis()


def task_simple(x, y):
    return [x, y]


@redis_func_cache(r, "myproject", ex=30)
def compute_simple(x, y):
    time.sleep(1)
    return task_simple(x, y)


class SomeData:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, SomeData):
            return False
        return __o.a == self.a and __o.b == self.b


def task_object(a, b):
    return SomeData(a, b)


# warning: using pickle is unsafe!
@redis_func_cache(r, "myproject", serializer=pickle, ex=30)
def compute_object(a, b):
    time.sleep(1)
    return task_object(a, b)


for _ in range(4):
    start = int(time.time())
    val = compute_simple(1, 2)
    assert val == task_simple(1, 2)
    end = int(time.time())
    print(f"Used {end - start} seconds")

print(r.get("myprojectcompute_simple-3550055125485641917"))


for _ in range(4):
    start = int(time.time())
    val = compute_object(1, 2)
    assert val == task_object(1, 2)
    end = int(time.time())
    print(f"Used {end - start} seconds")

print(r.get("myprojectcompute_object-3550055125485641917"))
