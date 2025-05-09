"""
Base models and utilities for Lazor Connect API.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Generic, List, TypeVar


# Type variable for generic models
T = TypeVar('T')


class TimestampedModel(BaseModel):
    """Base model with creation and update timestamps"""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def update_timestamp(self):
        """Update the updated_at timestamp to the current time"""
        self.updated_at = datetime.now()


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic model for paginated responses"""
    items: List[T]
    total: int
    page: int = 1
    size: int = 10
