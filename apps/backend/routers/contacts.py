"""
Contact router for Lazor Connect API.
"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from uuid import UUID

from models import Contact, ContactCreate, ContactUpdate
from services.contactService import ContactService

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    responses={404: {"description": "Contact not found"}},
)


@router.post("", response_model=Contact)
def create_contact(contact: ContactCreate):
    """Create a new contact"""
    new_contact = Contact(**contact.model_dump(mode="json"))
    return ContactService.create_contact(new_contact.model_dump(mode="json"))


@router.get("", response_model=List[Contact])
def list_contacts(
    search: Optional[str] = None,
    favorite: Optional[bool] = None,
    contact_type: Optional[str] = None
):
    """
    List all contacts with optional filtering
    
    - **search**: Search string to filter contacts
    - **favorite**: Filter by favorite status
    - **contact_type**: Filter by contact type
    """
    return ContactService.list_contacts(
        search=search,
        favorite=favorite,
        contact_type=contact_type
    )


@router.get("/search/{query}", response_model=List[Contact])
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
    return ContactService.search_contacts(query=query, limit=limit)


@router.get("/{contact_id}", response_model=Contact)
def get_contact(contact_id: UUID = Path(..., title="The ID of the contact to get")):
    """Get a specific contact by ID"""
    contact_id_str = str(contact_id)
    contact = ContactService.get_contact(contact_id_str)
    
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return contact


@router.put("/{contact_id}", response_model=Contact)
def update_contact(
    contact: ContactUpdate,
    contact_id: UUID = Path(..., title="The ID of the contact to update")
):
    """Update an existing contact"""
    contact_id_str = str(contact_id)
    
    # Update fields, excluding None values
    update_data = contact.model_dump(exclude_unset=True)
    
    # Update the contact
    updated_contact = ContactService.update_contact(contact_id_str, update_data)
    
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return updated_contact


@router.delete("/{contact_id}", response_model=dict)
def delete_contact(contact_id: UUID = Path(..., title="The ID of the contact to delete")):
    """Delete a contact"""
    contact_id_str = str(contact_id)
    
    # Delete the contact
    success = ContactService.delete_contact(contact_id_str)
    
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return {"message": "Contact successfully deleted"}
