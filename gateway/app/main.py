"""Main file"""
from .middleware import InterceptorMiddleware
from .params import GrpcClientParams
from .routers import Events, Invites, Notifications, Users
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

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
app.add_middleware(InterceptorMiddleware)

app.include_router(Events)
app.include_router(Users)
app.include_router(Notifications)
app.include_router(Invites)
