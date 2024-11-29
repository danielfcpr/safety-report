from fastapi import APIRouter, HTTPException
from openai import OpenAI, OpenAIError
from pydantic import BaseModel
import config
router = APIRouter()

# Initialize the OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

class DetectionRequest(BaseModel):
    detections: list[str]

@router.post("/generate-report")
async def generate_report(request: DetectionRequest):
    prompt = (
        "You are a safety expert specialized in construction site safety. "
        "Generate a comprehensive safety report based on the detected objects listed below. "
        "This report should comply with the regulatory requirements for construction sites in Luxembourg:\n"
    )
    for detection in request.detections:
        prompt += f"- {detection}\n"

    try:
        # Use the ChatCompletion API
        completion =  client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert report writer specialized in construction site safety."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )
        # Extract the response text
        report = completion.choices[0].message.content
        return {"report": report}

    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the report: {e}")