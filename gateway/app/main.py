from .middleware import InterceptorMiddleware
from .params import GrpcClientParams
from .routers import Events, Invites, Users
from fastapi import Depends, FastAPI

app = FastAPI(dependencies=[Depends(GrpcClientParams)])
app.add_middleware(InterceptorMiddleware)

app.include_router(Events)
app.include_router(Users)
app.include_router(Invites)
