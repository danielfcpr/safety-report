# services/object_detection.py
from ultralytics import YOLO
from fastapi import APIRouter, File, UploadFile
from PIL import Image
from io import BytesIO

router = APIRouter()

# Load the custom YOLO model
model = YOLO("security_model_v1.pt")

@router.post("/detect-objects")
async def detect_objects(file: UploadFile = File(...)):
    # Read and open image
    image_data = await file.read()
    img = Image.open(BytesIO(image_data))

    # Run YOLO detection
    results = model(img)  # returns a list of Results objects

    # Extract data from results
    detections = []
    for result in results:
        # Process each detected item and convert to JSON
        detections.append(result.tojson())  # Serialize result to JSON

    return {"detections": detections}  # Return JSON response
