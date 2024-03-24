"""Redis client"""
import os

from redis import Redis

from utils.singleton import singleton


@singleton
class RedisClient:
    """
    Data class that stores user information

    Attributes
    ----------
    db : redis.Redis
        Redis client

    """

    db: Redis

    def __init__(self):
        self.db = Redis(
            host=os.environ["REDIS_HOST"],
            port=os.environ["REDIS_PORT"],
            socket_connect_timeout=2,
        )
