import os
import httpx
from typing import Optional
from app.config.config_app import settings
class LlmClient:
    def __init__(
            self,
            base_url: Optional[str]= None,
            api_key: Optional[str]= None,
            model: Optional[str]= None,
    ):
        self.base_url = (base_url or settings.ollama_base_url)
        self.api_key = (api_key or settings.api_key)
        self.model = model or settings.model


    async def generate(self, system_prompt:str, user_prompt:str, temperature: float = 0.2)-> str:
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload = {
            "model": self.model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        async with httpx.AsyncClient(timeout=60.0, headers= headers) as client:
            resp = await client.post(f"{self.base_url}/chat/completions", json= payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
            