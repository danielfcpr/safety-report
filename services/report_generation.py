from fastapi import APIRouter, HTTPException
from openai import OpenAI, OpenAIError
from pydantic import BaseModel
from typing import List, Dict
import config
router = APIRouter()

# Initialize the OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

class DetectionSummary(BaseModel):
    file_name: str
    detections: List[str]

class DetectionRequest(BaseModel):
    detections_summary: List[DetectionSummary]

@router.post("/generate-report")
async def generate_report(request: DetectionRequest):
    prompt = (
        "You are a safety expert specialized in construction site safety. "
        "Generate a comprehensive safety report based on the detected objects from the photos listed below. "
        "Focus on the presence or absence of critical safety equipment like helmets and vests. "
        "This report should comply with the regulatory requirements for construction sites in Luxembourg:\n"
    )

    # Include each file's detections with context
    for summary in request.detections_summary:
        prompt += f"\nFile: {summary.file_name}\n"
        prompt += "\n".join(f"- {detection}" for detection in summary.detections)

    try:
        # Use the ChatCompletion API
        completion =  client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert report writer specialized in construction site safety."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
        )
        # Extract the response text
        report = completion.choices[0].message.content
        return {"report": report}

    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the report: {e}")