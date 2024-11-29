from fastapi import FastAPI, UploadFile, File, HTTPException
from services.object_detection import router as object_detection_router, detect_objects
from services.report_generation import router as report_generation_router, generate_report, DetectionRequest

app = FastAPI()

# Include the routers for object detection and report generation
app.include_router(object_detection_router, prefix="/api/object-detection", tags=["Object Detection"])
app.include_router(report_generation_router, prefix="/api/report-generation", tags=["Report Generation"])


@app.post("/api/process-image")
async def process_image(file: UploadFile = File(...)):
    """
    Process an image through the entire pipeline: object detection + report generation.
    """
    try:
        # Step 1: Perform object detection
        detection_results = await detect_objects(file)

        # Step 2: Generate a report based on detected objects
        report_request = DetectionRequest(detections=detection_results["detections"])
        report = await generate_report(report_request)

        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {e}")
