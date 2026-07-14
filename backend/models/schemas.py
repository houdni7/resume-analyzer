from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


def gen_id() -> str:
    return uuid.uuid4().hex[:12]



class ResumeStructured(BaseModel):
    sections: list[str] = []


class ResumeRecord(BaseModel):
    resume_id: str = Field(default_factory=gen_id)
    filename: str = ""
    status: str = "uploaded"
    raw_text: str = ""
    structured: ResumeStructured = Field(default_factory=ResumeStructured)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())



class BasicInfo(BaseModel):
    name: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""


class JobIntention(BaseModel):
    target_position: str = ""
    expected_salary: str = ""


class EducationItem(BaseModel):
    degree: str = ""
    school: str = ""
    major: str = ""
    year: str = ""


class ProjectItem(BaseModel):
    name: str = ""
    role: str = ""
    description: str = ""


class WorkItem(BaseModel):
    company: str = ""
    position: str = ""
    duration: str = ""
    description: str = ""


class Background(BaseModel):
    work_years: int = 0
    education: list[EducationItem] = []
    projects: list[ProjectItem] = []
    work_experience: list[WorkItem] = []
    skills: list[str] = []


class ResumeAnalysis(BaseModel):
    resume_id: str
    basic_info: BasicInfo = Field(default_factory=BasicInfo)
    job_intention: JobIntention = Field(default_factory=JobIntention)
    background: Background = Field(default_factory=Background)


class DimensionScores(BaseModel):
    skill_match_rate: float = 0.0
    experience_relevance: float = 0.0
    education_match: float = 0.0
    project_alignment: float = 0.0


class MatchResult(BaseModel):
    resume_id: str
    overall_score: int = 0
    dimensions: DimensionScores = Field(default_factory=DimensionScores)
    matched_skills: list[str] = []
    missing_skills: list[str] = []
    ai_comment: str = ""
    job_keywords: list[str] = []
    resume_keywords: list[str] = []


# --- API Envelope ---

class ApiResponse(BaseModel):
    code: int = 0
    data: Optional[dict | list] = None
    message: str = "success"
