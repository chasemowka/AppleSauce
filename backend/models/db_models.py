"""Database models for AppleSauce"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """User account model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    picture_url = Column(String(500), nullable=True)

    # OAuth fields
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    apple_id = Column(String(255), unique=True, nullable=True, index=True)

    # Account status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    saved_jobs = relationship("SavedJob", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    """User resume model"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Resume content
    filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=True)

    # Parsed data (stored as JSON)
    skills = Column(JSON, default=list)
    sections = Column(JSON, default=dict)
    experience_years = Column(Integer, default=0)

    # Quality analysis (from LLM)
    quality_score = Column(Integer, nullable=True)
    quality_analysis = Column(JSON, nullable=True)

    # Metadata
    is_primary = Column(Boolean, default=False)  # User's main resume
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="resumes")


class SavedJob(Base):
    """Saved/bookmarked jobs for a user"""
    __tablename__ = "saved_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Job data (denormalized for offline access)
    job_external_id = Column(String(255), nullable=True)  # ID from source API
    title = Column(String(500), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    url = Column(String(1000), nullable=True)
    source = Column(String(50), nullable=True)  # indeed, aws, etc.

    # Match data
    match_percentage = Column(Integer, nullable=True)
    matched_skills = Column(JSON, default=list)

    # User actions
    status = Column(String(50), default="saved")  # saved, applied, interviewing, rejected, offer
    notes = Column(Text, nullable=True)
    applied_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="saved_jobs")
