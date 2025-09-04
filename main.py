from fastapi import FastAPI, UploadFile, File, HTTPException
from services.object_detection import router as object_detection_router, detect_objects
from services.report_generation import router as report_generation_router, generate_report, DetectionRequest
from typing import List
app = FastAPI()

# Include the routers for object detection and report generation
app.include_router(object_detection_router, prefix="/api/object-detection", tags=["Object Detection"])
app.include_router(report_generation_router, prefix="/api/report-generation", tags=["Report Generation"])


@app.post("/api/process-image")
async def process_image(files: List[UploadFile] = File(...)):
    """
    Process an image through the entire pipeline: object detection + report generation.
    """
    try:
        detection_results = await detect_objects(files)
        report_request = DetectionRequest(detections_summary=detection_results["detections_summary"])
        report = await generate_report(report_request)

        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {e}")
