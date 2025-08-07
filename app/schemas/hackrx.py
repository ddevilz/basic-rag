"""Schemas for the HackRx API endpoints."""

from typing import List, Dict, Any, Union

from pydantic import BaseModel, Field, HttpUrl


class HackRxRunRequest(BaseModel):
    """Schema for the HackRx run request."""
    
    documents: Union[HttpUrl, List[HttpUrl]] = Field(
        ..., 
        description="URL or list of URLs to documents to process"
    )
    questions: List[str] = Field(
        ..., 
        description="List of questions to answer based on the documents"
    )


# Internal models for processing
class QuestionAnswer(BaseModel):
    """Schema for a question and its answer with detailed information (internal use)."""
    
    question: str = Field(..., description="The question that was asked")
    answer: str = Field(..., description="The answer to the question")
    confidence: float = Field(..., description="Confidence score for the answer")
    context: List[str] = Field(..., description="Relevant context used to generate the answer")
    sources: List[str] = Field(..., description="Sources of the information used to generate the answer")


class HackRxRunDetailedResponse(BaseModel):
    """Schema for the detailed HackRx run response (internal use)."""
    
    results: List[QuestionAnswer] = Field(..., description="List of question-answer pairs")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional metadata about the processing"
    )


# External API response model matching the expected format
class HackRxRunResponse(BaseModel):
    """Schema for the HackRx run response as expected by the API consumer."""
    
    answers: List[str] = Field(..., description="List of answers to the questions")

