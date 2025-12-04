from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    project_id: str = ""
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