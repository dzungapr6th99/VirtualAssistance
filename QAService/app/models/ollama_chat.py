from pydantic import BaseModel
from typing import List, Literal, Optional
from datetime import datetime, timezone

RoleType = Literal["system", "user", "assistant"]

class OllamaChatMessage(BaseModel):
    role: RoleType
    content: str

class OllamaChatRequest(BaseModel):
    model:str
    messages: List[OllamaChatMessage]
    stream: Optional[bool] = True

class OllamaChatResponseMessage(BaseModel):
    role: RoleType =  "assistant"
    content:str

class OllamaChatResponse(BaseModel):
    model: str
    created_at:str
    message:OllamaChatResponseMessage
    done: bool = True

    total_duration: int = 0
    load_duration: int=0
    prompt_eval_duration: int = 0
    eval_count: int = 0
    eval_duration:int=0
    @staticmethod
    def now_iso()-> str:
        return datetime.now(timezone.utc).isoformat
