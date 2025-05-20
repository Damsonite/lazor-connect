#!/usr/bin/env python
"""
Migration script to update the database schema.
This script converts the old contact model to the new contact model.
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Add the project root to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()


def migrate_contacts():
    """Migrate contacts from the old schema to the new schema."""
    supabase_url: str = os.getenv("SUPABASE_URL")
    supabase_key: str = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set")
        sys.exit(1)
        
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Get all contacts from the old schema
    try:
        response = supabase.table("contacts").select("*").execute()
        contacts = response.data
        print(f"Found {len(contacts)} contacts to migrate")
    except Exception as e:
        print(f"Error fetching contacts: {e}")
        sys.exit(1)
    
    # Migrate each contact
    for contact in contacts:
        try:
            # Create the new contact with combined name
            new_contact = {
                "name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip(),
                "nickname": None,
                "birthday": None,
                "relationship_type": map_contact_type_to_relationship(contact.get('contact_type')),
                "family_details": contact.get('notes')
            }
            
            # Insert the contact into the new schema
            response = supabase.table("contacts_new").insert(new_contact).execute()
            new_id = response.data[0]["id"]
            
            # Migrate phone numbers if they exist
            if contact.get('phone_numbers'):
                for phone in contact.get('phone_numbers', []):
                    contact_method = {
                        "contact_id": new_id,
                        "type": "phone",
                        "value": phone.get('number'),
                        "preferred": phone.get('is_primary', False)
                    }
                    supabase.table("contact_methods").insert(contact_method).execute()
            
            # Migrate email if it exists
            if contact.get('email'):
                contact_method = {
                    "contact_id": new_id,
                    "type": "email",
                    "value": contact.get('email'),
                    "preferred": True
                }
                supabase.table("contact_methods").insert(contact_method).execute()
            
            # Migrate social profiles if they exist
            for profile in contact.get('social_profiles', []):
                contact_method = {
                    "contact_id": new_id,
                    "type": "social_media",
                    "value": f"{profile.get('platform')}: {profile.get('username')}",
                    "preferred": False
                }
                supabase.table("contact_methods").insert(contact_method).execute()
                
            print(f"Migrated contact {new_contact['name']}")
            
        except Exception as e:
            print(f"Error migrating contact {contact.get('id')}: {e}")
    
    print("Migration completed")


def map_contact_type_to_relationship(contact_type):
    """Map the old contact type to the new relationship type."""
    if not contact_type:
        return None
        
    mapping = {
        "personal": "friend",
        "work": "colleague",
        "family": "family",
        "other": "other"
    }
    return mapping.get(contact_type, "other")


if __name__ == "__main__":
    migrate_contacts()
