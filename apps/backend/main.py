from fastapi import FastAPI, HTTPException, Query, Path, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# Import from our local models package
from models import Contact, ContactCreate, ContactUpdate, ContactList

app = FastAPI(
    title="Lazor Connect API",
    description="API for managing contacts in Lazor Connect",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database for development
contacts_db = {}

@app.get("/ping")
def ping():
    """Health check endpoint"""
    return {"status": "online", "timestamp": datetime.now().isoformat()}

# Contact endpoints
@app.post("/contacts", response_model=Contact)
def create_contact(contact: ContactCreate):
    """Create a new contact"""
    new_contact = Contact(**contact.model_dump())
    contacts_db[str(new_contact.id)] = new_contact
    return new_contact


@app.get("/contacts", response_model=ContactList)
def list_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    favorite: Optional[bool] = None,
    contact_type: Optional[str] = None
):
    """
    List all contacts with optional filtering
    
    - **skip**: Number of contacts to skip (pagination)
    - **limit**: Maximum number of contacts to return
    - **search**: Search string to filter contacts
    - **favorite**: Filter by favorite status
    - **contact_type**: Filter by contact type
    """
    filtered_contacts = list(contacts_db.values())
    
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


@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: UUID = Path(..., title="The ID of the contact to get")):
    """Get a specific contact by ID"""
    contact_id_str = str(contact_id)
    if contact_id_str not in contacts_db:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contacts_db[contact_id_str]


@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(
    contact: ContactUpdate,
    contact_id: UUID = Path(..., title="The ID of the contact to update")
):
    """Update an existing contact"""
    contact_id_str = str(contact_id)
    if contact_id_str not in contacts_db:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    # Get existing contact
    existing_contact = contacts_db[contact_id_str]
    
    # Update fields, excluding None values
    update_data = contact.model_dump(exclude_unset=True)
    updated_contact = existing_contact.model_copy(update=update_data)
    
    # Update the timestamp
    updated_contact.update_timestamp()
    
    # Save updated contact
    contacts_db[contact_id_str] = updated_contact
    return updated_contact


@app.delete("/contacts/{contact_id}", response_model=dict)
def delete_contact(contact_id: UUID = Path(..., title="The ID of the contact to delete")):
    """Delete a contact"""
    contact_id_str = str(contact_id)
    if contact_id_str not in contacts_db:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    # Remove contact from database
    del contacts_db[contact_id_str]
    return {"message": "Contact successfully deleted"}


@app.get("/contacts/search/{query}", response_model=List[Contact])
def search_contacts(
    query: str = Path(..., title="The search query"),
    limit: int = Query(10, ge=1, le=100)
):
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
    results = [
        contact for contact in contacts_db.values()
        if contact.search_in_fields(query)
    ]
    
    # Sort by relevance (simplified - just alphabetical by name)
    results.sort(key=lambda x: x.full_name.lower())
    
    return results[:limit]
