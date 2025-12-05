import os
from functools import lru_cache
from app.services.rag_client import RagClient
from app.services.llm_client import LlmClient
from app.services.project_catalog import ProjectCatalog
from app.services.project_router import ProjectRouter
from app.services.qa_engine import QaEngine
from app.config.config_app import settings
@lru_cache 
def get_rag_client() -> RagClient:
    return RagClient(base_url=settings.ollama_base_url)

@lru_cache 
def get_llm_client() -> LlmClient:
    return LlmClient()

@lru_cache 
def get_project_catalog() -> ProjectCatalog:
    return ProjectCatalog(rag_client=get_rag_client())

def get_project_router() -> ProjectRouter:
    return ProjectRouter(rag_client= get_rag_client(), catalog= get_project_catalog())

def get_qa_engine() ->QaEngine:
    return QaEngine(
        rag_client= get_rag_client(),
        llm_client= get_llm_client(),
        project_catalog= get_project_catalog(),
        project_router= get_project_router(),
        
    )