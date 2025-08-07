"""Vector store service for document embeddings and retrieval."""

import os
from typing import List, Dict, Any, Optional

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

from app.core.config import settings


class VectorStoreService:
    """Service for managing document embeddings and retrieval."""
    
    def __init__(self):
        """Initialize the vector store service."""
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    async def create_vector_store(self, documents: List[Dict[str, Any]]) -> FAISS:
        """Create a vector store from document chunks.
        
        Args:
            documents: List of document chunks with text and metadata
            
        Returns:
            FAISS vector store
        """
        # Convert dictionaries back to Document objects
        docs = [
            Document(
                page_content=doc["page_content"],
                metadata=doc["metadata"]
            )
            for doc in documents
        ]
        
        # Create vector store
        vector_store = FAISS.from_documents(docs, self.embeddings)
        return vector_store
    
    async def similarity_search(
        self, 
        vector_store: FAISS, 
        query: str, 
        k: int = 4
    ) -> List[Document]:
        """Perform similarity search on the vector store.
        
        Args:
            vector_store: FAISS vector store
            query: Query string
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        return vector_store.similarity_search(query, k=k)
    
    async def save_vector_store(self, vector_store: FAISS, index_name: str) -> str:
        """Save the vector store to disk.
        
        Args:
            vector_store: FAISS vector store
            index_name: Name for the index
            
        Returns:
            Path where the vector store was saved
        """
        # Create directory if it doesn't exist
        save_path = os.path.join(settings.DOCUMENT_STORAGE_PATH, "vector_stores")
        os.makedirs(save_path, exist_ok=True)
        
        # Save vector store
        index_path = os.path.join(save_path, index_name)
        vector_store.save_local(index_path)
        
        return index_path
    
    async def load_vector_store(self, index_path: str) -> Optional[FAISS]:
        """Load a vector store from disk.
        
        Args:
            index_path: Path to the vector store
            
        Returns:
            FAISS vector store or None if not found
        """
        if not os.path.exists(index_path):
            return None
        
        return FAISS.load_local(index_path, self.embeddings)
