from firebase import db
from fastapi import HTTPException, BackgroundTasks
from dotenv import load_dotenv
from app.ml_model import run_pipeline
from fastapi import APIRouter
from app.schema import CreateDogSchema
from app.utils import put_img_into_bucket, create_inference_record, \
    create_dog_record
from app.constants import GCS_DOG_FOLDER_NAME, GCS_DOG_FOLDER_PATH, \
    DOGS_COLLECTION, DOG_INFERENCES

load_dotenv()

api_router = APIRouter()


async def save_dog_record(payload, detected_emotion, confidence_emotion):
    try:
        # Put image (in byte-string) into GCS bucket and obtain the
        # url link to the image
        img_public_url = put_img_into_bucket(
            base64_image_string=payload.image,
            gcs_img_folder_path=GCS_DOG_FOLDER_PATH,
            animal_type=GCS_DOG_FOLDER_NAME
        )

        # Create inference record
        inference_data = create_inference_record(
            img_public_url=img_public_url,
            detected_emotion=detected_emotion,
            confidence_emotion=confidence_emotion
        )

        # Obtain reference to the document with 'dog_id'
        # as the document id (if any)
        dog_id = payload.dog_id
        dog_ref = db.collection(DOGS_COLLECTION).document(dog_id)

        # If document for dog exists, append current inference to the
        # inference list in the dog's document.
        # Else, create a new document for the dog, with dog_id as the
        # id of the document.
        if dog_ref.get().exists:
            current_inferences = dog_ref.get().to_dict()[DOG_INFERENCES]
            current_inferences.append(inference_data)
            dog_ref.set({DOG_INFERENCES: current_inferences}, merge=True)

        else:
            dog_record = create_dog_record(
                name=payload.name,
                inference_data=inference_data
            )
            dog_ref.set(dog_record)
        print("Saved dog inference data to firestore and image to GCS bucket")

    except Exception as ex:
        print(ex)


@api_router.post("/dog", response_model=dict)
async def create_dog_record_api(
    payload: CreateDogSchema,
    background_tasks: BackgroundTasks
):
    """
    Create a new dog record / add inference to existing dog record
    (if the record exists)
    """
    try:
        # Obtain emotion & confidence score from ML pipeline
        res = run_pipeline(payload.image)
        detected_emotion = res["label"]
        confidence_emotion = res["score"]

        # Start the background task to add dog record to firestore
        # & image to GCS bucket
        background_tasks.add_task(
            save_dog_record,
            payload,
            detected_emotion,
            confidence_emotion
        )

        return {
            "msg": f"Added inference for dog {payload.dog_id} successfully",
            "data": {
                "dog_id": payload.dog_id,
                "name": payload.name,
                "detected_emotion": detected_emotion,
                "confidence_emotion": confidence_emotion
            }
        }
    except KeyError as ex:
        raise HTTPException(
            status_code=404,
            detail=f"Required field is not present in request: {ex}"
        )
    except Exception as ex:
        raise HTTPException(
            status_code=404,
            detail=f"Error: {ex}"
        )
