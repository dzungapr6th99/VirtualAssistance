import httpx
from typing import List, Optional
from app.models.rag import RagSearchRequest, RagSearchResponse, RagSearchResultItem
from app.models.projects import ProjectListResponse, ProjectMeta, ProjectSearchItem, ProjectSearchRequest, ProjectSearchResponse

class RagClient:
    def __init__(self, base_url:str):
        self._base_url = base_url.rstrip("/")
        

    async def search_chunks(
            self,
            query: str,
            top_k: int=3,
            project_ids:Optional[List[str]]= None,
    ) -> List[RagSearchResultItem]:
        req = RagSearchRequest(query= query, top_k= top_k, project_ids= project_ids)
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(f'{self._base_url}/search', json= req.model_dump())
            resp.raise_for_status()
            data = RagSearchResponse.model_validate(resp.json())
        return data.results
    
    async def list_projects(self) -> List[ProjectMeta]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(f"{self._base_url}/projects")
            resp.raise_for_status()
            data = ProjectListResponse.model_validate(resp.json())
        return data.projects
    
    async def search_projects(self, query:str, top_k: int = 3) -> List[ProjectSearchItem]:
        req = ProjectSearchRequest(query=query, top_k= top_k)
        async with httpx.AsyncClient(timeout= 20.0) as client:
            resp = await client.post(f"{self._base_url}/projects/search", json= req.model_dump)

