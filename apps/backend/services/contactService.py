"""
Contact service for Lazor Connect API.
This service handles all business logic related to contacts and manages data storage.
"""
from typing import List, Optional, Dict

from models import Contact, ContactCreate
from db import supabase


class ContactService:
    """Service for managing contacts"""
    
    @staticmethod
    def list_contacts(search: Optional[str] = None, 
                      relationship_type: Optional[str] = None,
                      relationship_strength: Optional[int] = None,
                      min_strength: Optional[int] = None) -> List[Dict]:
        """Get all contacts from the database with optional filtering"""
        query = supabase.table("contacts").select("*")
        
        if search:
            query = query.ilike("name", f"%{search}%")
            
        if relationship_type:
            query = query.eq("relationship_type", relationship_type)
            
        if relationship_strength is not None:
            query = query.eq("relationship_strength", relationship_strength)
            
        # Add min_strength filtering if provided
        if min_strength is not None:
            query = query.gte("relationship_strength", min_strength)
            
        response = query.execute()
        return response.data
    
    @staticmethod
    def get_contact(contact_id: int) -> Optional[Dict]:
        """Get a single contact by ID"""
        response = supabase.table("contacts").select("*").eq("id", contact_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_contact(contact: Dict) -> Dict:
        """Create a new contact in the database"""
        # Ensure only the name field is required
        payload = {
            "name": contact["name"],
        }
        
        # Add optional fields if present
        for field in ["nickname", "birthday", "contact_methods", 
                     "relationship_type", "relationship_strength",
                     "conversation_topics", "important_dates", "reminders",
                     "interests", "family_details", "preferences",
                     "last_connection", "avg_days_btw_contacts", 
                     "recommended_contact_freq_days"]:
            if field in contact and contact[field] is not None:
                payload[field] = contact[field]
                
        response = supabase.table("contacts").insert(payload).execute()
        return response.data[0]
    
    @staticmethod
    def update_contact(contact_id: int, contact_data: Dict) -> Optional[Dict]:
        """Update a contact in the database"""
        response = supabase.table("contacts").update(contact_data).eq("id", contact_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_contact(contact_id: int) -> bool:
        """Delete a contact from the database"""
        response = supabase.table("contacts").delete().eq("id", contact_id).execute()
        return bool(response.data)
    
    @staticmethod
    def get_due_for_contact(days_threshold: int = 7) -> List[Dict]:
        """
        Get contacts that are due for reaching out based on recommended contact frequency
        
        Returns contacts where:
        1. Current date - last_connection > recommended_contact_freq_days
        2. If recommended_contact_freq_days is not set, uses days_threshold parameter
        """
        from datetime import datetime, timedelta
        
        # Get all contacts
        all_contacts = ContactService.list_contacts()
        
        # Filter contacts that are due for contact
        due_contacts = []
        current_date = datetime.now()
        
        for contact in all_contacts:
            # Skip if no last_connection date
            if not contact.get("last_connection"):
                continue
                
            last_connection = datetime.fromisoformat(contact["last_connection"].replace("Z", "+00:00"))
            recommended_freq = contact.get("recommended_contact_freq_days", days_threshold)
            
            days_since_contact = (current_date - last_connection).days
            if days_since_contact >= recommended_freq:
                due_contacts.append(contact)
                
        return due_contacts
    
    @staticmethod
    def search_contacts(query: str, limit: int = 10) -> List[Dict]:
        """
        Search for contacts with a specific query string
        
        The search is performed across text fields including:
        - Name
        - Nickname
        - Contact methods
        - Conversation topics
        - Interests
        """
        # Use the list_contacts method with search parameter
        contacts = ContactService.list_contacts(search=query)
        
        # Limit the results
        return contacts[:limit]
