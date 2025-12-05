from pydantic import BaseModel
from typing import List, Optional

class RagSearchRequest(BaseModel):
    query:str
    top_k: int = 5
    project_ids:Optional[List[str]]= None

class RagSearchResultItem(BaseModel):
    chunk_id: str
    file_name: str
    content: str
    score: float
    #optional data
    project_id: Optional[str] = None
    section_title: Optional[str] = None

class RagSearchResponse(BaseModel):
    results: List[RagSearchResultItem]
