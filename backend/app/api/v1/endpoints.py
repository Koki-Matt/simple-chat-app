"""API v1 endpoints for health and message operations."""

from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.message import (
    Message,
    MessageCreate,
    TextGenerationRequest,
    TextGenerationResponse,
)


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


# Global pipeline instance (lazy loaded)
_pipeline = None


def get_text_generation_pipeline():
    """Get or create the text generation pipeline."""
    global _pipeline  # pylint: disable=global-statement
    if _pipeline is None:
        try:
            from transformers import pipeline  # pylint: disable=import-error
            _pipeline = pipeline("text-generation", model="gpt2")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load text generation model: {str(e)}"
            ) from e
    return _pipeline


@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text(request: TextGenerationRequest) -> TextGenerationResponse:
    """Generate text using transformers pipeline."""
    try:
        pipeline_instance = get_text_generation_pipeline()
        
        # Generate text
        result = pipeline_instance(
            request.prompt,
            max_length=request.max_length,
            temperature=request.temperature,
            do_sample=True,
            pad_token_id=pipeline_instance.tokenizer.eos_token_id,
        )
        
        # Extract generated text (remove the original prompt)
        generated_text = result[0]["generated_text"]
        if generated_text.startswith(request.prompt):
            generated_text = generated_text[len(request.prompt):].strip()
        
        return TextGenerationResponse(
            generated_text=generated_text,
            prompt=request.prompt
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Text generation failed: {str(e)}"
        ) from e


