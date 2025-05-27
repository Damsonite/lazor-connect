"""
Models for chat functionality in Lazor Connect API.
"""

from typing import Dict, Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ProfileUpdateRequest(BaseModel):
    fields: Dict[str, Any]
