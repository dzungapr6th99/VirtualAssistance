from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    project_id: Optional[str] = None
    query: str
    top_k: int = 5

class SearchHit(BaseModel):
    chunk_id:str
    doc_id: str
    section_title: str
    content: str
    score:float

class SearchResponse(BaseModel):
    hits: List[SearchHit]
    
class HybridSearchItem(BaseModel):
    chunk_id: str
    project_id: Optional[str] = None
    file_name:str
    section_title: Optional[str] = None
    content: str
    score: float
    source: str
    
class HybridSearchResponse(BaseModel):
    result: List[HybridSearchItem]