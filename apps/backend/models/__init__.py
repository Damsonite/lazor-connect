"""
Models package for Lazor Connect API.
This module exports all models for easy importing.
"""

# Contact-related models
from .contact import (
    Contact,
    ContactBase,
    ContactCreate,
    ContactUpdate,
    ContactMethod,
    ImportantDate,
    Reminder,
    Preferences
)

# Enum types
from .enums import ContactType, RelationshipType
