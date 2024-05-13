"""Main file"""
# mypy: ignore-errors
from contextlib import asynccontextmanager
from os import environ
from typing import AsyncIterator

from .middleware import InterceptorMiddleware
from .middleware.rate_limiter import handler as rate_limiter_handler
from .params import GrpcClientParams
from .routers import Events, Invites, Notifications, Users
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """
    Context manager that enables lifespan of FastAPI application.

    Parameters
    ----------
    _ : FastAPI
        FastAPI application.

    Returns
    -------
    AsyncContextManager[Never]
        None

app = FastAPI(
    dependencies=[Depends(GrpcClientParams)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
    """
    redis_client = redis.from_url(environ["REDIS_URL"])
    await FastAPILimiter.init(redis_client, http_callback=rate_limiter_handler)
    yield None
    await FastAPILimiter.close()


app = FastAPI(
    dependencies=[Depends(GrpcClientParams), Depends(RateLimiter(times=1, seconds=2))],
    lifespan=lifespan,
)
app.add_middleware(InterceptorMiddleware)

app.include_router(Events)
app.include_router(Users)
app.include_router(Notifications)
app.include_router(Invites)
