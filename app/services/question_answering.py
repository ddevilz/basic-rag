"""Question answering service using LangChain and LLMs."""

from typing import List, Dict, Any

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS

from app.core.config import settings


class QuestionAnsweringService:
    """Service for answering questions based on document context."""
    
    def __init__(self):
        """Initialize the question answering service."""
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    async def answer_question(
        self, 
        vector_store: FAISS, 
        question: str
    ) -> Dict[str, Any]:
        """Answer a question based on the document context.
        
        Args:
            vector_store: FAISS vector store containing document embeddings
            question: Question to answer
            
        Returns:
            Dictionary with answer and metadata
        """
        # Create retrieval QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True
        )
        
        # Get answer
        result = qa_chain({"query": question})
        
        # Extract source documents
        source_docs = result.get("source_documents", [])
        
        # Format response
        return {
            "question": question,
            "answer": result["result"],
            "confidence": 0.9,  # Placeholder - could implement actual confidence scoring
            "context": [doc.page_content for doc in source_docs],
            "sources": [doc.metadata.get("source", "unknown") for doc in source_docs]
        }
    
    async def batch_answer_questions(
        self, 
        vector_store: FAISS, 
        questions: List[str]
    ) -> List[Dict[str, Any]]:
        """Answer multiple questions based on the document context.
        
        Args:
            vector_store: FAISS vector store containing document embeddings
            questions: List of questions to answer
            
        Returns:
            List of dictionaries with answers and metadata
        """
        results = []
        for question in questions:
            answer = await self.answer_question(vector_store, question)
            results.append(answer)
        
        return results
