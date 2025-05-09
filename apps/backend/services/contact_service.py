"""
Contact service for Lazor Connect API.
This service handles all business logic related to contacts and manages data storage.
"""
import os
from typing import List, Optional, Dict

from models import Contact, ContactList

# Import the Supabase client if available
try:
    from db import supabase
    USE_SUPABASE = bool(os.getenv("USE_SUPABASE", ""))
except (ImportError, AttributeError):
    USE_SUPABASE = False

# In-memory database for development
contacts_db = {}


class ContactService:
    """Service for managing contacts"""
    
    @staticmethod
    def get_all_contacts() -> List[Dict]:
        """Get all contacts from the database"""
        if USE_SUPABASE:
            # Using Supabase for production
            response = supabase.table("contacts").select("*").execute()
            return response.data
        
        # Using in-memory database for development
        return list(contacts_db.values())
    
    @staticmethod
    def get_contact(contact_id: str) -> Optional[Dict]:
        """Get a single contact by ID"""
        if USE_SUPABASE:
            # Using Supabase for production
            response = supabase.table("contacts").select("*").eq("id", contact_id).execute()
            return response.data[0] if response.data else None
        
        # Using in-memory database for development
        return contacts_db.get(contact_id)
    
    @staticmethod
    def create_contact(contact: Dict) -> Dict:
        """Create a new contact in the database"""
        if USE_SUPABASE:
            # Using Supabase for production
            response = supabase.table("contacts").insert(contact).execute()
            return response.data[0]
        
        # Using in-memory database for development
        contact_id = str(contact.get("id"))
        contacts_db[contact_id] = contact
        return contact
    
    @staticmethod
    def update_contact(contact_id: str, contact_data: Dict) -> Optional[Dict]:
        """Update a contact in the database"""
        if USE_SUPABASE:
            # Using Supabase for production
            response = supabase.table("contacts").update(contact_data).eq("id", contact_id).execute()
            return response.data[0] if response.data else None
        
        # Using in-memory database for development
        if contact_id not in contacts_db:
            return None
        
        contacts_db[contact_id].update(contact_data)
        return contacts_db[contact_id]
    
    @staticmethod
    def delete_contact(contact_id: str) -> bool:
        """Delete a contact from the database"""
        if USE_SUPABASE:
            # Using Supabase for production
            response = supabase.table("contacts").delete().eq("id", contact_id).execute()
            return bool(response.data)
        
        # Using in-memory database for development
        if contact_id not in contacts_db:
            return False
        
        del contacts_db[contact_id]
        return True
    
    @staticmethod
    def search_contacts(query: str, limit: int = 10) -> List[Contact]:
        """
        Search for contacts with a specific query string
        
        The search is performed across all text fields including:
        - Name
        - Email
        - Phone numbers
        - Company
        - Job title
        - Notes
        - Tags
        """
        # Get all contacts and filter them based on the query
        all_contacts = ContactService.get_all_contacts()
        
        # For proper searching, we need Contact objects
        contact_objects = [Contact.model_validate(c) if isinstance(c, dict) else c for c in all_contacts]
        
        results = [
            contact for contact in contact_objects
            if contact.search_in_fields(query)
        ]
        
        # Sort by name
        results.sort(key=lambda x: x.full_name.lower())
        
        return results[:limit]
    
    @staticmethod
    def list_contacts(
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        favorite: Optional[bool] = None,
        contact_type: Optional[str] = None
    ) -> ContactList:
        """
        List all contacts with optional filtering
        
        - **skip**: Number of contacts to skip (pagination)
        - **limit**: Maximum number of contacts to return
        - **search**: Search string to filter contacts
        - **favorite**: Filter by favorite status
        - **contact_type**: Filter by contact type
        """
        # Get all contacts
        all_contacts = ContactService.get_all_contacts()
        
        # Convert to Contact objects if they're dictionaries
        contact_objects = [Contact.model_validate(c) if isinstance(c, dict) else c for c in all_contacts]
        
        filtered_contacts = contact_objects
        
        # Filter by favorite status
        if favorite is not None:
            filtered_contacts = [c for c in filtered_contacts if c.favorite == favorite]
        
        # Filter by contact type
        if contact_type:
            filtered_contacts = [c for c in filtered_contacts if c.contact_type.value == contact_type]
        
        # Advanced search functionality
        if search:
            filtered_contacts = [c for c in filtered_contacts if c.search_in_fields(search)]
        
        # Sort by last name, then first name
        filtered_contacts.sort(key=lambda x: (x.last_name.lower(), x.first_name.lower()))
        
        total = len(filtered_contacts)
        items = filtered_contacts[skip:skip+limit]
        
        return ContactList(
            items=items,
            total=total,
            page=skip // limit + 1 if limit > 0 else 1,
            size=limit
        )
