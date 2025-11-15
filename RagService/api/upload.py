from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from uuid import uuid4
from typing import List

from RagService.models.chunk import ChunkRecord, UpdloadResponse
from RagService.services.chunker import chunk_text
from RagService.services.embedding_service import get_embeddings
from RagService.services.milvus_client import insert_chunks
from RagService.services.neo4j_client import write_graph

router = APIRouter(prefix="/api/documents", tags= ["documents"])

@router.post("/upload", response_model= UpdloadResponse)
async def upload_markdown(
    file:UploadFile = File(...),
    project_id: str = Form("default")
):
    