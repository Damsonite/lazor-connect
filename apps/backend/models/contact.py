"""
Contact models for Lazor Connect API.
"""

from datetime import date, datetime
from pydantic import BaseModel
from typing import Dict, List, Optional
from uuid import UUID

from .base import TimestampedModel
from .enums import ContactType, RelationshipType


class ContactMethod(BaseModel):
    """Model for contact methods"""
    type: str  # e.g., 'presential', 'phone', 'social_media'
    value: str  # e.g., 'cinema', '123-456-7890', '@username'
    preferred: Optional[bool] = None


class ImportantDate(BaseModel):
    """Model for important dates"""
    date: date
    description: str


class Reminder(BaseModel):
    """Model for reminders"""
    text: str
    due_date: Optional[date] = None


class Preferences(BaseModel):
    """Model for preferences"""
    likes: Optional[List[str]] = None
    dislikes: Optional[List[str]] = None


class ContactBase(BaseModel):
    """Base model for contact information"""
    # Basic contact information
    name: str
    nickname: Optional[str] = None
    birthday: Optional[str] = None  # ISO format string for compatibility
    contact_methods: Optional[List[ContactMethod]] = None
    
    # Relationship management fields
    last_connection: Optional[datetime] = None
    avg_days_btw_contacts: Optional[float] = None
    recommended_contact_freq_days: Optional[int] = None
    relationship_type: Optional[str] = None  # e.g., 'friend', 'family', 'colleague'
    relationship_strength: Optional[int] = None  # 1-5
    
    # Contextual information
    conversation_topics: Optional[List[str]] = None
    important_dates: Optional[List[ImportantDate]] = None
    reminders: Optional[List[Reminder]] = None
    
    # Personal details
    interests: Optional[List[str]] = None
    family_details: Optional[str] = None
    preferences: Optional[Preferences] = None


class ContactCreate(ContactBase):
    """Model for creating a new contact"""
    pass


class Contact(ContactBase, TimestampedModel):
    """Model for contact responses, includes system fields"""
    id: UUID
    
    class Config:
        from_attributes = True


class ContactUpdate(BaseModel):
    """Model for updating an existing contact (all fields optional)"""
    name: Optional[str] = None
    nickname: Optional[str] = None
    birthday: Optional[str] = None
    contact_methods: Optional[List[ContactMethod]] = None
    
    last_connection: Optional[datetime] = None
    avg_days_btw_contacts: Optional[float] = None
    recommended_contact_freq_days: Optional[int] = None
    relationship_type: Optional[str] = None
    relationship_strength: Optional[int] = None
    
    conversation_topics: Optional[List[str]] = None
    important_dates: Optional[List[ImportantDate]] = None
    reminders: Optional[List[Reminder]] = None
    
    interests: Optional[List[str]] = None
    family_details: Optional[str] = None
    preferences: Optional[Preferences] = None