"""
Document models and schemas for the application.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    """Schema for creating a new document."""

    file_name: str
    file_content: bytes


class DocumentResponse(BaseModel):
    """Schema for document response."""

    id: str
    file_name: str
    parsed_text_preview: str  # First 200 chars
    embedding_size: int
    created_at: datetime

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class DocumentInDB(BaseModel):
    """Complete document schema as stored in MongoDB."""

    file_name: str
    file_content: bytes  # Original file as binary
    parsed_text: str  # Extracted text content
    embedding: List[float]  # Embedding vector
    embedding_size: int  # Dimension of embedding
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB insertion."""
        return {
            "file_name": self.file_name,
            "file_content": self.file_content,
            "parsed_text": self.parsed_text,
            "embedding": self.embedding,
            "embedding_size": self.embedding_size,
            "created_at": self.created_at,
        }
