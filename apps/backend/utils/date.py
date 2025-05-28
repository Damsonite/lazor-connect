"""
Date-related utility functions for the backend services.
"""
from datetime import datetime, timezone
from typing import Optional, Union


def parse_date_string(date_str: Union[str, datetime]) -> Optional[datetime]:
    """
    Parse a date string or datetime object to a timezone-aware datetime.
    
    Args:
        date_str: Date string in ISO format or datetime object
        
    Returns:
        Timezone-aware datetime object or None if parsing fails
    """
    if date_str is None:
        return None
        
    # If it's already a datetime object
    if isinstance(date_str, datetime):
        # Make sure it's timezone-aware
        if date_str.tzinfo is None:
            return date_str.replace(tzinfo=timezone.utc)
        return date_str
    
    # If it's a string, try to parse it
    if isinstance(date_str, str):
        try:
            # Try parsing ISO format
            parsed_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            # Make sure it's timezone-aware
            if parsed_date.tzinfo is None:
                return parsed_date.replace(tzinfo=timezone.utc)
            return parsed_date
        except (ValueError, TypeError):
            return None
    
    return None


def get_date_difference_in_days(date1: Union[str, datetime], date2: Union[str, datetime]) -> Optional[int]:
    """
    Calculate the difference in days between two dates.
    
    Args:
        date1: First date (string or datetime)
        date2: Second date (string or datetime)
        
    Returns:
        Number of days between the dates, or None if parsing fails
    """
    parsed_date1 = parse_date_string(date1)
    parsed_date2 = parse_date_string(date2)
    
    if parsed_date1 is None or parsed_date2 is None:
        return None
    
    # Calculate difference
    diff = abs((parsed_date1 - parsed_date2).days)
    return diff


def get_days_since_date(date: Union[str, datetime], reference_date: Optional[datetime] = None) -> Optional[int]:
    """
    Get the number of days since a given date.
    
    Args:
        date: The date to calculate from
        reference_date: The reference date (defaults to current UTC time)
        
    Returns:
        Number of days since the date, or None if parsing fails
    """
    if reference_date is None:
        reference_date = datetime.now(timezone.utc)
    
    parsed_date = parse_date_string(date)
    if parsed_date is None:
        return None
    
    # Calculate days since
    diff = (reference_date - parsed_date).days
    return diff


def is_same_day(date1: Union[str, datetime], date2: Union[str, datetime]) -> bool:
    """
    Check if two dates are on the same day (ignoring time).
    
    Args:
        date1: First date
        date2: Second date
        
    Returns:
        True if dates are on the same day, False otherwise
    """
    parsed_date1 = parse_date_string(date1)
    parsed_date2 = parse_date_string(date2)
    
    if parsed_date1 is None or parsed_date2 is None:
        return False
    
    # Compare dates (ignore time)
    return parsed_date1.date() == parsed_date2.date()


def is_consecutive_day(date1: Union[str, datetime], date2: Union[str, datetime]) -> bool:
    """
    Check if two dates are consecutive days.
    
    Args:
        date1: First date
        date2: Second date
        
    Returns:
        True if dates are consecutive days, False otherwise
    """
    diff = get_date_difference_in_days(date1, date2)
    return diff == 1 if diff is not None else False
