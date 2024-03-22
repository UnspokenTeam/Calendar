import prisma
from prisma import Prisma

from utils.singleton import singleton


@singleton
class Db:
    db: prisma.Client

    def __init__(self):
        self.db = Prisma(auto_register=True)

    async def connect(self):
        await self.db.connect()
