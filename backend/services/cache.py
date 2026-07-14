import json
import hashlib

try:
    import redis.asyncio as aioredis
    _has_redis = True
except ImportError:
    _has_redis = False

from config import REDIS_URL, CACHE_TTL

_pool = None


async def get_redis():
    if not _has_redis:
        return None
    global _pool
    if _pool is None:
        _pool = aioredis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)
    return aioredis.Redis(connection_pool=_pool)


def _make_key(resume_text: str, suffix: str = "") -> str:
    h = hashlib.md5(resume_text.encode("utf-8")).hexdigest()
    return f"resume:md5:{h}{suffix}"


async def get_cached_analysis(resume_text: str):
    try:
        r = await get_redis()
        if r is None:
            return None
        raw = await r.get(_make_key(resume_text, ":analysis"))
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None


async def set_cached_analysis(resume_text: str, data: dict) -> None:
    try:
        r = await get_redis()
        if r is None:
            return
        await r.set(_make_key(resume_text, ":analysis"), json.dumps(data, ensure_ascii=False), ex=CACHE_TTL)
    except Exception:
        pass


async def get_cached_match(resume_text: str, jd_text: str):
    try:
        r = await get_redis()
        if r is None:
            return None
        combined = resume_text + "|||" + jd_text
        raw = await r.get(_make_key(combined, ":match"))
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None


async def set_cached_match(resume_text: str, jd_text: str, data: dict) -> None:
    try:
        r = await get_redis()
        if r is None:
            return
        combined = resume_text + "|||" + jd_text
        await r.set(_make_key(combined, ":match"), json.dumps(data, ensure_ascii=False), ex=CACHE_TTL)
    except Exception:
        pass


async def close_redis():
    global _pool
    if _pool:
        await _pool.disconnect()
        _pool = None
