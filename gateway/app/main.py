from .routers import Events
from fastapi import FastAPI

app = FastAPI()

app.include_router(Events)
