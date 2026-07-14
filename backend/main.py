import traceback

def handler(event, context):
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from config import CORS_ORIGINS
        from routers import resume, match

        app = FastAPI(title="Test")
        app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
        app.include_router(resume.router)
        app.include_router(match.router)

        return {"statusCode": 200, "headers": {"content-type": "text/plain"}, "body": "all imports ok"}
    except Exception as e:
        return {"statusCode": 200, "headers": {"content-type": "text/plain"}, "body": traceback.format_exc()}
