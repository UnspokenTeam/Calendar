from .params import GrpcClientParams
from .routers import Events
from fastapi import Depends, FastAPI

app = FastAPI(dependencies=[Depends(GrpcClientParams)])

app.include_router(Events)
