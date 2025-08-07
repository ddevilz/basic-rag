"""Document schemas for the API."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl, Field


class DocumentType(str, Enum):
    """Enum for document types."""
    
    PDF = "pdf"
    DOCX = "docx"
    EMAIL = "email"


class DocumentUrlRequest(BaseModel):
    """Schema for document URL download request."""
    
    url: HttpUrl = Field(..., description="URL of the document to download")
    filename: Optional[str] = Field(None, description="Optional filename to use for the downloaded document")
    doc_type: Optional[DocumentType] = Field(None, description="Optional document type (pdf, docx, email)")


class DocumentDownloadResponse(BaseModel):
    """Schema for document download response."""
    
    file_path: str = Field(..., description="Local path where the document was saved")
    filename: str = Field(..., description="Filename of the downloaded document")
    doc_type: str = Field(..., description="Type of the document")
    success: bool = Field(..., description="Whether the download was successful")
    message: str = Field(..., description="Status message")


# Keep old schemas for backward compatibility
PDFUrlRequest = DocumentUrlRequest
PDFDownloadResponse = DocumentDownloadResponse
