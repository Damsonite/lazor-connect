"""
Base models and utilities for Lazor Connect API.
"""

from pydantic import BaseModel
from datetime import datetime

class TimestampedModel(BaseModel):
    """Base model with creation and update timestamps"""
    created_at: datetime
    updated_at: datetime