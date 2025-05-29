"""
Contact router for Lazor Connect API.
"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional, Dict

from models import ContactCreate, ContactUpdate
from services.contactService import ContactService
from services.streakService import StreakService
from services.mockContactService import mock_contact_service

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


# Mock endpoints for when database is unavailable (must be defined before parameterized routes)
@router.get("/mock", response_model=List[dict])
def list_mock_contacts(
    search: Optional[str] = None,
    relationship_type: Optional[str] = None,
    relationship_strength: Optional[int] = Query(None, ge=1, le=5),
    min_strength: Optional[int] = Query(None, ge=1, le=5)
):
    """
    List mock contacts (fallback when database is unavailable)
    
    - **search**: Search string to filter contacts (searches in name field)
    - **relationship_type**: Filter by relationship type (friend, family, colleague, etc.)
    - **relationship_strength**: Filter by exact relationship strength (1-5 scale)
    - **min_strength**: Filter for contacts with at least this relationship strength
    """
    return mock_contact_service.list_contacts(
        search=search,
        relationship_type=relationship_type,
        relationship_strength=relationship_strength,
        min_strength=min_strength
    )


@router.post("/mock", response_model=dict)
def create_mock_contact(contact: ContactCreate):
    """Create a new mock contact (fallback when database is unavailable)"""
    return mock_contact_service.create_contact(contact.model_dump(mode="json"))


@router.post("/mock/reset")
def reset_mock_data():
    """Reset mock data to original state"""
    mock_contact_service.reset_mock_data()
    return {"message": "Mock data reset successfully"}


@router.get("/mock/{contact_id}", response_model=dict)
def get_mock_contact(contact_id: str):
    """Get a mock contact by ID (fallback when database is unavailable)"""
    contact = mock_contact_service.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Mock contact not found")
    return contact


@router.put("/mock/{contact_id}", response_model=dict)
def update_mock_contact(contact_id: str, contact: ContactUpdate):
    """Update a mock contact (fallback when database is unavailable)"""
    updated_contact = mock_contact_service.update_contact(
        contact_id, 
        contact.model_dump(mode="json", exclude_unset=True)
    )
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Mock contact not found")
    return updated_contact


@router.delete("/mock/{contact_id}")
def delete_mock_contact(contact_id: str):
    """Delete a mock contact (fallback when database is unavailable)"""
    if not mock_contact_service.delete_contact(contact_id):
        raise HTTPException(status_code=404, detail="Mock contact not found")
    return {"message": "Mock contact deleted successfully"}


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

@router.post("/{contact_id}/contacted", response_model=dict)
def mark_as_contacted(
    contact_id: str = Path(..., title="The ID of the contact"),
    interaction_details: Optional[str] = Query(None, description="Optional details about the interaction")
):
    """
    Mark that the user contacted this person today.
    This updates the streak and last_connection without going through chat.
    """
    updated_contact = StreakService.update_streak_on_contact(contact_id)
    
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    # If interaction details provided, try to extract useful information
    if interaction_details:
        try:
            from services.geminiClient import GeminiClient
            client = GeminiClient()
            if client.is_available():
                # Extract information from the interaction details
                import asyncio
                loop = asyncio.get_event_loop()
                extracted_data = loop.run_until_complete(client.extract_profile_data(interaction_details))
                
                if extracted_data:
                    from utils.json import normalize_extracted_data
                    extracted_data = normalize_extracted_data(extracted_data)
                    # Update contact with extracted information
                    ContactService.update_contact(contact_id, extracted_data)
        except Exception as e:
            print(f"Error extracting data from interaction details: {e}")
    
    return {
        "message": "Contact marked as contacted today",
        "current_streak": updated_contact.get("current_streak", 0),
        "longest_streak": updated_contact.get("longest_streak", 0),
        "last_connection": updated_contact.get("last_connection")
    }

@router.get("/recommendations/due", response_model=List[dict])
def get_contact_recommendations():
    """
    Get AI-powered recommendations for contacts that need attention.
    Returns contacts sorted by priority (most urgent first) with personalized suggestions.
    """
    from datetime import datetime, timezone
    
    # Get all contacts that are due
    due_contacts = ContactService.get_due_for_contact(days_threshold=1)
    
    # Enhance with status information and sort by urgency
    recommendations = []
    
    for contact in due_contacts:
        try:
            # Calculate status for each contact
            current_date = datetime.now(timezone.utc)
            last_connection = contact.get("last_connection")
            recommended_freq = contact.get("recommended_contact_freq_days", 7)
            
            if last_connection:
                last_conn_date = datetime.fromisoformat(last_connection.replace("Z", "+00:00"))
                days_since = (current_date - last_conn_date).days
            else:
                days_since = 999
            
            # Determine urgency
            if days_since >= recommended_freq * 2:
                urgency = "high"
                priority_score = days_since + 100
            elif days_since >= recommended_freq:
                urgency = "medium" 
                priority_score = days_since + 50
            else:
                urgency = "low"
                priority_score = days_since
            
            # Generate personalized suggestion
            suggestion = _generate_contact_suggestion(contact, days_since)
            
            recommendations.append({
                **contact,
                "days_since_contact": days_since,
                "urgency_level": urgency,
                "priority_score": priority_score,
                "suggestion": suggestion,
                "conversation_starters": _get_conversation_starters(contact)
            })
            
        except Exception as e:
            print(f"Error processing contact {contact.get('id')}: {e}")
            continue
    
    # Sort by priority (highest score first)
    recommendations.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
    
    return recommendations[:10]  # Return top 10 recommendations

def _generate_contact_suggestion(contact: Dict, days_since: int) -> str:
    """Generate a personalized suggestion for contacting someone."""
    name = contact.get('name', 'esta persona')
    
    if days_since >= 30:
        return f"¡Hace mucho que no hablas con {name}! Es hora de reconectarse."
    elif days_since >= 14:
        return f"Han pasado {days_since} días. {name} probablemente aprecie saber de ti."
    elif days_since >= 7:
        return f"Buen momento para contactar a {name}. ¡Mantén esa conexión!"
    else:
        return f"¿Ya hablaste con {name} hoy? ¡Sigue con esa racha!"

def _get_conversation_starters(contact: Dict) -> List[str]:
    """Generate conversation starters based on contact information."""
    starters = []
    name = contact.get('name', 'esta persona')
    
    # Based on interests
    if contact.get('interests'):
        interest = contact['interests'][0]  # Take first interest
        starters.append(f"¿Cómo va tu {interest}? ¡Me gustaría saber qué has estado haciendo!")
    
    # Based on relationship type
    rel_type = contact.get('relationship_type', '').lower()
    if rel_type == 'family':
        starters.append("¿Cómo está la familia? ¡Tengo ganas de saber de ustedes!")
    elif rel_type == 'friend':
        starters.append("¡Hola! ¿Qué tal todo? Tenía ganas de charlar contigo.")
    elif rel_type == 'colleague':
        starters.append("¿Cómo van las cosas en el trabajo? ¡Espero que todo esté bien!")
    
    # Generic starters
    if not starters:
        starters.extend([
            f"¡Hola {name}! ¿Cómo estás? Tenía ganas de saber de ti.",
            f"¿Qué tal todo, {name}? ¡Espero que tengas un buen día!",
            f"¡Hola! ¿Cómo han estado las cosas? Me acordé de ti y quería saludar."
        ])
    
    return starters[:3]  # Return max 3 starters
