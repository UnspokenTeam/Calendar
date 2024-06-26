"""Postgres client"""

import logging

from prisma import Client, Prisma

from utils import singleton


@singleton
class PostgresClient:
    """
    Postgres client

    Attributes
    ----------
    db : prisma.Client
        Prisma db client
    _connected : bool
        Flag to indicate if connection is established

    Methods
    -------
    async connect()
        Connects prisma client to database
    async disconnect()
        Disconnects prisma client from database

    """

    db: Client
    _connected: bool = False

    def __init__(self) -> None:
        self.db = Prisma(auto_register=True)

    async def connect(self) -> None:
        """Connect to database"""
        await self.db.connect()
        logging.info("Connected to Postgres")
        self._connected = True

    async def disconnect(self) -> None:
        """Disconnect from database"""
        if not self._connected:
            logging.info("Not connected to Postgres. Skipping disconnect...")
            return

        await self.db.disconnect()
        logging.info("Disconnected from Postgres")
        self._connected = False
