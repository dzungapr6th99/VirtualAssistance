from typing import List
from textwrap import dedent
from app.models.projects import ProjectMeta
from .rag_client import RagClient

class ProjectCatalog:
    """
    Store meta data of pfoject + build system prompt fagment for RAG/Neo4j
    """

    def __init__(self, rag_client:RagClient):
        self._rag_client = rag_client
        self.projects:List[ProjectMeta] = []
        self.system_prompt_fragment:str = ""

    async def refresh(self)-> None:
        """
        Call Rag Service to get list of projects which are ragged.
        Then retbuild the prompt
        """
        projects = await self._rag_client.list_projects()
        self.projects = projects
        self.system_prompt_fragment = self._build_system_prompt_fragment(projects)

    def _build_system_prompt_fragment(self, projects: List[ProjectMeta])-> str:
        if not projects:
            return ""
        lines = ["These are the list overview of project which are ragged in the system", ""]
        for p in projects:
            lines.append(f"[{p.project_id}]")
            lines.append(f" - Title: {p.title}")
            if p.description:
                lines.append(f"- Description: {','.join(p.description)}")
            if p.aliases:
                lines.append(f"- Aliases: {','.join(p.aliases)}")
            if p.tags:
                lines.append(f"- Tags: {','.join(p.tags)}")
            lines.append[""]
        return dedent("\n".join(lines))
    
