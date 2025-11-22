from pydantic import BaseModel 
from typing import List

""" 
Chunk record for document. The document will be split to many 
"""
class ChunkRecord(BaseModel):
    chunk_id: str
    project_id: str
    doc_id: str
    file_name: str
    section_title: str
    content: str

class ChunkCodeRecord(BaseModel):
    chunk_code_id: str
    project_id: str
    file_name: str
    file_path: str
    content: str
    function_name: str

class UpdloadResponse(BaseModel):
    project_id: str
    doc_id: str
    file_name: str
    chunk_count: int
    