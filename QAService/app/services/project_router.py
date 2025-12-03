from typing import List
from .rag_client import RagClient
from .project_catalog import ProjectCatalog
from app.config.config_app import settings
class ProjectRouter:
    """
    Analyse question to verify which project are relevant.
    """
    def __init__(self, rag_client:RagClient, catalog:ProjectCatalog):
        self._rag_client= rag_client
        self._catalog= catalog

    async def route(self, question: str) ->List[str]:
        results = await self._rag_client.search_projects(question, top_k= 3)
        if not results:
            return []
        
        project_ids = [r.project_id for r in results if r.score > settings.threshold_score]

        return project_ids

