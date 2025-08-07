"""Utility for handling various document types (PDF, DOCX, email)."""

import os
import uuid
from typing import Optional, Tuple

import requests
from fastapi import HTTPException


class DocumentHandler:
    """Class for handling document downloads and processing."""

    def __init__(self, storage_dir: str = "storage/documents"):
        """Initialize the document handler.
        
        Args:
            storage_dir: Directory to store downloaded documents
        """
        self.storage_dir = storage_dir
        self._ensure_storage_dir_exists()
    
    def _ensure_storage_dir_exists(self) -> None:
        """Ensure the storage directory exists."""
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def download_document(self, url: str, filename: Optional[str] = None, 
                         doc_type: Optional[str] = None) -> Tuple[str, str]:
        """Download a document from a URL and save it locally.
        
        Args:
            url: URL of the document to download
            filename: Optional filename to use for the downloaded document
            doc_type: Optional document type (pdf, docx, email)
            
        Returns:
            Tuple containing the local file path and the filename
            
        Raises:
            HTTPException: If the download fails or the content type is not supported
        """
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Determine document type from content-type or URL if not specified
            content_type = response.headers.get('Content-Type', '')
            if not doc_type:
                if 'application/pdf' in content_type or url.lower().endswith('.pdf'):
                    doc_type = 'pdf'
                elif 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type or url.lower().endswith('.docx'):
                    doc_type = 'docx'
                elif 'message/rfc822' in content_type or url.lower().endswith('.eml'):
                    doc_type = 'email'
                else:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Unsupported document type. Content-Type: {content_type}"
                    )
            
            # Generate a filename if not provided
            if not filename:
                filename = f"{uuid.uuid4()}.{doc_type}"
            elif not filename.lower().endswith(f'.{doc_type}'):
                filename = f"{filename}.{doc_type}"
            
            file_path = os.path.join(self.storage_dir, filename)
            
            # Save the document file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return file_path, filename
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to download document: {str(e)}"
            )
    
    def extract_text(self, file_path: str) -> str:
        """Extract text content from a document.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content
            
        Raises:
            HTTPException: If text extraction fails
        """
        try:
            # Determine document type from file extension
            if file_path.lower().endswith('.pdf'):
                return self._extract_text_from_pdf(file_path)
            elif file_path.lower().endswith('.docx'):
                return self._extract_text_from_docx(file_path)
            elif file_path.lower().endswith('.eml'):
                return self._extract_text_from_email(file_path)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file format for text extraction: {file_path}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract text: {str(e)}"
            )
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        # This is a placeholder - we'll implement the actual extraction later
        # using PyPDF or a similar library
        return f"PDF text extraction not yet implemented for {file_path}"
    
    def _extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from a DOCX file.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            Extracted text content
        """
        # This is a placeholder - we'll implement the actual extraction later
        # using python-docx
        return f"DOCX text extraction not yet implemented for {file_path}"
    
    def _extract_text_from_email(self, file_path: str) -> str:
        """Extract text from an email file.
        
        Args:
            file_path: Path to the email file
            
        Returns:
            Extracted text content
        """
        # This is a placeholder - we'll implement the actual extraction later
        # using email or mailparser libraries
        return f"Email text extraction not yet implemented for {file_path}"
