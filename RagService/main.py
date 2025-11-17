from fastapi import FastAPI
from api import upload

app = FastAPI(title = "AI Agent RAG Service")
app.include_router(upload.router)