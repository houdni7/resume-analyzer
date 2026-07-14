import asyncio
import base64
import json
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS
from routers import resume, match

app = FastAPI(title="Resume Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(match.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


def handler(event, context):
    method = event.get("method", "GET")
    path = event.get("path", "/")
    headers_raw = event.get("headers", {})
    query = event.get("queryParameters", {})
    body = event.get("body", "")
    is_base64 = event.get("isBase64Encoded", False)

    if is_base64 and body:
        body = base64.b64decode(body)
    elif isinstance(body, str):
        body = body.encode("utf-8")

    raw_headers = [(str(k).encode(), str(v).encode()) for k, v in headers_raw.items()]
    query_string = "&".join(f"{k}={v}" for k, v in query.items()).encode()

    scope = {
        "type": "http",
        "method": method.upper(),
        "path": path,
        "raw_path": path.encode(),
        "query_string": query_string,
        "headers": raw_headers,
        "scheme": "https",
        "server": ("", 80),
        "client": ("", 0),
        "http_version": "1.1",
    }

    response_status = 200
    response_headers = {}
    response_body = []

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message):
        nonlocal response_status, response_headers, response_body
        if message["type"] == "http.response.start":
            response_status = message["status"]
            for h in message.get("headers", []):
                response_headers[h[0].decode()] = h[1].decode()
        elif message["type"] == "http.response.body":
            if message.get("body"):
                response_body.append(message["body"])

    loop = asyncio.new_event_loop()
    loop.run_until_complete(app(scope, receive, send))
    loop.close()

    raw_body = b"".join(response_body)
    try:
        body_str = raw_body.decode("utf-8")
        is_base = False
    except UnicodeDecodeError:
        body_str = base64.b64encode(raw_body).decode("utf-8")
        is_base = True

    return {
        "statusCode": response_status,
        "headers": response_headers,
        "body": body_str,
        "isBase64Encoded": is_base,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
