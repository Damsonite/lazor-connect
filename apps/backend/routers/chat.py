"""
Chat router for Lazor Connect API.
The focus is on helping users build rich contact profiles rather than
maintaining conversational history.
"""
from fastapi import APIRouter, HTTPException, Path
from typing import Dict, Any

from models import ChatRequest
from services.chatService import ChatService
from services.contactService import ContactService

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Contact not found"}},
)

contact_service = ContactService()
chat_service = ChatService(contact_service)

@router.post("/{contact_id}/send", response_model=Dict[str, Any])
async def send_message(
    contact_id: str = Path(..., title="The ID of the contact to chat with"), 
    request: ChatRequest = None
):
    """
    Send a message to get contact profile recommendations.
    Helps build better contact profiles through AI suggestions about:
    - Conversation topics based on interests
    - Interaction recommendations
    - Profile improvement suggestions
    """
    try:
        response = await chat_service.handle_message(contact_id, request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@router.get("/{contact_id}/greeting", response_model=Dict[str, Any])
async def get_greeting(
    contact_id: str = Path(..., title="The ID of the contact to get initial greeting for")
):
    """
    Get an initial greeting with contact profile recommendations.
    The greeting will include suggestions based on profile completeness
    and existing information about the contact.
    """
    try:
        greeting = await chat_service.get_initial_greeting(contact_id)
        return greeting
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting greeting: {str(e)}")
