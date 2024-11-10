# main.py
from fastapi import FastAPI
from services.image_upload import router as image_upload_router
from services.object_detection import router as object_detection_router
from services.report_generation import router as report_generation_router
app = FastAPI()

# Register the router
app.include_router(image_upload_router)
app.include_router(object_detection_router)
app.include_router(report_generation_router)
@app.get("/")
async def read_root():
    return {"message": "Hello World",
            "API status": "runninx"}

