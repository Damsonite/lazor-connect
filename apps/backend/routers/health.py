"""
Health check router for Lazor Connect API.
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    tags=["health"]
)


@router.get("/ping")
def ping():
    """Health check endpoint"""
    return {"status": "online", "timestamp": datetime.now().isoformat()}
