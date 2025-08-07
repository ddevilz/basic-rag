"""Utility for downloading PDF files from URLs."""

import os
import uuid
from typing import Optional, Tuple

import requests
from fastapi import HTTPException


class PDFDownloader:
    """Class for handling PDF downloads from URLs."""

    def __init__(self, storage_dir: str = "storage/documents"):
        """Initialize the PDF downloader.
        
        Args:
            storage_dir: Directory to store downloaded PDFs
        """
        self.storage_dir = storage_dir
        self._ensure_storage_dir_exists()
    
    def _ensure_storage_dir_exists(self) -> None:
        """Ensure the storage directory exists."""
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def download_pdf(self, url: str, filename: Optional[str] = None) -> Tuple[str, str]:
        """Download a PDF from a URL and save it locally.
        
        Args:
            url: URL of the PDF to download
            filename: Optional filename to use for the downloaded PDF
            
        Returns:
            Tuple containing the local file path and the filename
            
        Raises:
            HTTPException: If the download fails or the content is not a PDF
        """
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Check if the content is a PDF
            content_type = response.headers.get('Content-Type', '')
            if 'application/pdf' not in content_type and not url.lower().endswith('.pdf'):
                raise HTTPException(
                    status_code=400, 
                    detail=f"URL does not point to a PDF file. Content-Type: {content_type}"
                )
            
            # Generate a filename if not provided
            if not filename:
                filename = f"{uuid.uuid4()}.pdf"
            elif not filename.lower().endswith('.pdf'):
                filename = f"{filename}.pdf"
            
            file_path = os.path.join(self.storage_dir, filename)
            
            # Save the PDF file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return file_path, filename
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to download PDF: {str(e)}"
            )