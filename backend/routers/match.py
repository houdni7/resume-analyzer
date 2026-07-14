import json

from fastapi import APIRouter, HTTPException

from models.schemas import ApiResponse, MatchResult
from services.scorer import rule_based_score
from services.cache import get_cached_match, set_cached_match

router = APIRouter(prefix="/api/match", tags=["match"])

from routers.resume import _resume_store, _analysis_store


@router.post("", response_model=ApiResponse)
async def match_resume(body: dict):
    resume_id = body.get("resume_id")
    job_description = body.get("job_description", "")

    if not resume_id:
        raise HTTPException(400, "resume_id is required")
    if not job_description:
        raise HTTPException(400, "job_description is required")

    record = _resume_store.get(resume_id)
    if not record:
        raise HTTPException(404, "Resume not found")

    analysis = _analysis_store.get(resume_id)
    skills = analysis.background.skills if analysis else []
    work_years = analysis.background.work_years if analysis else 0

    # try cache
    cached = await get_cached_match(record.raw_text, job_description)
    if cached:
        cached["resume_id"] = resume_id
        return ApiResponse(data=cached, message="success (cached)")

    result = rule_based_score(
        resume_text=record.raw_text,
        resume_skills=skills,
        job_description=job_description,
        work_years=work_years,
    )
    result.resume_id = resume_id

    # try AI comment
    try:
        from config import DASHSCOPE_API_KEY, DASHSCOPE_MODEL
        import urllib.request

        if DASHSCOPE_API_KEY:
            prompt = f"""你是一个专业的简历匹配助手。请根据以下信息给出60字以内的简历匹配评价。

岗位描述：{job_description}

候选人技能：{', '.join(skills) if skills else '无'}
工作年限：{work_years}年
规则匹配得分：{result.overall_score}/100
匹配技能：{', '.join(result.matched_skills[:5])}
缺失技能：{', '.join(result.missing_skills[:5])}

请给出简短评价："""
            body = json.dumps({"model": DASHSCOPE_MODEL, "messages": [{"role": "user", "content": prompt}]}).encode()
            req = urllib.request.Request(
                "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                data=body,
                headers={"Authorization": f"Bearer {DASHSCOPE_API_KEY}", "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                result.ai_comment = data["choices"][0]["message"]["content"].strip()
    except Exception:
        pass

    data = result.model_dump()
    await set_cached_match(record.raw_text, job_description, data)

    return ApiResponse(data=data, message="success")
