import os

from redis import Redis


class RedisClient:
    _db: Redis

    def __init__(self):
        self._db = Redis(
            host=os.environ["REDIS_HOST"],
            port=os.environ["REDIS_PORT"],
            socket_connect_timeout=2,
        )
