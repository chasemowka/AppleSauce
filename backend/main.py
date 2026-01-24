from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.resume_parser import parse_resume_structured
from services.job_matcher import match_jobs, get_suggestions
from services.job_api_service import job_api_service
from services.clearance_filter import clearance_filter, ClearanceLevel
from services.llm_service import llm_service
from routes.auth import router as auth_router
from routes.user import router as user_router
from database import init_db
import json

app = FastAPI(title="AppleSauce API", description="Resume matching and job search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse a resume (PDF or DOCX), returning structured data"""
    content = await file.read()
    result = parse_resume_structured(content, file.filename)

    return {
        "filename": file.filename,
        "text": result.get("text", ""),
        "skills": result.get("skills", []),
        "sections": result.get("sections", {}),
        "experience_years": result.get("experience_years", 0),
        "message": "Resume parsed successfully" if "error" not in result else result["error"]
    }

@app.get("/jobs/clearance")
async def get_jobs_by_clearance(level: str = "none", query: str = "engineer", source: str = "all"):
    """
    Get job listings filtered by security clearance level
    
    - level: "none", "confidential", "secret", "top_secret"
    - query: Search keywords (e.g., "python developer", "data scientist")
    - source: "indeed", "aws", "netflix", "microsoft", "all"
    """
    # Get jobs using existing endpoint logic
    jobs = []
    
    if source == "all" or source == "indeed":
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
    
    # Filter by clearance level
    try:
        clearance_level = ClearanceLevel(level.lower())
    except ValueError:
        clearance_level = ClearanceLevel.NONE
    
    filtered_jobs = clearance_filter.filter_jobs_by_clearance(jobs, clearance_level)
    
    return {
        "jobs": filtered_jobs, 
        "count": len(filtered_jobs), 
        "query": query,
        "clearance_level": level
    }

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
    resume_skills = data.get("skills", [])  # Pre-extracted skills from resume
    query = data.get("query", "software engineer")

    # Get jobs
    jobs = job_api_service.search_indeed_jobs(query)

    # Match and score with weighted algorithm
    matches = match_jobs(resume_text, jobs, resume_skills if resume_skills else None)
    return {"matches": matches, "count": len(matches)}

@app.post("/suggestions")
async def get_job_suggestions(data: dict):
    """
    Get resume improvement suggestions for a specific job

    Request body:
    - resume_text: Full resume text
    - resume_skills: List of skills extracted from resume
    - job_title: Title of the job
    - job_description: Job description text
    - job_skills: Skills required by the job
    - matched_skills: Skills that matched between resume and job
    """
    resume_text = data.get("resume_text", "")
    resume_skills = data.get("resume_skills", [])
    job_title = data.get("job_title", "")
    job_description = data.get("job_description", "")
    job_skills = data.get("job_skills", [])
    matched_skills = data.get("matched_skills", [])

    # Use LLM service to generate personalized suggestions
    suggestions = llm_service.generate_job_suggestions(
        resume_text=resume_text,
        resume_skills=resume_skills,
        job_title=job_title,
        job_description=job_description,
        job_skills=job_skills,
        matched_skills=matched_skills
    )

    return {
        "suggestions": suggestions,
        "llm_powered": llm_service.is_available()
    }

@app.post("/resume/analyze")
async def analyze_resume(data: dict):
    """
    Analyze resume quality and provide feedback

    Request body:
    - resume_text: Full resume text
    - sections: Dictionary of detected sections (optional)
    """
    resume_text = data.get("resume_text", "")
    sections = data.get("sections", {})

    analysis = llm_service.analyze_resume_quality(resume_text, sections)

    return {
        "analysis": analysis,
        "llm_powered": llm_service.is_available()
    }

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "running",
        "message": "AppleSauce API is running",
        "docs": "/docs",
        "llm_available": llm_service.is_available()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)