from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    project_id: str = "default"
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