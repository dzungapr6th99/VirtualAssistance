from pymilvus import connections, Collection, MilvusClient
from typing import List
from app.config.config_app import Settings
from app.models.chunk import ChunkRecord

connections.connect(
    alias= "default",
    user= "",
    password= "",
    db_name= Settings.milvus_db_name,
    host = Settings.milvus_host,
    port = Settings.milvus_port
)


_collection = Collection(Settings.milvus_collection)

def insert_chunks(chunks: List[ChunkRecord], embeddings: List[List[float]])-> None:
    chunk_ids = [c.chunk_id for c in chunks]
    project_ids = [c.project_id for c in chunks]
    doc_ids = [c.doc_id  for c in chunks]
    sections = [c.section for c in chunks]
    contents = [c.content for c in chunks]
    _collection.insert()
