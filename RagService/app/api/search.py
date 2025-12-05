from fastapi import APIRouter, HTTPException
from app.models.query import SearchHit, SearchRequest, SearchResponse, HybridSearchItem, HybridSearchResponse
from app.services.embedding_service import get_embeddings
from app.services.milvus_client import search_relevant_chunks
from app.services.neo4j_client import expand_related
from app.config.config_app import settings
router = APIRouter(prefix= "/api/query", tags= ["search"])

@router.post("vector-search", response_model= SearchResponse)
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

@router.post("hybrid-search", tags= ["search"])
async def hybrid_search(request: SearchRequest) -> HybridSearchResponse:
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query is empty")
    embeddings = await get_embeddings([request.query])
    if not embeddings:
        raise HTTPException(status_code=500, detail= "Failed to compute embedding")
    query_vec_chunks = embeddings[0]
    try:
        vector_chunks = search_relevant_chunks(
            embedding= query_vec_chunks,
            top_k= request.top_k,
            project_id= request.project_id
        )
        vector_chunks = [item for item in vector_chunks if item > settings.milvus_score_threshold]
    except Exception as ex:
        raise HTTPException(status_code=500, detail = f"Milvus search vector error: {ex}")
    
    try:
        graph_chunks = await expand_related(vector_chunks, request.top_k)
    except Exception as ex:
        raise HTTPException(status_code=500, detail= f"Neo4j search relation error: {ex}")
    all_items = []
    for c in vector_chunks:
        all_items.append(
            HybridSearchItem(
                chunk_id=c.get("chunk_id"),
                project_id=c.get("project_id"),
                file_name= "",
                section_title=c.get("section_title"),
                content=c.get("content"),
                score=float(c.get("score")),
                source="vector",
            )
        )
    for c in graph_chunks:
        all_items.append(
            HybridSearchItem(
                chunk_id= c.get("chunk_id"),
                project_id=c.get("project_id"),
                file_name= "",
                section_title=c.get("section_title"),
                content=c.get("content"),
                score=0,
                source="graph",
            )
        )
    
    all_items.sort(key=lambda x: x.score, reverse=True)
    top_items = all_items[: request.top_k]

    return HybridSearchResponse(results=top_items)