import json
import re
import urllib.request

from config import DASHSCOPE_API_KEY, DASHSCOPE_MODEL
from models.schemas import (
    BasicInfo, Background, EducationItem, JobIntention,
    ProjectItem, ResumeAnalysis, WorkItem,
)

EXTRACT_PROMPT = """你是一个专业的简历解析助手。请从以下简历文本中提取关键信息，严格以 JSON 格式返回。

要求：
1. 所有字段都必须存在，没有信息则使用空字符串 "" 或空数组 []。
2. 数字类型字段如无信息则返回 0。
3. 只返回 JSON，不要包含任何解释、markdown 代码块标记或其他文字。

返回格式：
{
  "basic_info": {"name": "姓名", "phone": "电话", "email": "邮箱", "address": "地址"},
  "job_intention": {"target_position": "期望职位", "expected_salary": "期望薪资"},
  "background": {
    "work_years": 0,
    "education": [{"degree": "学历", "school": "学校", "major": "专业", "year": "毕业时间"}],
    "projects": [{"name": "项目名称", "role": "担任角色", "description": "项目描述"}],
    "work_experience": [{"company": "公司", "position": "职位", "duration": "时间段", "description": "工作描述"}],
    "skills": ["技能1", "技能2"]
  }
}

简历文本：
{resume_text}
"""

DASHSCOPE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"


def _call_dashscope(prompt: str) -> str:
    body = json.dumps({"model": DASHSCOPE_MODEL, "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(DASHSCOPE_URL, data=body, headers={
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())["choices"][0]["message"]["content"]


def _clean_json(text: str) -> str:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    return m.group(1).strip() if m else text


def extract_resume_info(resume_text: str) -> ResumeAnalysis:
    if not DASHSCOPE_API_KEY:
        return _fallback_extract(resume_text)

    prompt = EXTRACT_PROMPT.replace("{resume_text}", resume_text[:3000])
    try:
        raw = _call_dashscope(prompt)
        data = json.loads(_clean_json(raw))
    except Exception:
        return _fallback_extract(resume_text)

    bi = data.get("basic_info", {})
    ji = data.get("job_intention", {})
    bg = data.get("background", {})
    try:
        return ResumeAnalysis(
            resume_id="",
            basic_info=BasicInfo(name=bi.get("name", ""), phone=bi.get("phone", ""),
                                 email=bi.get("email", ""), address=bi.get("address", "")),
            job_intention=JobIntention(target_position=ji.get("target_position", ""),
                                       expected_salary=ji.get("expected_salary", "")),
            background=Background(
                work_years=bg.get("work_years", 0),
                education=[EducationItem(**e) for e in bg.get("education", [])],
                projects=[ProjectItem(**p) for p in bg.get("projects", [])],
                work_experience=[WorkItem(**w) for w in bg.get("work_experience", [])],
                skills=bg.get("skills", []),
            ),
        )
    except Exception:
        return _fallback_extract(resume_text)


def _fallback_extract(text: str) -> ResumeAnalysis:
    return ResumeAnalysis(resume_id="", basic_info=BasicInfo(), job_intention=JobIntention(),
                          background=Background(skills=_extract_simple_skills(text)))


SKILL_KEYWORDS = [
    "Java", "Python", "Go", "Rust", "C++", "TypeScript", "JavaScript",
    "Spring Boot", "Spring", "Django", "Flask", "FastAPI",
    "MySQL", "PostgreSQL", "Redis", "MongoDB", "Elasticsearch",
    "Docker", "Kubernetes", "AWS", "阿里云", "Azure",
    "React", "Vue", "Angular", "Node.js", "Next.js",
    "Git", "Linux", "CI/CD", "微服务", "分布式",
]


def _extract_simple_skills(text: str) -> list[str]:
    return [kw for kw in SKILL_KEYWORDS if kw.lower() in text.lower()]
