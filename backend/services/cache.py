import json
import hashlib


def _make_key(text: str, suffix: str = "") -> str:
    h = hashlib.md5(text.encode("utf-8")).hexdigest()
    return f"resume:md5:{h}{suffix}"


async def get_cached_analysis(resume_text: str):
    return None


async def set_cached_analysis(resume_text: str, data: dict) -> None:
    pass


async def get_cached_match(resume_text: str, jd_text: str):
    return None


async def set_cached_match(resume_text: str, jd_text: str, data: dict) -> None:
    pass
