
from typing import List
import chromadb
from langchain_core.documents import Document
from llm import create_embedding_model
from models import ConfluencePage
import google.generativeai as genai
from logger import logger 

class GeminiEmbeddingFunction(chromadb.EmbeddingFunction):
  def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
    model = 'models/embedding-001'
    title = "Embedding of single string"
    return genai.embed_content(model=model,
                                content=input,
                                task_type="retrieval_document",
                                title=title)["embedding"]
    
class VectorStorage:
    def __init__(self):
        self.gemini_embeddings = create_embedding_model()
        chroma_client = chromadb.PersistentClient(path="data")
        collection_name= "confluence"
        try:
            self.db = chroma_client.get_collection(collection_name,embedding_function=GeminiEmbeddingFunction())
        except ValueError:
            self.db = chroma_client.create_collection(name="confluence", embedding_function=GeminiEmbeddingFunction())
        
    def insert(self, page: ConfluencePage):
        document = self.query_by_id(page.title)
        if document is not None and len(document["documents"]) > 0:
            logger.debug(f"Document {page.title} already exists in the database")
            return
        
        documents: List[str] = [page.page_content]
        metadatas: List[any] = [{
            "space": page.space,
            "title": page.title,
            "link": page.link,
            "num_tokens": page.num_tokens
        
        }]
        ids: List[str] = [page.title]
    
        self.db.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
            )
        
    def search(self, query: str, top_k: int = 10) -> List[Document]:
        docs: chromadb.QueryResult = self.db.query(query_texts=[query], n_results=top_k)
        
        logger.debug(f"Search results: {docs}")
        
        if docs is None or docs['documents'] is None or len(docs['documents']) == 0 or len(docs['documents'][0]) == 0:
            return []
        
        result: List[Document] = []
        for doc in docs['documents'][0]:
            result.append(Document(
                page_content=doc,
            ))
        return result
    
    def query_by_id(self, id: str) -> Document:
        return self.db.get(ids=[id])