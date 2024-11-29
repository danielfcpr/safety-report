from ultralytics import YOLO
from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import io
import json
router = APIRouter()

# Load the custom YOLO model
model = YOLO("../security_model_v1.pt")

@router.post("/detect-objects")
async def detect_objects(file: UploadFile = File(...)):
    try:
        # Read the uploaded image as a PIL Image
        image_data = await file.read()
        img = Image.open(io.BytesIO(image_data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {e}")

    try:
        # Perform object detection
        results = model(img)

        # Convert results to JSON
        result_string = results[0].to_json(normalize=True, decimals=5)
        result_json = json.loads(result_string)

        # Extract the 'name' fields
        object_list = []
        for item in result_json:
            object_list.append(item["name"])

        return {"detections": object_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Object detection failed: {e}")
