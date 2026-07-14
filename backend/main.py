import sys
import json
import os
import base64
import asyncio
import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, "/code")

_err = None
_app = None

try:
    from config import CORS_ORIGINS
except Exception:
    _err = "CONFIG_FAIL: " + traceback.format_exc()
    CORS_ORIGINS = ["*"]

if not _err:
    try:
        from routers import resume, match
    except Exception:
        _err = "ROUTER_FAIL: " + traceback.format_exc()

if not _err:
    try:
        _app = FastAPI(title="Resume Analyzer API", version="1.0.0")
        _app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS,
                            allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
        _app.include_router(resume.router)
        _app.include_router(match.router)

        @_app.get("/api/health")
        async def health():
            return {"status": "ok"}

        @_app.get("/api/ping")
        async def ping():
            return {"ok": True}
    except Exception:
        _err = "APP_FAIL: " + traceback.format_exc()


def handler(event, context):
    try:
        if isinstance(event, bytes):
            event = json.loads(event.decode("utf-8"))
        elif isinstance(event, str):
            event = json.loads(event)
    except Exception:
        return {"statusCode": 500, "isBase64Encoded": False,
                "headers": {"content-type": "text/plain"},
                "body": "EVENT_PARSE_FAIL"}

    if _err:
        return {"statusCode": 500, "isBase64Encoded": False,
                "headers": {"content-type": "text/plain"}, "body": _err}

    request_context = event.get("requestContext", {})
    http_ctx = request_context.get("http", {})

    path = (event.get("path") or event.get("rawPath") or
            http_ctx.get("path") or "/")
    method = (event.get("method") or event.get("httpMethod") or
              http_ctx.get("method") or "GET")

    headers_raw = event.get("headers", {})
    body = event.get("body", "")
    is_base64 = event.get("isBase64Encoded", False)

    if is_base64 and body:
        body = base64.b64decode(body)
    elif isinstance(body, str):
        body = body.encode("utf-8")

    raw_headers = [(str(k).lower().encode(), str(v).encode()) for k, v in headers_raw.items()]
    query = event.get("queryParameters") or event.get("queryStringParameters") or {}
    if isinstance(query, str):
        query = {}
    query_string = "&".join(f"{k}={v}" for k, v in query.items() if v is not None).encode()

    scope = {
        "type": "http", "asgi": {"version": "3.0"},
        "method": method.upper(), "path": path,
        "raw_path": path.encode(), "query_string": query_string,
        "headers": raw_headers, "scheme": "https",
        "server": ("fc", 80), "client": ("fc", 0),
        "http_version": "1.1",
    }

    rstatus = 200
    rheaders = {}
    rbody = []

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message):
        nonlocal rstatus, rheaders, rbody
        if message["type"] == "http.response.start":
            rstatus = message["status"]
            for h in message.get("headers", []):
                rheaders[h[0].decode()] = h[1].decode()
        elif message["type"] == "http.response.body":
            if message.get("body"):
                rbody.append(message["body"])

    async def _run():
        await _app(scope, receive, send)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())

    raw_body = b"".join(rbody)
    try:
        body_str = raw_body.decode("utf-8")
        is_base = False
    except UnicodeDecodeError:
        body_str = base64.b64encode(raw_body).decode("utf-8")
        is_base = True

    return {"statusCode": rstatus, "headers": rheaders, "body": body_str, "isBase64Encoded": is_base}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
