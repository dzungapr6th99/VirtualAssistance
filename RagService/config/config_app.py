import os


############### Database Configuration ###############

############### Data Path ###############
UPLOAD_PATH = os.getenv("UPLOAD_PATH", "tmp/qa-data")

############### Number of log files ###############
LOGS_NUM = int(os.getenv("logs_num", "0"))

from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Agent RAG Service for Robot"
    
    ############### Milvus Configuration ###############
    milvus_host: str = os.getenv("MILVUS_HOST", "127.0.0.1")
    milvus_port: str = os.getenv("MILVUS_PORT", "19530")
    milvus_db_name: str = os.getenv("MILVUS_DB_NAME", "default")
    milvus_collection: str = os.getenv("MILVUS_COLLECTION", "robot_document")
    
    ############### Neo4j Configuration ###############
    neo4j_uri:str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "123456")

    ############### Api Url ###################
    embedding_api_base: str = os.getenv("EMBEDDING_API_BASE", "http://127.0.0.1:2010")
    embedding_api_path: str = os.getenv("EMBEDDING_PATH", "/embeddings")