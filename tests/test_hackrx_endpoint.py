"""Tests for the HackRx API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStoreService
from app.services.question_answering import QuestionAnsweringService


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_document_processor():
    """Mock the DocumentProcessor service."""
    with patch.object(DocumentProcessor, "process_document_from_url") as mock:
        # Mock return value for process_document_from_url
        mock.return_value = [
            {
                "page_content": "This policy has a grace period of thirty days for premium payment.",
                "metadata": {"source": "test_document.pdf", "page": 1}
            },
            {
                "page_content": "The waiting period for pre-existing diseases is thirty-six months.",
                "metadata": {"source": "test_document.pdf", "page": 2}
            }
        ]
        yield mock


@pytest.fixture
def mock_vector_store():
    """Mock the VectorStoreService."""
    with patch.object(VectorStoreService, "create_vector_store") as mock_create:
        mock_vector_store = MagicMock()
        mock_create.return_value = mock_vector_store
        
        with patch.object(VectorStoreService, "save_vector_store") as mock_save:
            mock_save.return_value = "/tmp/test_index"
            yield mock_create, mock_vector_store, mock_save


@pytest.fixture
def mock_qa_service():
    """Mock the QuestionAnsweringService."""
    with patch.object(QuestionAnsweringService, "batch_answer_questions") as mock:
        mock.return_value = [
            {
                "question": "What is the grace period for premium payment?",
                "answer": "The grace period for premium payment is thirty days.",
                "confidence": 0.9,
                "context": ["This policy has a grace period of thirty days for premium payment."],
                "sources": ["test_document.pdf"]
            },
            {
                "question": "What is the waiting period for pre-existing diseases?",
                "answer": "The waiting period for pre-existing diseases is thirty-six months.",
                "confidence": 0.9,
                "context": ["The waiting period for pre-existing diseases is thirty-six months."],
                "sources": ["test_document.pdf"]
            }
        ]
        yield mock


def test_hackrx_run_endpoint(client, mock_document_processor, mock_vector_store, mock_qa_service):
    """Test the /hackrx/run endpoint."""
    # Set up test data
    test_request = {
        "documents": "https://example.com/test.pdf",
        "questions": [
            "What is the grace period for premium payment?",
            "What is the waiting period for pre-existing diseases?"
        ]
    }
    
    # Make the request with authentication
    response = client.post(
        "/api/v1/hackrx/run",
        json=test_request,
        headers={"Authorization": "Bearer 97d9f7fb0dd56082c8776bb5be7a4ae27a39ec2121fcb7ed89277aa49dcefda1"}
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "answers" in data
    assert isinstance(data["answers"], list)
    assert len(data["answers"]) == 2
    
    # Verify answers content
    assert "The grace period for premium payment is thirty days." in data["answers"]
    assert "The waiting period for pre-existing diseases is thirty-six months." in data["answers"]
    
    # Verify service calls
    mock_document_processor.assert_called_once()
    mock_vector_store[0].assert_called_once()  # create_vector_store
    mock_vector_store[2].assert_called_once()  # save_vector_store
    mock_qa_service.assert_called_once()


def test_hackrx_run_endpoint_unauthorized(client):
    """Test the /hackrx/run endpoint with invalid token."""
    # Set up test data
    test_request = {
        "documents": "https://example.com/test.pdf",
        "questions": ["What is the grace period?"]
    }
    
    # Make the request with invalid authentication
    response = client.post(
        "/api/v1/hackrx/run",
        json=test_request,
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    # Check response
    assert response.status_code == 401
