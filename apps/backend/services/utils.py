"""
Utility functions for the backend services.
"""
from typing import Dict, Any
from datetime import datetime
import re

def clean_json_response(text: str) -> str:
    """
    Clean and prepare JSON text from AI response.
    
    Args:
        text: The response text to clean
        
    Returns:
        Cleaned JSON string
    """
    # Start with basic cleaning
    cleaned_text = text.strip() if isinstance(text, str) else text
    
    # If text is already a string (API response object), return it directly
    if not isinstance(cleaned_text, str):
        return "{}"
        
    # Remove markdown code blocks if present
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:]
    elif cleaned_text.startswith("```"):
        cleaned_text = cleaned_text[3:]
        
    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]
        
    # Final trim of whitespace
    cleaned_text = cleaned_text.strip()
    
    # Extra validation to ensure we have valid JSON format
    if not cleaned_text.startswith("{"):
        # Try to find the first { and start there
        start_index = cleaned_text.find("{")
        if start_index != -1:
            cleaned_text = cleaned_text[start_index:]
        else:
            # No JSON object found
            return "{}"
            
    # Make sure we end with a valid JSON closing
    if not cleaned_text.endswith("}"):
        end_index = cleaned_text.rfind("}")
        if end_index != -1:
            cleaned_text = cleaned_text[:end_index+1]
        else:
            # No JSON closing found
            return "{}"
    
    return cleaned_text

def normalize_extracted_data(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes and validates extracted data.
        """
        if not extracted_data:
            return {}
            
        # Create a copy to avoid modifying the original
        normalized_data = extracted_data.copy()
        
        # Validate and fix date fields
        current_year = datetime.now().year
        
        # Fix birthday if present but invalid
        if 'birthday' in normalized_data and normalized_data['birthday']:
            # Check if the year is 0000 or invalid
            birthday_match = re.match(r'(\d{4})-(\d{2})-(\d{2})', normalized_data['birthday'])
            if birthday_match:
                year, month, day = birthday_match.groups()
                if year == '0000' or int(year) < 1900 or int(year) > current_year:
                    # Replace with a reasonable year (current year)
                    normalized_data['birthday'] = f"{current_year}-{month}-{day}"
                    print(f"Fixed invalid birthday year: {year} -> {current_year}")
        
        # Make sure preferences structure is properly set up
        if 'preferences' not in normalized_data:
            normalized_data['preferences'] = {}
        if 'likes' not in normalized_data['preferences']:
            normalized_data['preferences']['likes'] = []
        if 'dislikes' not in normalized_data['preferences']:
            normalized_data['preferences']['dislikes'] = []
            
        # Ensure interests are also added to preferences.likes and vice versa
        if 'interests' in normalized_data and normalized_data['interests']:
            if not normalized_data['preferences']['likes']:
                normalized_data['preferences']['likes'] = normalized_data['interests'].copy()
            else:
                # Add any interests that aren't already in likes
                for interest in normalized_data['interests']:
                    if interest not in normalized_data['preferences']['likes']:
                        normalized_data['preferences']['likes'].append(interest)
        
        # Also ensure preferences.likes are in interests
        if normalized_data['preferences']['likes']:
            if 'interests' not in normalized_data or not normalized_data['interests']:
                normalized_data['interests'] = normalized_data['preferences']['likes'].copy()
            else:
                # Add any likes that aren't already in interests
                for like in normalized_data['preferences']['likes']:
                    if like not in normalized_data['interests']:
                        normalized_data['interests'].append(like)
                        
        return normalized_data