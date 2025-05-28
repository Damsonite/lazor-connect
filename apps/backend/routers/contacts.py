"""
Contact router for Lazor Connect API.
"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional

from models import ContactCreate, ContactUpdate
from services.contactService import ContactService
from services.streakService import StreakService

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    responses={404: {"description": "Contact not found"}},
)


@router.post("", response_model=dict)
def create_contact(contact: ContactCreate):
    """Create a new contact"""
    return ContactService.create_contact(contact.model_dump(mode="json"))


@router.get("", response_model=List[dict])
def list_contacts(
    search: Optional[str] = None,
    relationship_type: Optional[str] = None,
    relationship_strength: Optional[int] = Query(None, ge=1, le=5),
    min_strength: Optional[int] = Query(None, ge=1, le=5)
):
    """
    List all contacts with optional filtering
    
    - **search**: Search string to filter contacts (searches in name field)
    - **relationship_type**: Filter by relationship type (friend, family, colleague, etc.)
    - **relationship_strength**: Filter by exact relationship strength (1-5 scale)
    - **min_strength**: Filter for contacts with at least this relationship strength
    """
    return ContactService.list_contacts(
        search=search,
        relationship_type=relationship_type,
        relationship_strength=relationship_strength,
        min_strength=min_strength
    )


@router.get("/search/{query}", response_model=List[dict])
def search_contacts(
    query: str = Path(..., title="The search query"),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Search for contacts with a specific query string
    
    The search is performed across text fields including:
    - Name
    - Nickname
    - Contact methods 
    - Conversation topics
    - Interests
    - Family details
    """
    return ContactService.search_contacts(query=query, limit=limit)


@router.get("/due-for-contact", response_model=List[dict])
def get_due_for_contact(
    days_threshold: int = Query(7, description="Number of days since last contact to consider due")
):
    """
    Get contacts that are due for reaching out based on recommended contact frequency
    
    Returns contacts where:
    1. Current date - last_connection > recommended_contact_freq_days
    2. If recommended_contact_freq_days is not set, uses days_threshold parameter
    """
    return ContactService.get_due_for_contact(days_threshold=days_threshold)


@router.get("/by-relationship/{relationship_type}", response_model=List[dict])
def get_by_relationship(
    relationship_type: str = Path(..., description="Type of relationship to filter by"),
    min_strength: Optional[int] = Query(None, ge=1, le=5, description="Minimum relationship strength")
):
    """
    Get contacts filtered by relationship type and optional minimum strength
    
    - **relationship_type**: Type of relationship (friend, family, colleague, etc.)
    - **min_strength**: Optional minimum relationship strength (1-5)
    """
    return ContactService.list_contacts(
        relationship_type=relationship_type,
        min_strength=min_strength
    )


@router.get("/{contact_id}", response_model=dict)
def get_contact(contact_id: str = Path(..., title="The ID of the contact to get")):
    """Get a specific contact by ID (UUID string)"""
    contact = ContactService.get_contact(contact_id)
    
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return contact


@router.put("/{contact_id}", response_model=dict)
def update_contact(
    contact: ContactUpdate,
    contact_id: str = Path(..., title="The ID of the contact to update")
):
    """Update an existing contact"""
    # Update fields, excluding None values
    update_data = contact.model_dump(exclude_unset=True)
    
    # Update the contact
    updated_contact = ContactService.update_contact(contact_id, update_data)
    
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return updated_contact


@router.delete("/{contact_id}", response_model=dict)
def delete_contact(contact_id: str = Path(..., title="The ID of the contact to delete")):
    """Delete a contact"""
    success = ContactService.delete_contact(contact_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return {"message": "Contact successfully deleted"}

@router.post("/{contact_id}/contact", response_model=dict)
def record_contact_interaction(contact_id: str = Path(..., title="The ID of the contact")):
    """
    Record a new contact interaction and update streak.
    This should be called when the user has a meaningful interaction with the contact.
    """
    updated_contact = StreakService.update_streak_on_contact(contact_id)
    
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return {
        "message": "Contact interaction recorded",
        "current_streak": updated_contact.get("current_streak", 0),
        "longest_streak": updated_contact.get("longest_streak", 0)
    }


@router.get("/streaks/stats", response_model=dict)
def get_streak_statistics():
    """
    Get overall streak statistics across all contacts.
    """
    return StreakService.get_streak_stats()


@router.get("/{contact_id}/streak", response_model=dict)
def get_contact_streak(contact_id: str = Path(..., title="The ID of the contact")):
    """
    Get streak information for a specific contact.
    """
    contact = ContactService.get_contact(contact_id)
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    current_streak, longest_streak = StreakService.calculate_streak(contact)
    
    return {
        "contact_id": contact_id,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "last_connection": contact.get("last_connection"),
        "recommended_frequency": contact.get("recommended_contact_freq_days", 7)
    }
