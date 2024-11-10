# services/object_detection.py
from ultralytics import YOLO
from fastapi import APIRouter
from PIL import Image

router = APIRouter()

# Load the custom YOLO model
model = YOLO("../security_model_v1.pt")

@router.post("/detect-objects")
async def detect_objects(image_path: str):
    # Open the image from the provided path
    img = Image.open(image_path)

    # Perform object detection
    results = model(img)

    # Extract bounding boxes, label names and
    detection_list = []
    for result in results:
        result.tojson()
        detection_list.append(result)

    return {"detection list": detection_list}
