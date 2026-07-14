from fastapi import APIRouter, File, UploadFile, HTTPException

from models.schemas import ApiResponse, ResumeAnalysis, ResumeRecord
from services.parser import parse_resume
from services.extractor import extract_resume_info
from services.cache import get_cached_analysis, set_cached_analysis

router = APIRouter(prefix="/api/resume", tags=["resume"])

_resume_store: dict[str, ResumeRecord] = {}
_analysis_store: dict[str, ResumeAnalysis] = {}


@router.post("/upload", response_model=ApiResponse)
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    content = await file.read()

    record = parse_resume(file.filename, content)
    _resume_store[record.resume_id] = record

    return ApiResponse(
        data=record.model_dump(),
        message="success",
    )


@router.post("/{resume_id}/analyze", response_model=ApiResponse)
async def analyze_resume(resume_id: str):
    record = _resume_store.get(resume_id)
    if not record:
        raise HTTPException(404, "Resume not found")

    # try cache first
    cached = await get_cached_analysis(record.raw_text)
    if cached:
        cached["resume_id"] = resume_id
        return ApiResponse(data=cached, message="success (cached)")

    analysis = extract_resume_info(record.raw_text)
    analysis.resume_id = resume_id
    _analysis_store[resume_id] = analysis

    data = analysis.model_dump()
    await set_cached_analysis(record.raw_text, data)

    return ApiResponse(data=data, message="success")


@router.get("/{resume_id}", response_model=ApiResponse)
async def get_resume(resume_id: str):
    record = _resume_store.get(resume_id)
    if not record:
        raise HTTPException(404, "Resume not found")

    analysis = _analysis_store.get(resume_id)

    result = record.model_dump()
    if analysis:
        result["analysis"] = analysis.model_dump()

    return ApiResponse(data=result, message="success")
