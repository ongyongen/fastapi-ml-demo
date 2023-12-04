from fastapi import FastAPI
from dog_api import api_router
from model import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
