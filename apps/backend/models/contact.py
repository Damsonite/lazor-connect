"""
Contact models for Lazor Connect API.
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID

from .base import TimestampedModel
from .enums import ContactType


class Address(BaseModel):
    """Model for address information"""
    street: str
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str
    
    def formatted_address(self) -> str:
        """Return a formatted address string"""
        address_parts = [self.street, self.city]
        if self.state:
            address_parts.append(self.state)
        address_parts.append(self.postal_code)
        address_parts.append(self.country)
        return ", ".join(address_parts)


class PhoneNumber(BaseModel):
    """Model for phone numbers"""
    number: str
    type: str = "mobile"  # mobile, home, work, etc.
    is_primary: bool = False


class SocialProfile(BaseModel):
    """Model for social media profiles"""
    platform: str  # LinkedIn, Twitter, Instagram, etc.
    username: str
    url: Optional[str] = None


class ContactBase(BaseModel):
    """Base model for contact information"""
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone_numbers: Optional[List[PhoneNumber]] = []
    addresses: Optional[List[Address]] = []
    social_profiles: Optional[List[SocialProfile]] = []
    company: Optional[str] = None
    job_title: Optional[str] = None
    contact_type: ContactType = ContactType.OTHER
    notes: Optional[str] = None
    favorite: bool = False
    tags: List[str] = []


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
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_numbers: Optional[List[PhoneNumber]] = None
    addresses: Optional[List[Address]] = None
    social_profiles: Optional[List[SocialProfile]] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    contact_type: Optional[ContactType] = None
    notes: Optional[str] = None
    favorite: Optional[bool] = None
    tags: Optional[List[str]] = None