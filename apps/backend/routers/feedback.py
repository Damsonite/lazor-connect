"""
Feedback router for Lazor Connect API (in-memory mock).
"""
from fastapi import APIRouter, Body, Depends
from typing import List, Dict
from datetime import datetime
from services.chatService import ChatService
from services.contactService import ContactService

router = APIRouter(
    prefix="/feedback",
    tags=["feedback"]
)

# In-memory feedback store (resets on server restart)
feedback_store: List[Dict] = []

chat_service = ChatService(ContactService())

@router.post("")
def submit_feedback(
    feedback: Dict = Body(..., example={"type": "like", "message": "Great suggestion!", "contact_id": "123"})
):
    """Submit feedback (like/dislike, message, etc.)"""
    feedback_entry = {
        **feedback,
        "timestamp": datetime.now().isoformat()
    }
    feedback_store.append(feedback_entry)
    return {"status": "ok", "received": feedback_entry}

@router.get("")
def get_feedback():
    """Get all feedback (for testing/demo)"""
    return feedback_store

@router.get("/summary")
def feedback_summary():
    return chat_service.get_feedback_summary()
