"""
Streak service for Lazor Connect API.
This service handles all business logic related to contact streaks.
"""
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple

from .contactService import ContactService
from utils.date import parse_date_string, get_days_since_date, is_same_day


class StreakService:
    """Service for managing contact streaks"""
    
    @staticmethod
    def calculate_streak(contact: Dict) -> Tuple[int, int]:
        """
        Calculate current and longest streak for a contact
        """
        if not contact.get("last_connection"):
            return 0, contact.get("longest_streak") or 0
            
        current_date = datetime.now(timezone.utc)
        last_connection = parse_date_string(contact["last_connection"])
        
        if last_connection is None:
            return 0, contact.get("longest_streak") or 0
        
        # Get the recommended frequency (default to 7 days if not set)
        recommended_freq = contact.get("recommended_contact_freq_days") or 7
        
        # Ensure recommended_freq is an integer
        if not isinstance(recommended_freq, int):
            recommended_freq = 7
        
        # Calculate days since last contact
        days_since_contact = get_days_since_date(last_connection, current_date)
        
        if days_since_contact is None:
            return 0, contact.get("longest_streak") or 0
        
        # Current streak logic:
        # - If within the recommended frequency window, maintain current streak
        # - If exceeded by 1 day grace period, reset to 0
        current_streak = contact.get("current_streak") or 0
        
        if days_since_contact <= recommended_freq + 1:  # 1 day grace period
            # Maintain current streak (it gets incremented when contact is made)
            pass
        else:
            # Reset streak if too much time has passed
            current_streak = 0
            
        # Longest streak should never decrease
        longest_streak = max(
            current_streak,
            contact.get("longest_streak") or 0
        )
        
        # Ensure we always return integers
        return int(current_streak), int(longest_streak)
    
    @staticmethod
    def update_streak_on_contact(contact_id: str) -> Optional[Dict]:
        """
        Update streak when a new contact/interaction is made.
        
        Args:
            contact_id: ID of the contact to update
            
        Returns:
            Updated contact data or None if contact not found
        """
        contact = ContactService.get_contact(contact_id)
        if not contact:
            return None
            
        current_date = datetime.now(timezone.utc)
        
        # Calculate new streak values
        current_streak, longest_streak = StreakService.calculate_streak(contact)
        
        # Ensure streak values are integers, not None
        current_streak = current_streak or 0
        longest_streak = longest_streak or 0
        
        print(f"DEBUG: After calculate_streak - current: {current_streak}, longest: {longest_streak}")
        
        # Check if this is a new contact period (not same day)
        last_connection = parse_date_string(contact.get("last_connection"))
            
        # Only increment if it's a different day or first contact
        if not last_connection or not is_same_day(last_connection, current_date):
            print(f"DEBUG: Incrementing streak from {current_streak}")
            current_streak += 1
            print(f"DEBUG: New current_streak: {current_streak}")
            
        # Update longest streak if current is higher
        longest_streak = max(current_streak, longest_streak)
        
        # Update the contact with new streak data
        update_data = {
            "last_connection": current_date.isoformat(),
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "last_streak_update": current_date.isoformat()
        }
        
        return ContactService.update_contact(contact_id, update_data)
    
    @staticmethod
    def get_streak_stats() -> Dict:
        """
        Get overall streak statistics across all contacts.
        
        Returns:
            Dictionary with streak statistics
        """
        contacts = ContactService.list_contacts()
        
        total_active_streaks = 0
        total_longest_streak = 0
        contacts_with_streaks = 0
        
        for contact in contacts:
            current_streak = contact.get("current_streak") or 0
            longest_streak = contact.get("longest_streak") or 0
            
            if current_streak > 0:
                total_active_streaks += current_streak
                contacts_with_streaks += 1
                
            if longest_streak > total_longest_streak:
                total_longest_streak = longest_streak
                
        return {
            "total_contacts": len(contacts),
            "contacts_with_active_streaks": contacts_with_streaks,
            "average_active_streak": (
                total_active_streaks / contacts_with_streaks 
                if contacts_with_streaks > 0 else 0
            ),
            "highest_streak_ever": total_longest_streak
        }
