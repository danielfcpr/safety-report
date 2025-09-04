# Construction Safety Report API (POC)

End-to-end pipeline that **detects safety items/risks in construction photos (YOLO)** and **drafts a safety report (LLM)** aligned with the client's requirements (Luxembourg construction site context). Built with **FastAPI**, **Ultralytics YOLO**, and **OpenAI (GPT-4o)**.

> ⚠️ **Disclaimer:** This POC is for demonstration. It is **not legal advice** and **not a certified compliance tool**. Any production use must be reviewed by legal/compliance stakeholders and adapted to the latest regulations.

---

## ✨ Features
- **/api/object-detection/detect-objects** → Detect PPE / site safety items and risks from uploaded images (custom YOLO model: `security_model_v1.pt`).  
- **/api/report-generation/generate-report** → Generate a **text safety report** (OpenAI) from detected items/risks.  
- **/api/process-image** → Orchestrate both steps: upload image(s) → get a ready draft report.

```
main.py
services/
 ├─ object_detection.py   # YOLO-based detection endpoint
 └─ report_generation.py  # LLM report generation endpoint
security_model_v1.pt      # Custom YOLO model (place at repo root)
data/test_img_*.png       # Sample images
requirements.txt
```

---

## 🧱 Architecture
```text
[Images] → [YOLO Detection API] → detections_summary (JSON)
                              ↘
                               → [LLM Report API] → safety report (text)
```

---

## 🔌 Endpoints

### 1) POST /api/object-detection/detect-objects
Form-data: `files` = one or more images.
Response:
```json
{
  "detections_summary": [
    {
      "file_name": "test_img_1.png",
      "detections": ["helmet","vest","gloves"]
    }
  ]
}
```

### 2) POST /api/report-generation/generate-report
Body:
```json
{
  "detections_summary": [
    { "file_name": "test_img_1.png", "detections": ["helmet","vest"] },
    { "file_name": "test_img_2.png", "detections": ["uninsulated_cable","no_gloves"] }
  ]
}
```
Response:
```json
{
  "report": "Drafted safety report text... (summary, non-compliances, recommendations)"
}
```

### 3) POST /api/process-image
Form-data: `files` = one or more images.  
Runs detection then report generation in one call. Returns same structure as above with `"report"`.

---

## ⚙️ Setup

### 1) Python env
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
```

### 2) Model
Ensure `security_model_v1.pt` is at the project root (as loaded by `services/object_detection.py` with `YOLO("../security_model_v1.pt")`).

### 3) API key
Create `config.py` at the project root **or** export an env var:
```python
# config.py
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
```

```bash
export OPENAI_API_KEY=sk-...   # PowerShell: $env:OPENAI_API_KEY="sk-..."
```

### 4) Run the API
```bash
uvicorn main:app --reload
# API docs at: http://127.0.0.1:8000/docs
```

---

## 🧪 Quick Tests (cURL)

**Detect only**
```bash
curl -X POST "http://127.0.0.1:8000/api/object-detection/detect-objects"   -H "accept: application/json"   -H "Content-Type: multipart/form-data"   -F "files=@data/test_img_1.png"   -F "files=@data/test_img_2.png"
```

**Generate report from detections**
```bash
curl -X POST "http://127.0.0.1:8000/api/report-generation/generate-report"   -H "Content-Type: application/json"   -d '{
        "detections_summary": [
          {"file_name":"test_img_1.png","detections":["helmet","vest"]},
          {"file_name":"test_img_2.png","detections":["no_gloves","uninsulated_cable"]}
        ]
      }'
```

**Full pipeline**
```bash
curl -X POST "http://127.0.0.1:8000/api/process-image"   -H "accept: application/json"   -H "Content-Type: multipart/form-data"   -F "files=@data/test_img_1.png"
```

---

## 📦 Requirements
(UTF‑16 file included in repo)
```
fastapi==0.115.4
openai==1.55.2
opencv-python==4.10.0.84
pillow==11.0.0
pydantic==2.9.2
ultralytics==8.3.28
uvicorn==0.32.0
```

---

## 🔒 Security & Compliance Notes
- **Privacy:** Do not upload personal data without consent. Strip EXIF and sensitive metadata from images.  
- **LLM output:** Treat as a **draft**. A qualified safety manager should review before use.  
- **Jurisdiction:** For Luxembourg compliance, keep a **maintained checklist** of legal clauses and map detections → obligations → recommendations.  
- **Production hardening:** auth (API keys/JWT), rate limiting, logging, PII handling, model monitoring.

---

## 🚧 Roadmap (suggested)
- Structured JSON report (sections: summary, findings, non‑compliance, actions).  
- Country-specific compliance templates (Luxembourg v1; EU/FR variants).  
- PDF export with company branding.  
- More detectors (workers-at-height, harness, nets, scaffolding).  
- Batch processing & async jobs.  
- Dockerization and CI.

---

## 🙌 Credits
Custom YOLO model: `security_model_v1.pt`  
Author: Daniel Calvo
