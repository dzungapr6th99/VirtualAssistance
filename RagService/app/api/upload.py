from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from uuid import uuid4
from typing import List

from app.models.chunk import ChunkRecord, UpdloadResponse
from app.services.chunker import chunk_text
from app.services.embedding_service import get_embeddings
from app.services.milvus_client import insert_chunks
from app.services.neo4j_client import write_graph
from app.services.markdown_parser import parse_markdown_with_sections

router = APIRouter(prefix="/api/documents", tags= ["documents"])

@router.post("/upload", response_model= UpdloadResponse)
async def upload_markdown(
    file: UploadFile = File(...),
    project_id: str = Form("default")
):
    if not file.filename.endswith(".md") and file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail = "File must be .md or .txt")
    
    content_bytes = await file.read()
    md_text = content_bytes.decode("utf-8", errors= "ignore")

    sections = parse_markdown_with_sections(md_text)

    if not sections:
        raise HTTPException(status_code=400, detail="No content found in file")
    
    doc_id = str(uuid4())
    file_name = file.filename

    chunk_records: List[ChunkRecord] = []
    texts_for_embedding: List[str] = []

    for section_title, text_block in sections:
        chunk_texts = chunk_text(text_block, max_chars= 1000, overlap=200)
        for chunk in chunk_texts:
            if not chunk.strip():
                continue
            chunk_id = str(uuid4())
            record = ChunkRecord(
                chunk_id= chunk_id,
                project_id= project_id,
                doc_id= doc_id,
                file_name= file_name,
                section_title= section_title,
                content= chunk
            )
            chunk_records.append(record)
            texts_for_embedding.append(chunk)
    
    if not chunk_records:
        raise HTTPException(status_code= 400, detail= "")
    embeddings = await get_embeddings(texts_for_embedding)
    if len(embeddings) != len (chunk_records):
        raise HTTPException(status_code=500, detail="Embedding length mismatch")
    
    insert_chunks(chunk_records, embeddings= embeddings)
    write_graph (project_id= project_id, doc_id= doc_id, file_name=file_name, chunks= chunk_records)

    return UpdloadResponse(
        project_id= project_id,
        doc_id= doc_id,
        file_name= file_name,
        chunk_count= len(chunk_records)
    )


