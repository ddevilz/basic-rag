"""Document API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.document import DocumentUrlRequest, DocumentDownloadResponse, DocumentType
from app.utils.document_handlers.document_handler import DocumentHandler

router = APIRouter(prefix="/document", tags=["Document"])


@router.post("/download", response_model=DocumentDownloadResponse)
async def download_document_from_url(request: DocumentUrlRequest):
    """Download a document from a URL and save it locally.
    
    Args:
        request: DocumentUrlRequest containing the URL, optional filename, and document type
        
    Returns:
        DocumentDownloadResponse with download status and file information
    """
    try:
        handler = DocumentHandler()
        file_path, filename = handler.download_document(
            url=str(request.url), 
            filename=request.filename,
            doc_type=request.doc_type.value if request.doc_type else None
        )
        
        # Determine document type from filename extension
        doc_type = filename.split('.')[-1] if '.' in filename else 'unknown'
        
        return DocumentDownloadResponse(
            file_path=file_path,
            filename=filename,
            doc_type=doc_type,
            success=True,
            message=f"{doc_type.upper()} document downloaded successfully"
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download document: {str(e)}"
        )


# Keep the old endpoint for backward compatibility
@router.post("/download-pdf", response_model=DocumentDownloadResponse)
async def download_pdf_from_url(request: DocumentUrlRequest):
    """Download a PDF from a URL and save it locally (legacy endpoint).
    
    Args:
        request: DocumentUrlRequest containing the URL and optional filename
        
    Returns:
        DocumentDownloadResponse with download status and file information
    """
    # Force PDF type
    request_with_type = DocumentUrlRequest(
        url=request.url,
        filename=request.filename,
        doc_type=DocumentType.PDF
    )
    return await download_document_from_url(request_with_type)
