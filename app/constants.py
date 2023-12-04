import os

# Data attribute fields
INFERENCE_TIMESTAMP = "timestamp"
INFERENCE_IMAGE = "image"
INFERENCE_DETECTED_EMOTION = "detected_emotion"
INFERENCE_CONFIDENCE_EMOTION = "confidence_emotion"

DOG_NAME = "name"
DOG_INFERENCES = "inferences"

# Firestore collections
DOGS_COLLECTION = "dogs"

# ML Model
DOG_EMOTION_ML_MODEL_REF = "dog_emotion"
DOG_EMOTION_MODEL_TYPE = "image-classification"
DOG_EMOTION_MODEL_NAME = "Dewa/dog_emotion_v3"

# GCS Variables and Filepaths
GCS_DOG_FOLDER_PATH = "dog"
GCS_DOG_FOLDER_NAME = "dog"

GCS_STORAGE_CLIENT = os.environ.get("GCS_STORAGE_CLIENT")
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
