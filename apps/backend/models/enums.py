"""
Enum definitions for Lazor Connect API.
"""

from enum import Enum


class ContactType(str, Enum):
    """Enum for contact types"""
    PERSONAL = "personal"
    WORK = "work"
    FAMILY = "family"
    OTHER = "other"
    
    
class RelationshipType(str, Enum):
    """Enum for relationship types"""
    FRIEND = "friend"
    FAMILY = "family"
    COLLEAGUE = "colleague"
    ACQUAINTANCE = "acquaintance"
    PROFESSIONAL = "professional"
    OTHER = "other"
