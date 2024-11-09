# services/image_upload.py
import os
from fastapi import APIRouter, UploadFile, File
from pathlib import Path

router = APIRouter()

# Define a temporary directory to store uploaded images
TEMP_DIR = Path("temp_images")
TEMP_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    # Save the uploaded image
    image_path = TEMP_DIR / file.filename
    with open(image_path, "wb") as image_file:
        image_file.write(await file.read())

    return {"image_path": str(image_path)}
