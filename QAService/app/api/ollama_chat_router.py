from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
import httpx
import json 
import asyncio
from app.models.ollama_chat import OllamaChatRequest, OllamaChatResponse, OllamaChatResponseMessage
from app.models.ollama_stream import OllamaStreamMessage, OllamaStreamChunk
from app.models.ask import AskRequest
from app.services.qa_engine import QaEngine
from app.dependencies import get_project_catalog, get_qa_engine
from config.config_app import settings
router = APIRouter(prefix= "/api", tags=["ollama-chat"])

@router.post("/chat", response_model=OllamaChatResponse)
async def ollama_chat(
    req: OllamaChatRequest,
    engine: QaEngine = Depends(get_qa_engine)
):
    if req.stream is False or None:
        user_msgs = [m for m in req.messages if m.role == "user"]
        if not user_msgs:
            raise HTTPException(status_code=306, detail="No user message found")
        question = user_msgs[-1].content
        qa_req = AskRequest(question= question)
        qa_resp = await engine.ask(qa_req)
        msg = OllamaChatResponseMessage(
            role="assistant",
            content= qa_resp.answer
        )
        resp = OllamaChatResponse(
            model = req.model,
            created_at= OllamaChatResponse.now_iso(),
            message= msg,
            done=True,
            total_duration=0,
            load_duration= 0 ,
            prompt_eval_duration= 0,
            eval_count= 0,
            eval_duration= 0
        )
        return resp
    else: 
        user_msgs = [m for m in req.messages if m.role == "user"]
        if not user_msgs:
            raise HTTPException(status_code=400, detail="No user message found")
        question = user_msgs[-1].content
        system_prompt, user_prompt = await engine.build_prompt_only(question)
        backend_url = settings.base_url
        payload = {
            "model": req.model,
            "stream": True,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        async def stream_forward():
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream("POST", backend_url, json=payload) as resp:
                    async for line in resp.aiter_lines():
                        if not line:
                            continue
                        
                        yield line + "\n"
        return StreamingResponse(stream_forward(), media_type="application/x-ndjson")