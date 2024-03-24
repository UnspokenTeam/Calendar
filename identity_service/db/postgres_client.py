"""Postgres client"""
import logging

from prisma import Prisma, Client

from utils.singleton import singleton


@singleton
class PostgresClient:
    """
    Postgres client

    Attributes
    ----------
    db : prisma.Client
        Prisma db client


    Methods
    -------
    async connect()
        Connects prisma client to database

    """

    db: Client

    def __init__(self):
        self.db = Prisma(auto_register=True)

    async def connect(self) -> None:
        """Connect to database"""
        await self.db.connect()
        logging.info("Connected to Postgres")
