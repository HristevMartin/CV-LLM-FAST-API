import logging

from fastapi import FastAPI

logger = logging.getLogger("uvicorn.error")
app = FastAPI(title="CV Chatbot API", version="1.0.0")
