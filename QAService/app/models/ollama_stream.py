from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime, timezone

RoleType = Literal["system", "user","assistant"]

class OllamaStreamMessage(BaseModel):
    role: RoleType = "assistant"
    content: str
class OllamaStreamChunk(BaseModel):
    model:str
    created_at:str
    message:OllamaStreamMessage
    done: bool = False

    #stats optional
    total_duration: int = 0
    load_duration: int = 0
    prompt_eval_count: int = 0
    prompt_eval_duration: int = 0
    eval_count: int = 0
    eval_duration: int = 0

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()