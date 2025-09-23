"""API v1 endpoints for health and message operations."""

from typing import List

from fastapi import APIRouter

from app.schemas.message import Message, MessageCreate


router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


_MESSAGES: List[Message] = []


@router.get("/messages", response_model=List[Message])
async def list_messages() -> List[Message]:
    """Return all messages in memory."""
    return _MESSAGES


@router.post("/messages", response_model=Message, status_code=201)
async def create_message(payload: MessageCreate) -> Message:
    """Create a new message and store it in memory."""
    message = Message(id=len(_MESSAGES) + 1, text=payload.text)
    _MESSAGES.append(message)
    return message


