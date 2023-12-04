from fastapi import FastAPI
from app.dog_api import api_router
from app.ml_model import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
