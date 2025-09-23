"""Pydantic schemas for message resources."""

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module,import-error


class MessageCreate(BaseModel):
    """Schema for creating a message."""

    text: str = Field(..., min_length=1, max_length=2000)


class Message(BaseModel):
    """Schema representing a message resource."""

    id: int
    text: str


