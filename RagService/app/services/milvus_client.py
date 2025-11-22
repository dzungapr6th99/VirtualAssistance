from pymilvus import connections, Collection, MilvusClient
from typing import List
from app.config.config_app import settings
from app.models.chunk import ChunkRecord


connections.connect(
    alias= "default",
    user= "",
    password= "",
    db_name= settings.milvus_db_name,
    host = settings.milvus_host,
    port = settings.milvus_port
)
#_client = MilvusClient(uri= f"{Settings.milvus_host}:{Settings.milvus_port}")

_collection = Collection(settings.milvus_collection)

def insert_chunks(chunks: List[ChunkRecord], embeddings: List[List[float]])-> None:
    chunk_ids = [c.chunk_id for c in chunks]
    project_ids = [c.project_id for c in chunks]
    doc_ids = [c.doc_id  for c in chunks]
    sections = [c.section for c in chunks]
    contents = [c.content for c in chunks]
    _collection.insert()
