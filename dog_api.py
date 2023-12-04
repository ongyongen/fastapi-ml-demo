from fastapi import HTTPException
from firebase import db
from utils import put_img_into_bucket, create_inference_record, create_dog_record
from schema import CreateDogSchema
from constants import *
from dotenv import load_dotenv
from utils import *
from model import run_pipeline
from fastapi import APIRouter

load_dotenv() 

api_router = APIRouter()

@api_router.post("/dog", response_model=dict)
async def create_dog_record(payload: CreateDogSchema):
    """
    Create a new dog record / add inference to existing dog record (if the record exists)   
    # {
    #   "name": "dog1",
    #   "dog_id": "99",
    #   "image": "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"
    # }

    """
    try:
        # Obtain emotion & confidence score from ML pipeline
        res = run_pipeline(payload.image)
        detected_emotion = res["label"]
        confidence_emotion = res["score"]

        # Put image (in byte-string) into GCS bucket and obtain the 
        # url link to the image
        img_public_url = put_img_into_bucket(
            base64_image_string = payload.image,
            gcs_img_folder_path = GCS_DOG_FOLDER_PATH,
            animal_type = GCS_DOG_FOLDER_NAME
        )

        # Create inference record
        inference_data = create_inference_record(
            img_public_url = img_public_url,
            detected_emotion = detected_emotion,
            confidence_emotion = confidence_emotion
        )

        # Obtain reference to the document with 'dog_id' as the document id (if any)
        dog_id = payload.dog_id
        dog_ref = db.collection(DOGS_COLLECTION).document(dog_id)

        # If document for dog exists, append current inference to the inference list in the dog's document
        # Else, create a new document for the dog 
        if dog_ref.get().exists:
            current_inferences = dog_ref.get().to_dict()[DOG_INFERENCES]
            current_inferences.append(inference_data)
            dog_ref.set({DOG_INFERENCES: current_inferences}, merge=True)

        else:
            dog_record = create_dog_record(
                name = payload.name,
                inference_data = inference_data
            )
            dog_ref.set(dog_record)

        return {
            "msg" : f"Added inference for dog {dog_id} successfully",
            "data" : {
                "name" : payload.name,
                "dog_id" : payload.dog_id,
                "detected_emotion" : detected_emotion,
                "confidence_emotion" : confidence_emotion
            }
        }
        
    except KeyError as ex:
        raise HTTPException(status_code=404, detail=f"Required field is not present in request: {ex}")
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"Error: {ex}")
