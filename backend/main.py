from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.resume_parser import parse_resume
from services.job_matcher import match_jobs, get_suggestions
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock job data
JOBS = [
    {"id": 1, "title": "Software Engineer", "company": "TechCorp", "skills": ["python", "javascript", "react"]},
    {"id": 2, "title": "Data Scientist", "company": "DataInc", "skills": ["python", "machine learning", "sql"]},
    {"id": 3, "title": "Frontend Developer", "company": "WebStudio", "skills": ["javascript", "react", "css"]}
]

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    text = parse_resume(content, file.filename)
    return {"message": "Resume uploaded", "text": text[:200] + "..."}

@app.get("/jobs")
async def get_jobs():
    return {"jobs": JOBS}

@app.post("/match")
async def match_resume(data: dict):
    resume_text = data.get("resume_text", "")
    matches = match_jobs(resume_text, JOBS)
    return {"matches": matches}

@app.get("/suggestions")
async def get_job_suggestions():
    suggestions = get_suggestions(JOBS)
    return {"suggestions": suggestions}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)