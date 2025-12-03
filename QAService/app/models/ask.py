from pydantic import BaseModel
from typing import List, Optional

class AskRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

class AskSource(BaseModel):
    chunk_id: str
    file_name: str
    project_name: Optional[str] = None
    section_title: Optional[str] = None
    content_preview:str

class AskResponse(BaseModel):
    answer: str
    sources: List[AskSource]


