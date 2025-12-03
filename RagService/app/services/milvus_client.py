from pymilvus import connections, Collection, MilvusClient, FieldSchema, CollectionSchema, DataType, utility
from typing import List, Dict, Any, Optional
from app.config.config_app import settings
from app.models.chunk import ChunkRecord

collection_name = f"{settings.milvus_collection}_{settings.ollama_embedding_model.replace('-', '_')}"

#_client = MilvusClient(uri= f"{Settings.milvus_host}:{Settings.milvus_port}")

def ensure_collection(dim) -> Collection:
    """
    Check is collection suitable with embedding model
    """
    if not utility.has_collection(collection_name):
        print(f"[Milvus] Creating new collection: {collection_name} (dim={dim})")

        fields = [
            FieldSchema(name="chunk_id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
            FieldSchema(name="project_id", dtype=DataType.VARCHAR, max_length=64),
            FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=64),
            FieldSchema(name="section_title", dtype=DataType.VARCHAR, max_length=256),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=8192),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        ]

        schema = CollectionSchema(fields=fields, description="Auto-created RAG collection")

        col = Collection(
            name=collection_name,
            schema=schema,
            shards_num=2,
        )

        # Create vector index
        col.create_index(
            field_name="embedding",
            index_params={
                "metric_type": "COSINE",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 1024}
            }
        )

        print("[Milvus] Index created. Loading collection…")
        col.load()
        return col
    # Nếu đã tồn tại → load
    col = Collection(collection_name)
    col.load()
    return col


connections.connect(
    alias= "default",
    user= "",
    password= "",
    db_name= settings.milvus_db_name,
    host = settings.milvus_host,
    port = settings.milvus_port
)

ensure_collection(settings.embedding_dim)
_collection = Collection(collection_name)


def insert_chunks(chunks: List[ChunkRecord], embeddings: List[List[float]])-> None:
    chunk_ids = [c.chunk_id for c in chunks]
    project_ids = [c.project_id for c in chunks]
    doc_ids = [c.doc_id  for c in chunks]
    sections = [c.section_title for c in chunks]
    contents = [c.content for c in chunks]
    _collection.insert([
        chunk_ids,
        project_ids,
        doc_ids,
        sections,
        contents,
        embeddings
    ])

def search_relevant_chunks(
        project_id: Optional[str],
        embedding: List[float],
        top_k: int=5
) -> List[Dict[str, Any]]:
    """Search milvus by vector"""
    search_params = {
        "metric_type": "COSINE",
        "params":{"nprobe": 10}
    }

    expr = ""
    if (project_id):
        expr = f'project_id == "{project_id}"'
    results = _collection.search(
        data = [embedding],
        anns_field= "embedding",
        param= search_params,
        limit = top_k,
        expr= expr if expr else None,
        output_fields= ["chunk_id", "project_id", "doc_id", "section_title", "content"]
    )

    hits: List[Dict[Any, str]] = []

    for hit in results[0]:
        entity = hit.entity
        hits.append({
            "chunk_id": entity.get("chunk_id"),
            "doc_id": entity.get("doc_id"),
            "section_title": entity.get("section_title"),
            "content": entity.get("content"),
            "score": float(hit.distance),
        })
    return hits