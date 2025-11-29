from typing import List
import httpx
from app.config.config_app import settings
import ollama


async def get_embeddings (texts: List[str])-> List[List[float]]:
    """
    Call embedding service: Post /embeddings
    Example: {"texts": ["...", "..."]}

    """
    model = settings.ollama_embedding_model
    vectors = []
    for t in texts:
        resp = ollama.embeddings(model= model, prompt= t)
        vectors.append(resp["embedding"])
    return vectors
