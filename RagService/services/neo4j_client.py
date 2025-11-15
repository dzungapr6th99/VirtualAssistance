from typing import List
from neo4j import GraphDatabase
from RagService.config.config_app import Settings
from RagService.models.chunk import ChunkRecord

_driver = GraphDatabase.driver(
    Settings.neo4j_uri,
    auth= (Settings.neo4j_user, Settings.neo4j_password)
)

def write_graph(project_id: str, file_name: str, doc_id: str, chunks: List[ChunkRecord])-> None:
    with _driver.session() as session:
        session.execute_write(_write_graph_tx, project_id, file_name, doc_id, chunks)

def _write_graph_tx(tx, project_id:str, file_name:str, doc_id:str, chunks: List[ChunkRecord]):
    tx.run(
        """
        MERGE(p: Project {project_id: $project_id})
        MERGE(d: Document {doc_id: $doc_id})
            ON CREATE SET d.file_name = $filename
        MERGE (p)-[:HAS_DOCUMENT]-> (d)
        """,
        project_id = project_id,
        doc_id = doc_id,
        file_name = file_name
    )
    