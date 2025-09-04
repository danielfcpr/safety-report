from ultralytics import YOLO
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
from PIL import Image
import io
import json

router = APIRouter()

# Load the custom YOLO model
model = YOLO("../security_model_v1.pt")


@router.post("/detect-objects")
async def detect_objects(files: List[UploadFile] = File(...)):
    images = []
    filenames = []

    # Convert UploadFile objects to PIL images for processing
    for file in files:
        try:
            image_data = await file.read()
            img = Image.open(io.BytesIO(image_data))
            images.append(img)
            filenames.append(file.filename)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image format for {file.filename}: {e}")

    try:
        # Perform model inference over list of images
        results = model(images, verbose=False)

        detections_summary = []
        for idx, result in enumerate(results):
            # Convert result for each image to JSON
            result_string = result.to_json(normalize=True, decimals=5)
            result_json = json.loads(result_string)

            # Extract the 'name' fields for detected objects
            object_list = [item["name"] for item in result_json]

            # Append result with corresponding image filename
            detections_summary.append({
                "file_name": filenames[idx],
                "detections": object_list
            })

        return {"detections_summary": detections_summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Object detection failed: {e}")
