"""
Contact models for Lazor Connect API.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from uuid import UUID, uuid4

from .base import TimestampedModel, PaginatedResponse
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
    
    @property
    def full_name(self) -> str:
        """Return the contact's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def search_in_fields(self, query: str) -> bool:
        """Search for a string in all text fields of the contact"""
        query = query.lower()
        searchable_fields = [
            self.first_name.lower(),
            self.last_name.lower(),
            self.email.lower() if self.email else "",
            self.company.lower() if self.company else "",
            self.job_title.lower() if self.job_title else "",
            self.notes.lower() if self.notes else ""
        ]
        
        # Add phone numbers
        for phone in self.phone_numbers:
            searchable_fields.append(phone.number)
        
        # Add tags
        searchable_fields.extend([tag.lower() for tag in self.tags])
        
        return any(query in field for field in searchable_fields)


class ContactCreate(ContactBase):
    """Model for creating a new contact"""
    pass


class Contact(ContactBase, TimestampedModel):
    """Model for contact responses, includes system fields"""
    id: UUID = Field(default_factory=uuid4)
    
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


# For pagination responses
class ContactList(PaginatedResponse[Contact]):
    """Model for paginated contact lists"""
    pass
