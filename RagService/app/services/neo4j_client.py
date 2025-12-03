from typing import List
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

    for section_title, section_chunks in section_map.items():
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

        for c in section_chunks:
            tx.run(
                """
                    MATCH (s:Section {doc_id: $doc_id, title: $title})
                    MERGE (ch:Chunk {chunk_id: $chunk_id})
                      ON CREATE SET ch.preview = $preview
                   MERGE (s)-[:HAS_CHUNK]->(ch)            
                """,
                doc_id = doc_id,
                title = section_title,
                chunk_id = c.chunk_id,
                preview = c.content[:200]
                )

    