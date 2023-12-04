import base64
from google.cloud import storage
from datetime import datetime
from app.constants import GCS_STORAGE_CLIENT, GCS_BUCKET_NAME
from app.schema import Inference, Dog

def put_img_into_bucket(base64_image_string, gcs_img_folder_path, animal_type):  
    """
    Store image (base64 string) as a jpeg in a GCS storage bucket and return the 
    public url to that image 
    """  
    storage_client = storage.Client(GCS_STORAGE_CLIENT)
    bucket = storage_client.bucket(GCS_BUCKET_NAME)

    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S-%f")
    file_name = f"{animal_type}_{timestamp}.jpg"

    img_data = base64_image_string.encode()
    content = base64.b64decode(img_data)

    blob = bucket.blob(f"{gcs_img_folder_path}/{file_name}")
    blob.upload_from_string(content, content_type='image/jpeg')
    
    return blob.public_url

def create_inference_record(
    img_public_url:str, 
    detected_emotion:str, 
    confidence_emotion:str
):
    """
    Create a dict storing inference data
    """
    inference_data = Inference(
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        image = img_public_url, 
        detected_emotion = detected_emotion,
        confidence_emotion = confidence_emotion
    ).to_dict()
    return inference_data

def create_dog_record(
    name:str,
    inference_data:dict
):
    """
    Create a dict storing dog record data
    """
    dog_record = Dog(
        name = name,
        inferences = [inference_data]
    ).to_dict()
    return dog_record
