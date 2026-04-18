"""RAG API request and response schemas"""
from pydantic import BaseModel, Field
from typing import List


class RAGQueryRequest(BaseModel):
    """Request model for RAG query"""
    query: str = Field(..., min_length=1, max_length=1000, description="The question to ask")
    
    model_config = {"json_schema_extra": {"examples": [{"query": "who is the prime minister of USA?"}]}}


class RAGQueryResponse(BaseModel):
    """Response model for RAG query"""
    query: str = Field(..., description="The processed query")
    context: List[str] = Field(default_factory=list, description="List of relevant context snippets")
    answer: str = Field(..., description="The generated answer from RAG app")
    
    model_config = {"json_schema_extra": {
        "examples": [{
            "query": "\"who PRIME MINISTER OF USA?\"",
            "context": ["Q: \"who donald trump?\"\nA: Donald Trump is a businessman..."],
            "answer": "A: The United States does not have a Prime Minister; it is led by a President."
        }]
    }}


class RAGAskResponse(BaseModel):
    """Wrapper for API response"""
    data: RAGQueryResponse
    message: str = "Query answered successfully"


class RAGHistoryItem(BaseModel):
    """Single history item from RAG app"""
    id: int | str
    user_id: str
    query: str
    context: List[str] = Field(default_factory=list)
    answer: str
    timestamp: str


class RAGHistoryResponse(BaseModel):
    """RAG history response payload"""
    user_id: str
    count: int
    history: List[RAGHistoryItem] = Field(default_factory=list)


class RAGHistoryApiResponse(BaseModel):
    """Wrapper for history API response"""
    data: RAGHistoryResponse
    message: str = "History fetched successfully"
