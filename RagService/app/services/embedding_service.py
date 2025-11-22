from typing import List
import httpx
from app.config.config_app import settings

async def get_embeddings (texts: List[str])-> List[List[float]]:
    """
    Call embedding service: Post /embeddings
    Example: {"texts": ["...", "..."]}

    """
    url = settings.embedding_api_base + settings.embedding_api_path
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url=url, json={"texts": texts})
        resp.raise_for_status()
        data = resp.json()