from .params import GrpcClientParams
from .routers import Events, Notifications, Users
from fastapi import Depends, FastAPI

app = FastAPI(dependencies=[Depends(GrpcClientParams)])

app.include_router(Events)
app.include_router(Users)
app.include_router(Notifications)
