"""Redis client"""
import logging
import os

from redis.asyncio import Redis, BlockingConnectionPool

from utils.singleton import singleton


@singleton
class RedisClient:
    """
    Data class that stores user information

    Attributes
    ----------
    db : redis.Redis
        Redis client
    _pool : BlockingConnectionPool
        Redis connection pool

    Methods
    -------
    async connect()
        Connect to Redis

    """

    db: Redis
    _pool: BlockingConnectionPool

    def __init__(self) -> None:
        self._pool = BlockingConnectionPool.from_url(
            f"redis://{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}"
        )

    async def connect(self) -> None:
        """Connect to Redis"""
        self.db = await Redis(connection_pool=self._pool, decode_responses=True)
        logging.info("Connected to Redis")
