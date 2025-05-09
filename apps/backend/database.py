"""
Database module for Lazor Connect API.
This module provides the database interface used by the routers.
It can work with both the in-memory database for development and
external databases like Supabase for production.
"""
import os
from typing import Dict, List, Optional, Any
from uuid import UUID

# Import the Supabase client if available
try:
    from db import supabase
    USE_SUPABASE = bool(os.getenv("USE_SUPABASE", ""))
except (ImportError, AttributeError):
    USE_SUPABASE = False

# In-memory database for development
contacts_db = {}

# Database interface functions
def get_all_contacts() -> List[Dict]:
    """Get all contacts from the database"""
    if USE_SUPABASE:
        # This would be replaced with actual Supabase queries in production
        response = supabase.table("contacts").select("*").execute()
        return response.data
    return list(contacts_db.values())

def get_contact(contact_id: str) -> Optional[Dict]:
    """Get a single contact by ID"""
    if USE_SUPABASE:
        # This would be replaced with actual Supabase queries in production
        response = supabase.table("contacts").select("*").eq("id", contact_id).execute()
        return response.data[0] if response.data else None
    return contacts_db.get(contact_id)

def create_contact(contact: Dict) -> Dict:
    """Create a new contact in the database"""
    if USE_SUPABASE:
        # This would be replaced with actual Supabase queries in production
        response = supabase.table("contacts").insert(contact).execute()
        return response.data[0]
    
    contact_id = str(contact.id)
    contacts_db[contact_id] = contact
    return contact

def update_contact(contact_id: str, contact_data: Dict) -> Optional[Dict]:
    """Update a contact in the database"""
    if USE_SUPABASE:
        # This would be replaced with actual Supabase queries in production
        response = supabase.table("contacts").update(contact_data).eq("id", contact_id).execute()
        return response.data[0] if response.data else None
    
    if contact_id not in contacts_db:
        return None
    
    contacts_db[contact_id].update(contact_data)
    return contacts_db[contact_id]

def delete_contact(contact_id: str) -> bool:
    """Delete a contact from the database"""
    if USE_SUPABASE:
        # This would be replaced with actual Supabase queries in production
        response = supabase.table("contacts").delete().eq("id", contact_id).execute()
        return bool(response.data)
    
    if contact_id not in contacts_db:
        return False
    
    del contacts_db[contact_id]
    return True
