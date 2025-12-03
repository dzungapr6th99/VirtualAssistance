from fastapi import APIRouter, HTTPException
from app.models.query import SearchHit, SearchRequest, SearchResponse
from app.services.embedding_service import get_embeddings
from app.services.milvus_client import search_relevant_chunks

router = APIRouter(prefix= "/api/query", tags= ["search"])

@router.post("vector-database/search", response_model= SearchResponse)
async def vector_search(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query is empty")
    embeddings = await get_embeddings([request.query])
    if not embeddings:
        raise HTTPException(status_code=500, detail= "Failed to compute embedding")
    query_vec = embeddings[0]
    raw_hits = search_relevant_chunks(
        embedding= query_vec,
        top_k= request.top_k,
        project_id= request.project_id
    )

    hits = [
        SearchHit(
            chunk_id=h["chunk_id"],
            doc_id=h["doc_id"],
            section_title=h["section_title"],
            content=h["content"],
            score=h["score"],
        )
        for h in raw_hits
    ]
    return SearchResponse(hits= hits)