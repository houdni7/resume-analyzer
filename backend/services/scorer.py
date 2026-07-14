import re
from typing import Optional

from models.schemas import DimensionScores, MatchResult


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[\u4e00-\u9fa5\w]+", text.lower()))


def _keyword_score(jd_text: str, resume_text: str) -> float:
    jd_tokens = _tokenize(jd_text)
    if not jd_tokens:
        return 0.0
    resume_tokens = _tokenize(resume_text)
    overlap = jd_tokens & resume_tokens
    return len(overlap) / len(jd_tokens)


def rule_based_score(
    resume_text: str,
    resume_skills: list[str],
    job_description: str,
    work_years: int = 0,
) -> MatchResult:
    jd_lower = job_description.lower()
    resume_lower = resume_text.lower()

    # extract job keywords
    jd_tokens = _tokenize(jd_lower)
    resume_tokens = _tokenize(resume_lower)
    jd_skills = [t for t in jd_tokens if any(s.lower() in t for s in resume_skills)] or list(jd_tokens)[:10]
    matched = [s for s in resume_skills if s.lower() in " ".join(jd_skills).lower()]
    missing = [s for s in jd_skills if s not in matched]

    # dimension scores
    skill_rate = len(matched) / max(len(jd_skills), 1)
    exp_rel = _keyword_score(job_description, resume_text)
    edu_match = 1.0 if any(tag in jd_lower for tag in ["本科", "硕士", "博士", "学历"]) else 0.8
    proj_align = _keyword_score(
        re.sub(r"(本科|硕士|博士|\d{4})", "", job_description),
        resume_text,
    )

    overall = int(
        skill_rate * 35 + exp_rel * 30 + edu_match * 15 + proj_align * 20
    )

    return MatchResult(
        resume_id="",
        overall_score=min(overall, 100),
        dimensions=DimensionScores(
            skill_match_rate=round(skill_rate, 2),
            experience_relevance=round(exp_rel, 2),
            education_match=round(edu_match, 2),
            project_alignment=round(proj_align, 2),
        ),
        matched_skills=matched[:15],
        missing_skills=missing[:15],
        job_keywords=list(jd_skills)[:20],
        resume_keywords=list(matched)[:20],
    )
