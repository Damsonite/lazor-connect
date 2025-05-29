"""
Mock Contact service for Lazor Connect API.
This service provides mock data when the database is unavailable.
"""
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import uuid


class MockContactService:
    """Mock service for managing contacts when database is unavailable"""
    
    # Mock data
    MOCK_CONTACTS = [
        {
            "id": str(uuid.uuid4()),
            "name": "Alice Johnson",
            "nickname": "Ally",
            "relationship_type": "friend",
            "relationship_strength": 4,
            "interests": ["hiking", "photography", "reading"],
            "last_connection": (datetime.now() - timedelta(days=3)).isoformat(),
            "current_streak": 5,
            "longest_streak": 12,
            "recommended_contact_freq_days": 7,
            "conversation_topics": ["travel", "books", "nature photography"],
            "personality": "Outgoing and adventurous, loves exploring new places",
            "family_details": "Has two younger siblings, close to her parents",
            "preferences": {
                "likes": ["coffee", "mountains", "indie music"],
                "dislikes": ["crowded places", "spicy food"]
            },
            "created_at": (datetime.now() - timedelta(days=30)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=3)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Bob Wilson",
            "nickname": "Bobby",
            "relationship_type": "colleague",
            "relationship_strength": 3,
            "interests": ["coding", "gaming", "cooking"],
            "last_connection": (datetime.now() - timedelta(days=7)).isoformat(),
            "current_streak": 1,
            "longest_streak": 8,
            "recommended_contact_freq_days": 14,
            "conversation_topics": ["technology", "video games", "recipes"],
            "personality": "Quiet but friendly, very detail-oriented",
            "family_details": "Married with one daughter",
            "preferences": {
                "likes": ["Italian food", "strategy games", "clean code"],
                "dislikes": ["meetings", "loud environments"]
            },
            "created_at": (datetime.now() - timedelta(days=45)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=7)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Carmen Rodriguez",
            "relationship_type": "family",
            "relationship_strength": 5,
            "interests": ["gardening", "cooking", "family time"],
            "last_connection": (datetime.now() - timedelta(days=1)).isoformat(),
            "current_streak": 15,
            "longest_streak": 25,
            "recommended_contact_freq_days": 3,
            "conversation_topics": ["family updates", "recipes", "garden tips"],
            "personality": "Warm and caring, always puts family first",
            "family_details": "Mother of three, grandmother of two",
            "preferences": {
                "likes": ["homemade meals", "flowers", "family gatherings"],
                "dislikes": ["processed food", "loud music"]
            },
            "created_at": (datetime.now() - timedelta(days=365)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=1)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "David Chen",
            "nickname": "Dave",
            "relationship_type": "friend",
            "relationship_strength": 4,
            "interests": ["music", "travel", "food"],
            "last_connection": (datetime.now() - timedelta(days=14)).isoformat(),
            "current_streak": 0,
            "longest_streak": 6,
            "recommended_contact_freq_days": 10,
            "conversation_topics": ["concerts", "restaurants", "travel stories"],
            "personality": "Enthusiastic and social, loves trying new experiences",
            "family_details": "Single, has a brother living abroad",
            "preferences": {
                "likes": ["live music", "Asian cuisine", "weekend trips"],
                "dislikes": ["staying indoors", "boring conversations"]
            },
            "created_at": (datetime.now() - timedelta(days=60)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=14)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Elena Petrov",
            "nickname": "Lena",
            "relationship_type": "colleague",
            "relationship_strength": 3,
            "interests": ["art", "history", "wine"],
            "last_connection": (datetime.now() - timedelta(days=5)).isoformat(),
            "current_streak": 2,
            "longest_streak": 7,
            "recommended_contact_freq_days": 12,
            "conversation_topics": ["art exhibitions", "historical documentaries", "wine tasting"],
            "personality": "Intellectual and cultured, appreciates fine things",
            "family_details": "Lives with partner, no children yet",
            "preferences": {
                "likes": ["museums", "red wine", "classical music"],
                "dislikes": ["fast food", "loud parties", "small talk"]
            },
            "created_at": (datetime.now() - timedelta(days=90)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=5)).isoformat()
        }
    ]
    
    def __init__(self):
        # Create a copy to allow modifications during runtime
        self._contacts_store = [contact.copy() for contact in self.MOCK_CONTACTS]
    
    def list_contacts(self, search: Optional[str] = None, 
                     relationship_type: Optional[str] = None,
                     relationship_strength: Optional[int] = None,
                     min_strength: Optional[int] = None) -> List[Dict]:
        """Get all mock contacts with optional filtering"""
        contacts = self._contacts_store.copy()
        
        if search:
            contacts = [c for c in contacts if search.lower() in c["name"].lower()]
            
        if relationship_type:
            contacts = [c for c in contacts if c.get("relationship_type") == relationship_type]
            
        if relationship_strength is not None:
            contacts = [c for c in contacts if c.get("relationship_strength") == relationship_strength]
            
        if min_strength is not None:
            contacts = [c for c in contacts if c.get("relationship_strength", 0) >= min_strength]
            
        return contacts
    
    def get_contact(self, contact_id: str) -> Optional[Dict]:
        """Get a single mock contact by ID"""
        for contact in self._contacts_store:
            if contact["id"] == contact_id:
                return contact.copy()
        return None
    
    def create_contact(self, contact: Dict) -> Dict:
        """Create a new mock contact"""
        new_contact = {
            "id": str(uuid.uuid4()),
            "name": contact["name"],
            "current_streak": 0,
            "longest_streak": 0,
            "last_connection": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Add optional fields if present
        for field in ["nickname", "birthday", "contact_methods", 
                     "relationship_type", "relationship_strength",
                     "conversation_topics", "important_dates", "reminders",
                     "interests", "family_details", "preferences", "personality",
                     "avg_days_btw_contacts", "recommended_contact_freq_days"]:
            if field in contact and contact[field] is not None:
                new_contact[field] = contact[field]
        
        self._contacts_store.append(new_contact)
        return new_contact.copy()
    
    def update_contact(self, contact_id: str, contact_data: Dict) -> Optional[Dict]:
        """Update a mock contact"""
        for i, contact in enumerate(self._contacts_store):
            if contact["id"] == contact_id:
                # Remove fields that shouldn't be updated
                clean_data = {k: v for k, v in contact_data.items() 
                             if k not in ['id', 'created_at']}
                clean_data["updated_at"] = datetime.now().isoformat()
                
                # Update the contact
                self._contacts_store[i].update(clean_data)
                return self._contacts_store[i].copy()
        return None
    
    def delete_contact(self, contact_id: str) -> bool:
        """Delete a mock contact"""
        for i, contact in enumerate(self._contacts_store):
            if contact["id"] == contact_id:
                del self._contacts_store[i]
                return True
        return False
    
    def reset_mock_data(self):
        """Reset to original mock data"""
        self._contacts_store = [contact.copy() for contact in self.MOCK_CONTACTS]


# Global instance
mock_contact_service = MockContactService()
