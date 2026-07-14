import re
import hashlib
from io import BytesIO

from pypdf import PdfReader

from models.schemas import ResumeRecord, ResumeStructured


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


def clean_text(raw: str) -> str:
    raw = re.sub(r"[ \t]{2,}", " ", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    return raw.strip()


def segment_sections(text: str) -> list[str]:
    section_headers = [
        "个人信息", "基本信息", "个人资料",
        "教育背景", "教育经历", "学习经历",
        "工作经历", "工作经验", "职业经历",
        "项目经历", "项目经验",
        "技能", "专业技能", "技术栈",
        "自我评价", "个人评价",
    ]
    pattern = "|".join(re.escape(h) for h in section_headers)
    parts = re.split(rf"(\n?(?:{pattern})\n?)", text, flags=re.IGNORECASE)
    sections = []
    current = ""
    for part in parts:
        stripped = part.strip()
        if not stripped:
            continue
        if re.match(rf"^({pattern})$", stripped, re.IGNORECASE):
            if current:
                sections.append(current)
            current = stripped
        else:
            current += "\n" + part
    if current:
        sections.append(current)
    return sections if sections else [text]


def md5_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def parse_resume(filename: str, file_bytes: bytes) -> ResumeRecord:
    raw = extract_text_from_pdf(file_bytes)
    cleaned = clean_text(raw)
    sections = segment_sections(cleaned)
    return ResumeRecord(
        filename=filename,
        raw_text=cleaned,
        structured=ResumeStructured(sections=sections),
        status="parsed",
    )
