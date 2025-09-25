"""Pydantic schemas for message resources."""

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module,import-error


class MessageCreate(BaseModel):
    """Schema for creating a message."""

    text: str = Field(..., min_length=1, max_length=2000)


class Message(BaseModel):
    """Schema representing a message resource."""

    id: int
    text: str


class TextGenerationRequest(BaseModel):
    """Schema for text generation requests."""

    prompt: str = Field(..., min_length=1, max_length=1000)
    max_length: int = Field(default=50, ge=1, le=200)
    temperature: float = Field(default=0.7, ge=0.1, le=2.0)


class TextGenerationResponse(BaseModel):
    """Schema for text generation responses."""

    generated_text: str
    prompt: str


