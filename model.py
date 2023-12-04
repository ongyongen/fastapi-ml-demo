from fastapi import FastAPI
from contextlib import asynccontextmanager
from transformers import pipeline
from constants import DOG_EMOTION_ML_MODEL_REF, DOG_EMOTION_MODEL_NAME, DOG_EMOTION_MODEL_TYPE

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize ML pipeline once upon app startup
    """
    print("Initialize App")
    ml_models[DOG_EMOTION_ML_MODEL_REF] = pipeline(DOG_EMOTION_MODEL_TYPE, model=DOG_EMOTION_MODEL_NAME)
    yield
    ml_models.clear()

def run_pipeline(base64_string):
    """
    Run ML pipeline to output the dog's emotion & confidence level for the 
    identified emotion
    """
    dog_emotion_model = ml_models[DOG_EMOTION_ML_MODEL_REF]
    res = dog_emotion_model(base64_string, top_k=1)[0]
    return res