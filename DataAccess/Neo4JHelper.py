from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from typing import TypeVar, Callable
from neo4j import GraphDatabase
from langchain_experimental.llms.ollama_functions import OllamaFunctions

import logging
T = TypeVar('T', bound = object)

class Neo4JHelper:
    def __init__(self, uri: str, user: str, password: str, graph: Neo4jGraph, graphLLM: OllamaFunctions):
        self._graph = graph
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._graphLLM = graphLLM
        
    def AddNode(self, func: Callable[[T], None], data: T) -> None:
        logging.info(msg = 'start insert Node with data ', object= data)
        with self._driver.session() as session:
            session.write_transaction(data)
            
    def AddDocument(self, docSplit: list[str], allowNode: list[str], allowRelationships: list[str], nodeProperties: list[str] )-> None:
        logging.info(msg= 'start insert graph Document with node '+ allowNode + 'properties ' + nodeProperties)
        graph_transformer = LLMGraphTransformer(
            llm= self._graphLLM, 
            allowed_nodes = allowNode,
            node_properties= nodeProperties,
            allowed_relationships= allowRelationships)
        graphDocument = graph_transformer.convert_to_graph_documents(docSplit)
        