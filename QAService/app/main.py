from fastapi import FastAPI
from app.api import ollama_chat_router
from app.config.config_app import settings

app = FastAPI(title="AI Agent QA Service")
app.include_router(ollama_chat_router.router)
