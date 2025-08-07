"""HackRx API endpoints."""

import uuid

from fastapi import APIRouter, HTTPException, status

from app.schemas.hackrx import HackRxRunRequest, HackRxRunResponse, HackRxRunDetailedResponse
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStoreService
from app.services.question_answering import QuestionAnsweringService

router = APIRouter(prefix="/hackrx", tags=["HackRx"])


@router.post("/run", response_model=HackRxRunResponse)
async def process_document_and_answer_questions(request: HackRxRunRequest):
    """Process a document and answer questions based on its content.
    
    Args:
        request: HackRxRunRequest containing document URL(s) and questions
        
    Returns:
        HackRxRunResponse with answers to the questions
    """
    try:
        # Initialize services
        document_processor = DocumentProcessor()
        vector_store_service = VectorStoreService()
        qa_service = QuestionAnsweringService()
        
        # Process document(s)
        documents = []
        
        # Handle both single URL and list of URLs
        urls = [request.documents] if not isinstance(request.documents, list) else request.documents
        
        for url in urls:
            # Process each document - convert HttpUrl to string if needed
            url_str = str(url) if hasattr(url, '__str__') else url
            doc_chunks = await document_processor.process_document_from_url(url_str)
            documents.extend(doc_chunks)
        
        # Create vector store
        vector_store = await vector_store_service.create_vector_store(documents)
        
        # Generate unique index name and save vector store
        index_name = f"hackrx_{uuid.uuid4().hex}"
        await vector_store_service.save_vector_store(vector_store, index_name)
        
        # Answer questions
        detailed_answers = await qa_service.batch_answer_questions(vector_store, request.questions)
        
        # Create detailed response (for internal use/logging)
        # We could log this or store it in a database for analytics
        _ = HackRxRunDetailedResponse(
            results=detailed_answers,
            metadata={
                "document_count": len(urls),
                "chunk_count": len(documents),
                "index_name": index_name
            }
        )
        
        # Create simplified response for API consumer
        simple_response = HackRxRunResponse(
            answers=[answer["answer"] for answer in detailed_answers]
        )
        
        return simple_response
    
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document and answer questions: {str(e)}"
        )
