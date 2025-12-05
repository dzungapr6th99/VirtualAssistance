import os


############### Database Configuration ###############

############### Data Path ###############
UPLOAD_PATH = os.getenv("UPLOAD_PATH", "tmp/qa-data")

############### Number of log files ###############
LOGS_NUM = int(os.getenv("logs_num", "0"))

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore", 
    )

    app_name: str = "AI Agent RAG Service for Robot"
    
    ############### Milvus Configuration ###############
    milvus_host: str = "127.0.0.1"                # Don't need http here
    milvus_port: str = "19530"
    milvus_db_name: str = "default"
    milvus_collection: str = "robot_document"
    milvus_score_threshold: float = 0.55
    ############### Neo4j Configuration ###############
    neo4j_uri: str = "neo4j://127.0.0.1:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "12345678"
    neo4j_database_name: str = "rag-document"
    ############### Api Url ###################
    embedding_api_base: str = "http://127.0.0.1:2010"
    embedding_api_path: str = "/embeddings"

    ############### Ollama ######################
    ollama_embedding_model:str = "nomic-embed-text"
    embedding_dim:int = 768
settings = Settings()  