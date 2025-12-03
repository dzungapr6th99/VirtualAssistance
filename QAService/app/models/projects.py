from pydantic import BaseModel
from typing import List, Optional

class ProjectMeta(BaseModel):
    project_id: str
    title:str
    description:Optional[str]= None
    aliases: List[str] = []
    tags: List[str] = []


class ProjectListResponse(BaseModel):
    projects: List[ProjectMeta]

class ProjectSearchRequest(BaseModel):
    query: str
    top_k: int = 3

class ProjectSearchItem(BaseModel):
    project_id:str
    title: str
    score: float
    description: Optional[str] = None

class ProjectSearchResponse(BaseModel):
    results:List[ProjectSearchItem]