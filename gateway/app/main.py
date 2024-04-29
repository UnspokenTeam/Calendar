from contextlib import asynccontextmanager, AbstractAsyncContextManager
from os import environ

import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from .middleware import InterceptorMiddleware
from .middleware.rate_limiter import handler as rate_limiter_handler
from .params import GrpcClientParams
from .routers import Events, Users
from fastapi import Depends, FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI) -> AbstractAsyncContextManager[None]:
    redis_client = redis.from_url(environ['REDIS_URL'])
    await FastAPILimiter.init(redis_client, http_callback=rate_limiter_handler)
    yield
    await FastAPILimiter.close()


app = FastAPI(dependencies=[Depends(GrpcClientParams), Depends(RateLimiter(times=1, seconds=2))], lifespan=lifespan)
app.add_middleware(InterceptorMiddleware)

app.include_router(Events)
app.include_router(Users)
