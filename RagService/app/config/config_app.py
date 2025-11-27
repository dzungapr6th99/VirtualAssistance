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
        extra="ignore",  # hoặc "allow" nếu bạn thích
    )

    app_name: str = "AI Agent RAG Service for Robot"
    
    ############### Milvus Configuration ###############
    milvus_host: str = "127.0.0.1"                # không cần http:// ở đây
    milvus_port: str = "19530"
    milvus_db_name: str = "default"
    milvus_collection: str = "robot_document"

    ############### Neo4j Configuration ###############
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "123456"

    ############### Api Url ###################
    embedding_api_base: str = "http://127.0.0.1:2010"
    embedding_api_path: str = "/embeddings"

    ############### Ollama ######################
    ollama_embedding_model:str = "nomic-embed-text"
    embedding_dim:int = 768
settings = Settings()  