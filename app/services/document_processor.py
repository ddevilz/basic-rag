"""Document processing service for extracting text and creating document chunks."""

from typing import List, Dict, Any, Optional

from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredEmailLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.utils.document_handlers.document_handler import DocumentHandler


class DocumentProcessor:
    """Service for processing documents and extracting text."""
    
    def __init__(self):
        """Initialize the document processor."""
        self.document_handler = DocumentHandler()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    async def process_document_from_url(self, url: str, doc_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Process a document from a URL.
        
        Args:
            url: URL of the document to process
            doc_type: Optional document type (pdf, docx, email)
            
        Returns:
            List of document chunks with text and metadata
        """
        # Download the document
        file_path, filename = self.document_handler.download_document(url, doc_type=doc_type)
        
        # Extract text based on document type
        extension = filename.split('.')[-1].lower() if '.' in filename else ''
        
        if extension == 'pdf':
            return await self._process_pdf(file_path, filename)
        elif extension in ['docx', 'doc']:
            return await self._process_docx(file_path, filename)
        elif extension in ['eml', 'msg']:
            return await self._process_email(file_path, filename)
        else:
            raise ValueError(f"Unsupported document type: {extension}")
    
    async def _process_pdf(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Process a PDF document.
        
        Args:
            file_path: Path to the PDF file
            filename: Name of the file
            
        Returns:
            List of document chunks with text and metadata
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Add metadata
        for doc in documents:
            doc.metadata["source"] = filename
            doc.metadata["file_path"] = file_path
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Convert to dictionaries for easier serialization
        return [
            {
                "page_content": chunk.page_content,
                "metadata": chunk.metadata
            }
            for chunk in chunks
        ]
    
    async def _process_docx(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Process a DOCX document.
        
        Args:
            file_path: Path to the DOCX file
            filename: Name of the file
            
        Returns:
            List of document chunks with text and metadata
        """
        loader = Docx2txtLoader(file_path)
        documents = loader.load()
        
        # Add metadata
        for doc in documents:
            doc.metadata["source"] = filename
            doc.metadata["file_path"] = file_path
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Convert to dictionaries for easier serialization
        return [
            {
                "page_content": chunk.page_content,
                "metadata": chunk.metadata
            }
            for chunk in chunks
        ]
    
    async def _process_email(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Process an email document.
        
        Args:
            file_path: Path to the email file
            filename: Name of the file
            
        Returns:
            List of document chunks with text and metadata
        """
        loader = UnstructuredEmailLoader(file_path)
        documents = loader.load()
        
        # Add metadata
        for doc in documents:
            doc.metadata["source"] = filename
            doc.metadata["file_path"] = file_path
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Convert to dictionaries for easier serialization
        return [
            {
                "page_content": chunk.page_content,
                "metadata": chunk.metadata
            }
            for chunk in chunks
        ]
