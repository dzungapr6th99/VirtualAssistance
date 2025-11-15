from DataAccess import Neo4JHelper
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from Entities.Object import ChunkNode
import os
class GraphDbProcess:
    """class used to process business logic with graph db Neo4j"""
    def __init__(self, graphDbHelper: Neo4JHelper) -> None:
        self._graphDbHelper = graphDbHelper
    def StoreDocument(self, path: str):
        loader = PyPDFLoader(path)
        pages = loader.load
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(pages)

