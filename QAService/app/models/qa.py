from typing import List, Optional
from pydantic import BaseModel

class QAHistoryMessage(BaseModel):
    role:str
    content:str
    
class QuestionRequest(BaseModel):
    question: str
    top_k: Optional[int] = None
    project_hint: Optional[str]= None
    history: List[QAHistoryMessage] = []
    
class SourceChunk(BaseModel):
    chunk_id: str
    project_id: str
    title: str
    content:str
    score:float
