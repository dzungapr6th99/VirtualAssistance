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
    base_url = "http://127.0.0.1:11434"
    api_key = "dzungapr6th"    
    model= "Deepseekv3"
    ################# RAG Service Configuration #############

    ################# Other config ##########################
    threshold_score:float = 0.45

settings = Settings()