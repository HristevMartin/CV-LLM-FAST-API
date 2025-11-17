from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import health_router, chat_router
from config.settings import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)

# routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "running"}