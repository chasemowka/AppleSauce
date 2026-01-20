from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.resume_parser import parse_resume
from services.job_matcher import match_jobs, get_suggestions
from services.job_api_service import job_api_service
import json

app = FastAPI(title="AppleSauce API", description="Resume matching and job search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse a resume (PDF or DOCX)"""
    content = await file.read()
    text = parse_resume(content, file.filename)
    return {"filename": file.filename, "text": text, "message": "Resume parsed successfully"}

@app.get("/jobs")
async def get_jobs(query: str = "software engineer", source: str = "all"):
    """
    Get job listings from multiple sources
    
    - query: Search keywords (e.g., "python developer", "data scientist")
    - source: "indeed", "aws", "netflix", "microsoft", "all"
    """
    jobs = []
    
    if source == "all" or source == "indeed":
        # Fetch from Indeed/JSearch
        indeed_jobs = job_api_service.search_indeed_jobs(query)
        jobs.extend(indeed_jobs)
    
    if source == "all" or source in ["aws", "amazon"]:
        aws_jobs = job_api_service.search_company_careers("aws", query)
        jobs.extend(aws_jobs)
    
    if source == "all" or source == "netflix":
        netflix_jobs = job_api_service.search_company_careers("netflix", query)
        jobs.extend(netflix_jobs)
    
    if source == "all" or source == "microsoft":
        microsoft_jobs = job_api_service.search_company_careers("microsoft", query)
        jobs.extend(microsoft_jobs)
    
    return {"jobs": jobs, "count": len(jobs), "query": query}

@app.get("/jobs/company/{company}")
async def get_company_jobs(company: str, keywords: str = ""):
    """
    Get jobs from specific company
    
    Supported companies: aws, netflix, microsoft, oracle, l3harris, openai
    """
    jobs = job_api_service.search_company_careers(company, keywords)
    return {"jobs": jobs, "company": company, "count": len(jobs)}

@app.post("/match")
async def match_resume(data: dict):
    """Match resume text to jobs and return scored results"""
    resume_text = data.get("resume_text", "")
    query = data.get("query", "software engineer")
    
    # Get jobs
    jobs = job_api_service.search_indeed_jobs(query)
    
    # Match and score
    matches = match_jobs(resume_text, jobs)
    return {"matches": matches, "count": len(matches)}

@app.post("/suggestions")
async def get_job_suggestions(data: dict):
    """Get resume improvement suggestions for a specific job"""
    resume_text = data.get("resume_text", "")
    job_id = data.get("job_id", 1)
    
    # For now, return generic suggestions
    # TODO: Integrate AWS Bedrock for AI-powered suggestions
    suggestions = [
        f"Add more keywords related to the job requirements",
        f"Highlight relevant projects and achievements",
        f"Quantify your accomplishments with metrics",
        f"Tailor your summary to match the job description"
    ]
    
    return {"suggestions": suggestions, "job_id": job_id}

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "running",
        "message": "AppleSauce API is running",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)