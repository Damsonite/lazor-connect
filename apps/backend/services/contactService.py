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
    def get_contact(contact_id: str) -> Optional[Dict]:
        """Get a single contact by ID (UUID string)"""
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
                     "interests", "family_details", "preferences", "personality",
                     "last_connection", "avg_days_btw_contacts", 
                     "recommended_contact_freq_days"]:
            if field in contact and contact[field] is not None:
                payload[field] = contact[field]
                
        response = supabase.table("contacts").insert(payload).execute()
        return response.data[0]
    
    @staticmethod
    def update_contact(contact_id: str, contact_data: Dict) -> Optional[Dict]:
        """Update a contact in the database"""
        try:
            # First get the current data to verify contact exists
            current = ContactService.get_contact(contact_id)
            if not current:
                print(f"Contact {contact_id} not found for update")
                return None
            
            # Remove any fields that shouldn't be directly updated
            clean_data = {k: v for k, v in contact_data.items() 
                         if k not in ['id', 'created_at', 'updated_at']}
            
            # Special handling for interests to ensure it's properly formatted as an array
            if 'interests' in clean_data:
                # If it's None, initialize as empty list
                if clean_data['interests'] is None:
                    clean_data['interests'] = []
                # If it's a string (single interest), convert to list
                elif isinstance(clean_data['interests'], str):
                    clean_data['interests'] = [clean_data['interests']]
                # Ensure all items are strings
                clean_data['interests'] = [str(item) for item in clean_data['interests'] if item]
                print(f"Formatted interests for update: {clean_data['interests']}")
            
            # Special handling for preferences to ensure proper structure
            if 'preferences' in clean_data:
                # Ensure preferences is a dictionary
                if not isinstance(clean_data['preferences'], dict):
                    # Try to convert from string if it's a string
                    if isinstance(clean_data['preferences'], str):
                        try:
                            import json
                            clean_data['preferences'] = json.loads(clean_data['preferences'])
                        except:
                            clean_data['preferences'] = {}
                    else:
                        clean_data['preferences'] = {}
                
                # Ensure likes and dislikes are lists
                if 'likes' not in clean_data['preferences']:
                    clean_data['preferences']['likes'] = []
                if 'dislikes' not in clean_data['preferences']:
                    clean_data['preferences']['dislikes'] = []
                
                print(f"Formatted preferences for update: {clean_data['preferences']}")
                
            # Special handling for personality field
            if 'personality' in clean_data:
                # If the current contact already has personality data, append the new information
                if current and 'personality' in current and current['personality']:
                    # If we're adding new information, append it to existing with a separator
                    if clean_data['personality']:
                        clean_data['personality'] = f"{current['personality']}\n\n{clean_data['personality']}"
                print(f"Formatted personality for update: {clean_data['personality']}")
            
            # Special handling for date fields to ensure proper format
            import re
            from datetime import datetime
            current_year = datetime.now().year
            
            # Validate birthday field
            if 'birthday' in clean_data and clean_data['birthday']:
                birthday_match = re.match(r'(\d{4})-(\d{2})-(\d{2})', clean_data['birthday'])
                if birthday_match:
                    year, month, day = birthday_match.groups()
                    if year == '0000' or int(year) < 1900 or int(year) > current_year:
                        # Replace with current year or default to None if date is invalid
                        try:
                            clean_data['birthday'] = f"{current_year}-{month}-{day}"
                            print(f"Fixed invalid birthday year in update: {year} -> {current_year}")
                        except:
                            print(f"Invalid birthday format: {clean_data['birthday']} - removing field")
                            del clean_data['birthday']
                else:
                    # If the format doesn't match YYYY-MM-DD, remove it
                    print(f"Invalid birthday format: {clean_data['birthday']} - removing field")
                    del clean_data['birthday']
                    
            # DO NOT add updated_at timestamp - let Supabase handle it through triggers
            # The error suggests updated_at column is handled by the database
            
            # Direct update using the Supabase client
            print(f"Sending update to Supabase for contact {contact_id} with data: {clean_data}")
            response = supabase.table("contacts").update(clean_data).eq("id", contact_id).execute()
            
            if not response.data:
                print("Update returned no data")
                # Get the current state of the contact to return
                return ContactService.get_contact(contact_id)
            
            print(f"Contact updated successfully with data: {clean_data}")
            return response.data[0] if response.data else None
            
        except Exception as e:
            print(f"Supabase update error: {e}")
            print(f"Contact update failed for contact_id: {contact_id}")
            print(f"Data being updated: {clean_data}")
            return None
    
    @staticmethod
    def delete_contact(contact_id: str) -> bool:
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
