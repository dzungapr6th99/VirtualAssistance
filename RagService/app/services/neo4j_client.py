from typing import List, Dict, Optional
from neo4j import GraphDatabase
from app.config.config_app import settings
from app.models.chunk import ChunkRecord

_driver = GraphDatabase.driver(
    settings.neo4j_uri,
    auth= (settings.neo4j_user, settings.neo4j_password),
    
)
_driver.verify_connectivity(database = settings.neo4j_database_name)
def write_graph(project_id: str, file_name: str, doc_id: str, chunks: List[ChunkRecord])-> None:
    with _driver.session(database = settings.neo4j_database_name) as session:
        session.execute_write(_write_graph_tx, project_id, file_name, doc_id, chunks)

async def expand_related(base_chunks:List[Dict], limit_per_doc: int = 3) -> List[Dict]:
    with _driver.session(database = settings.neo4j_database_name) as session:
        return session.execute_read(_query_realted, base_chunks, limit_per_doc)
        
def _write_graph_tx(tx, project_id:str, file_name:str, doc_id:str, chunks: List[ChunkRecord]):
    tx.run(
        """
        MERGE(p: Project {project_id: $project_id})
        MERGE(d: Document {doc_id: $doc_id})
            ON CREATE SET d.file_name = $file_name
        MERGE (p)-[:HAS_DOCUMENT]-> (d)
        """,
        project_id = project_id,
        doc_id = doc_id,
        file_name = file_name
    )
    section_map = {}
    for c in chunks:
        section_map.setdefault(c.section_title, []).append(c)

    for section_title in section_map.items():
        tx.run(
            """
            MATCH (p:Project {project_id: $project_id})-[:HAS_DOCUMENT]->(d:Document {doc_id: $doc_id})
            MERGE (s:Section {doc_id: $doc_id, title: $title})
            MERGE (d)-[:HAS_SECTION]->(s)           
            """,
            project_id = project_id,
            doc_id = doc_id,
            title=section_title
        )

def _query_graph_tx(tx, project_id: str, doc_id: Optional[str] = None, limit: int=50)-> List[Dict]:
    if doc_id:
        query = """
        MATCH (p:Project {project_id: $project_id})-[:HAS_DOCUMENT]->(d:Document {doc_id: $doc_id})
              -[:HAS_SECTION]->(s:Section)
        RETURN
            p.project_id AS project_id,
            d.doc_id     AS doc_id,
            d.file_name  AS file_name,
            s.title      AS section_title
        ORDER BY d.file_name, s.title
        LIMIT $limit
        """
        params = {
            "project_id": project_id,
            "doc_id": doc_id,
            "limit": limit
        }
        result = tx.run(query, **params)
    else:
        query = """
        MATCH (p:Project {project_id: $project_id})-[:HAS_DOCUMENT]->(d:Document)
              -[:HAS_SECTION]->(s:Section)
        RETURN
            p.project_id AS project_id,
            d.doc_id     AS doc_id,
            d.file_name  AS file_name,
            s.title      AS section_title
        ORDER BY d.file_name, s.title
        LIMIT $limit
        """
        params = {
            "project_id": project_id,
            "limit": limit
        }
        result = tx.run(query, **params)
    
    return [record.data() for record in result]

def _query_realted(tx, base_chunks:List[Dict], limit: int = 5
    )-> List[Dict]:
    results: List[Dict] = []
    for c in base_chunks:
        project_id= c.get("project_id")
        doc_id = c.get("doc_id")
        if not project_id or not doc_id:
            continue
        rows = _query_graph_tx(tx, project_id= project_id, doc_id= doc_id, limit= limit)
        results.extend(rows)
    return results
