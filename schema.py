from constants import *
from pydantic import BaseModel

class CreateDogSchema(BaseModel):
    dog_id : str
    name : str
    image : str


class Inference:
    def __init__(
            self, 
            timestamp, 
            image, 
            detected_emotion, 
            confidence_emotion
        ):
        self.timestamp = timestamp
        self.image = image
        self.detected_emotion = detected_emotion
        self.confidence_emotion = confidence_emotion

    def to_dict(self):
        return {
            INFERENCE_TIMESTAMP : self.timestamp,
            INFERENCE_IMAGE : self.image,
            INFERENCE_DETECTED_EMOTION : self.detected_emotion,
            INFERENCE_CONFIDENCE_EMOTION : self.confidence_emotion
        }

class Dog:
    def __init__(
            self, 
            name, 
            inferences
        ):
        self.name = name
        self.inferences = inferences

    def to_dict(self):
        return {
            DOG_NAME : self.name,
            DOG_INFERENCES : self.inferences
        }
    