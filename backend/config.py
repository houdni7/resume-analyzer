import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
DASHSCOPE_MODEL = os.getenv("DASHSCOPE_MODEL", "qwen-plus")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))

OSS_BUCKET = os.getenv("OSS_BUCKET", "")
OSS_ENDPOINT = os.getenv("OSS_ENDPOINT", "")
OSS_ACCESS_KEY = os.getenv("OSS_ACCESS_KEY", "")
OSS_SECRET_KEY = os.getenv("OSS_SECRET_KEY", "")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
