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
    chunk_id: Optional[str] = None
    project_id: Optional[str] = None
    file_name: Optional[str] = None
    section_title: Optional[str] = None
    content:  Optional[str] = None
    score:  Optional[float] = None 
    source:  Optional[str] = None
    
class HybridSearchResponse(BaseModel):
    results: List[HybridSearchItem]