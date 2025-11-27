from fastapi import FastAPI
from app.api import upload
from app.config.config_app import settings
from app.services.milvus_client import ensure_collection

app = FastAPI(title = "AI Agent RAG Service")
app.include_router(upload.router)

# @app.on_event("startup")
# async def on_startup():
#     print(">>> FASTAPI STARTUP")
#     ensure_collection(settings.embedding_dim)