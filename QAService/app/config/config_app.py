import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding= "utf-8",
        extra="ignore"
    )

    app_name: str = "AI Agent Q/A service for Robot and RCS"
    ################# LLM Service Configuration #############
    ollama_base_url:str = "http://127.0.0.1:11434"
    api_key:str = "dzungapr6th"    
    model:str= "Deepseekv3"
    max_content_char: int = 8000
    ################# RAG Service Configuration #############
    rag_base_url:str = "http://127.0.0.1:8000"
    rag_top_k: int = 5
    
    ################# Other config ##########################
    threshold_score:float = 0.45

settings = Settings()