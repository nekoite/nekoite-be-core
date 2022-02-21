from functools import lru_cache, _make_key
import functools
from typing import Callable, Dict, Hashable, Tuple
import json

from nekoite_be_core.types.interfaces import IStrSerializer

try:
    import redis
except ImportError:
    pass

try:
    from functools import cache  # type: ignore
except ImportError:

    def cache(user_function: Callable):  # type: ignore
        'Simple lightweight unbounded cache.  Sometimes called "memoize".'
        return lru_cache(maxsize=None)(user_function)


__all__ = ["redis_func_cache", "lru_cache", "cache"]


def _default_key_maker(
    func: Callable, args: Tuple[Hashable, ...], kwargs: Dict[str, Hashable], typed: bool
) -> str:
    return func.__name__ + str(hash(_make_key(args, kwargs, typed)))


def redis_func_cache(
    r: redis.Redis,
    prefix: str,
    *,
    typed: bool = False,
    key_maker: Callable[
        [Callable, Tuple[Hashable, ...], Dict[str, Hashable], bool], str
    ] = None,
    serializer: IStrSerializer = json,
    **redis_kwargs,
):
    """
    Currently the serializer used is json instead of pickle for security issues,
    but pickle can also be used by settiing the `serializer=pickle`.
    """
    import redis

    if not isinstance(r, redis.Redis):
        raise RuntimeError("r should be a redis instance")

    if not key_maker:
        key_maker = _default_key_maker

    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            key = prefix + key_maker(func, args, kwargs, typed)
            v = r.get(key)
            if v:
                return serializer.loads(v)
            v = func(*args, **kwargs)
            r.set(key, serializer.dumps(v), **redis_kwargs)
            return v

        return _wrapper

    return _decorator
