"""Protected user routes - require authentication"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.db_models import User, Resume, SavedJob
from routes.auth import require_auth
from services.resume_parser import parse_resume_structured
from services.llm_service import llm_service

router = APIRouter(prefix="/user", tags=["User"])


# Pydantic models for request/response validation
class SaveJobRequest(BaseModel):
    job_external_id: Optional[str] = None
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None
    match_percentage: Optional[int] = None
    matched_skills: Optional[List[str]] = []


class UpdateJobStatusRequest(BaseModel):
    status: str  # saved, applied, interviewing, rejected, offer
    notes: Optional[str] = None


# Resume endpoints
@router.get("/resumes")
async def get_user_resumes(
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Get all resumes for the current user"""
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return {
        "resumes": [
            {
                "id": r.id,
                "filename": r.filename,
                "skills": r.skills or [],
                "experience_years": r.experience_years,
                "quality_score": r.quality_score,
                "is_primary": r.is_primary,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in resumes
        ],
        "count": len(resumes)
    }


@router.post("/resumes/upload")
async def upload_user_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Upload and save a resume for the current user"""
    content = await file.read()
    result = parse_resume_structured(content, file.filename)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Check if this is the first resume (make it primary)
    existing_count = db.query(Resume).filter(Resume.user_id == current_user.id).count()
    is_primary = existing_count == 0

    # Analyze quality if LLM is available
    quality_analysis = None
    quality_score = None
    if llm_service.is_available():
        analysis = llm_service.analyze_resume_quality(
            result.get("text", ""),
            result.get("sections", {})
        )
        quality_score = analysis.get("score")
        quality_analysis = analysis

    # Create resume record
    resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        raw_text=result.get("text", ""),
        skills=result.get("skills", []),
        sections=result.get("sections", {}),
        experience_years=result.get("experience_years", 0),
        quality_score=quality_score,
        quality_analysis=quality_analysis,
        is_primary=is_primary,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "id": resume.id,
        "filename": resume.filename,
        "skills": resume.skills,
        "sections": resume.sections,
        "experience_years": resume.experience_years,
        "quality_score": resume.quality_score,
        "quality_analysis": resume.quality_analysis,
        "is_primary": resume.is_primary,
        "message": "Resume uploaded and saved successfully"
    }


@router.get("/resumes/{resume_id}")
async def get_resume(
    resume_id: int,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Get a specific resume by ID"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return {
        "id": resume.id,
        "filename": resume.filename,
        "raw_text": resume.raw_text,
        "skills": resume.skills or [],
        "sections": resume.sections or {},
        "experience_years": resume.experience_years,
        "quality_score": resume.quality_score,
        "quality_analysis": resume.quality_analysis,
        "is_primary": resume.is_primary,
        "created_at": resume.created_at.isoformat() if resume.created_at else None,
    }


@router.delete("/resumes/{resume_id}")
async def delete_resume(
    resume_id: int,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Delete a resume"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    db.delete(resume)
    db.commit()

    return {"message": "Resume deleted successfully"}


@router.put("/resumes/{resume_id}/primary")
async def set_primary_resume(
    resume_id: int,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Set a resume as the primary resume"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Unset current primary
    db.query(Resume).filter(
        Resume.user_id == current_user.id,
        Resume.is_primary == True
    ).update({"is_primary": False})

    # Set new primary
    resume.is_primary = True
    db.commit()

    return {"message": "Primary resume updated", "resume_id": resume_id}


# Saved jobs endpoints
@router.get("/saved-jobs")
async def get_saved_jobs(
    status: Optional[str] = None,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Get all saved jobs for the current user, optionally filtered by status"""
    query = db.query(SavedJob).filter(SavedJob.user_id == current_user.id)

    if status:
        query = query.filter(SavedJob.status == status)

    jobs = query.order_by(SavedJob.created_at.desc()).all()

    return {
        "saved_jobs": [
            {
                "id": j.id,
                "job_external_id": j.job_external_id,
                "title": j.title,
                "company": j.company,
                "location": j.location,
                "url": j.url,
                "source": j.source,
                "match_percentage": j.match_percentage,
                "matched_skills": j.matched_skills or [],
                "status": j.status,
                "notes": j.notes,
                "applied_at": j.applied_at.isoformat() if j.applied_at else None,
                "created_at": j.created_at.isoformat() if j.created_at else None,
            }
            for j in jobs
        ],
        "count": len(jobs)
    }


@router.post("/saved-jobs")
async def save_job(
    job: SaveJobRequest,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Save a job to the user's list"""
    # Check if already saved
    existing = db.query(SavedJob).filter(
        SavedJob.user_id == current_user.id,
        SavedJob.title == job.title,
        SavedJob.company == job.company
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Job already saved")

    saved_job = SavedJob(
        user_id=current_user.id,
        job_external_id=job.job_external_id,
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        url=job.url,
        source=job.source,
        match_percentage=job.match_percentage,
        matched_skills=job.matched_skills or [],
        status="saved",
    )
    db.add(saved_job)
    db.commit()
    db.refresh(saved_job)

    return {
        "id": saved_job.id,
        "message": "Job saved successfully"
    }


@router.put("/saved-jobs/{job_id}")
async def update_saved_job(
    job_id: int,
    update: UpdateJobStatusRequest,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Update a saved job's status or notes"""
    saved_job = db.query(SavedJob).filter(
        SavedJob.id == job_id,
        SavedJob.user_id == current_user.id
    ).first()

    if not saved_job:
        raise HTTPException(status_code=404, detail="Saved job not found")

    saved_job.status = update.status
    if update.notes is not None:
        saved_job.notes = update.notes

    # Track when user marks as applied
    if update.status == "applied" and not saved_job.applied_at:
        saved_job.applied_at = datetime.utcnow()

    db.commit()

    return {"message": "Job updated successfully", "status": saved_job.status}


@router.delete("/saved-jobs/{job_id}")
async def delete_saved_job(
    job_id: int,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Remove a saved job"""
    saved_job = db.query(SavedJob).filter(
        SavedJob.id == job_id,
        SavedJob.user_id == current_user.id
    ).first()

    if not saved_job:
        raise HTTPException(status_code=404, detail="Saved job not found")

    db.delete(saved_job)
    db.commit()

    return {"message": "Saved job removed"}


# Dashboard/stats endpoint
@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Get dashboard stats for the current user"""
    resume_count = db.query(Resume).filter(Resume.user_id == current_user.id).count()
    primary_resume = db.query(Resume).filter(
        Resume.user_id == current_user.id,
        Resume.is_primary == True
    ).first()

    # Job stats by status
    saved_count = db.query(SavedJob).filter(
        SavedJob.user_id == current_user.id,
        SavedJob.status == "saved"
    ).count()
    applied_count = db.query(SavedJob).filter(
        SavedJob.user_id == current_user.id,
        SavedJob.status == "applied"
    ).count()
    interviewing_count = db.query(SavedJob).filter(
        SavedJob.user_id == current_user.id,
        SavedJob.status == "interviewing"
    ).count()

    return {
        "user": {
            "name": current_user.name,
            "email": current_user.email,
        },
        "resumes": {
            "count": resume_count,
            "primary": {
                "id": primary_resume.id,
                "filename": primary_resume.filename,
                "skills_count": len(primary_resume.skills or []),
                "quality_score": primary_resume.quality_score,
            } if primary_resume else None,
        },
        "jobs": {
            "saved": saved_count,
            "applied": applied_count,
            "interviewing": interviewing_count,
            "total": saved_count + applied_count + interviewing_count,
        }
    }
