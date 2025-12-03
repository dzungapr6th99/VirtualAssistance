from typing import List
from textwrap import dedent
from app.models.ask import AskRequest, AskResponse, AskSource
from app.models.rag import RagSearchResultItem
from .rag_client import RagClient
from .llm_client import LlmClient
from .project_catalog import ProjectCatalog
from .project_router import ProjectRouter

class QaEngine:
    def __init__(
            self, 
            rag_client:RagClient,
            llm_client:LlmClient,
            project_catalog:ProjectCatalog,
            project_router: ProjectRouter
               ):
        self._rag= rag_client
        self._llm = llm_client
        self._catalog = project_catalog
        self._router = project_router
    
    async def ask(self, req: AskRequest)-> AskResponse:
        project_ids = await self._router.route(req.question)
        results:List[RagSearchResultItem] = await self._rag.search_chunks(
            query= req.question,
            top_k= 5,
            project_ids=project_ids or None
        )
        if not results:
            return AskResponse(
                answer="No document was ragged"
            )
        context_blocks = []
        for idx, r in enumerate(results,start= 1):
            project_part = f" | Project: {r.project_name} " if r.project_name else ""
            header = f"[{idx}] (File: {r.file_name}{project_part} - Section: {r.section_title or ''})"
            context_blocks.append(f"{header}\n{r.content}")
        context_text = "\n\n".join(context_blocks)

        base_system_prompt = dedent("""
            You are a senior software engineer assistant.
            Answer in the same language as the user question.
            Only use the provided context blocks.
            If something is not clearly in the context, say you are not sure.
            When relevant, explicitly mention the project name based on the context.
            Always cite sources using [index] like [1], [2].
                                    """)
        system_prompt = base_system_prompt
        if self._catalog.system_prompt_fragment:
            system_prompt+="\n\n" + self._catalog.system_prompt_fragment
        user_prompt = f"""Question:
{req.question}

Context:
{context_text}
"""
        answer = await self._llm.generate(system_prompt= system_prompt, user_prompt= user_prompt, temperature= 0.2)

        sources = [
            AskSource(
                chunk_id= r.chunk_id,
                file_name=r.file_name,
                project_name=r.project_name,
                section_title= r.section_title,
                content_preview= (r.content[:300] + "...") if len(r.content) > 300 else r.content
            )
            for r in results
        ]
        return AskResponse(answer= answer, sources= sources)