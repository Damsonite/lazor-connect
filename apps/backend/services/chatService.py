from typing import Dict, Any
import random

from .utils import normalize_extracted_data  
from .contactService import ContactService 
from .geminiClient import GeminiClient

class ChatService:
    def __init__(self, contact_service: ContactService):
        self.contact_service = contact_service
        self.client = GeminiClient()
    
    async def _log_interaction(self, contact_id: str, user_message: str, bot_response: str):
        """
        Logs an interaction without storing full conversation history.
        This could be used for analytics or to update the 'last_connection' field.
        """
        try:
            user_preview = user_message[:30] + "..." if user_message and len(user_message) > 30 else user_message
            bot_preview = bot_response[:30] + "..." if bot_response and len(bot_response) > 30 else bot_response
            
            print(f"Logging interaction for contact_id: {contact_id}")
            print(f"User message topic: {user_preview}")
            print(f"Bot response type: {bot_preview}")
            
            # In a real implementation, you might:
            # 1. Update the contact's last_connection timestamp
            # 2. Extract and store topics from the conversation
            # 3. Update interaction frequency stats
            pass
        except Exception as e:
            print(f"Error in _log_interaction: {e}")
            # Don't let logging errors affect the main flow

    async def handle_message(self, contact_id: str, user_message: str) -> Dict[str, Any]:
        """
        Handles an incoming message from a user for a specific contact.
        Provides short, conversational responses to help build the contact profile.
        Occasionally asks for open-ended feedback and stores the user's reply as feedback.
        """
        contact = self.contact_service.get_contact(contact_id)
        if not contact:
            return {"error": "Contact not found", "status_code": 404}

        # Use GeminiClient to handle the conversation
        try:
            bot_response_text = await self.client.handle_conversation(contact, user_message)
            # Occasionally ask for feedback (e.g., 1 in 5 chance)
            if random.randint(1, 5) == 1:
                bot_response_text += "\n\nBy the way, how am I doing? Feel free to share any feedback or suggestions."
        except Exception as e:
            print(f"Error in handle_conversation: {e}")
            bot_response_text = "I'm sorry, I encountered an error processing your message. Please try again later."

        # Detect if the user's message is a feedback reply (open-ended, not like/dislike)
        feedback_triggers = ["feedback", "suggestion", "improve", "doing", "better", "worse", "bad", "good"]
        if any(kw in user_message.lower() for kw in feedback_triggers):
            feedback_store.append({
                "type": "open_feedback",
                "message": user_message,
                "contact_id": contact_id,
                "timestamp": __import__('datetime').datetime.now().isoformat()
            })

        # Log the interaction instead of storing conversation history
        await self._log_interaction(contact_id, user_message, bot_response_text)
        
        # Extract any potential profile data directly
        extracted_data = {}
        if self.client.is_available() and user_message:
            try:
                # Get raw extracted data from GeminiClient
                extracted_data = await self.client.extract_profile_data(user_message)
                # Normalize the data using the external utility function
                extracted_data = normalize_extracted_data(extracted_data)
                # Update contact if we have data
                if contact_id and extracted_data:
                    await self._update_contact_with_extracted_data(contact_id, extracted_data)
            except Exception as e:
                print(f"Error extracting or processing profile data: {e}")
                # Continue without extracted data
                extracted_data = {}

        # --- Update last_connection if AI extracted it ---
        if extracted_data and 'last_connection' in extracted_data and extracted_data['last_connection']:
            from datetime import datetime, timezone, timedelta
            try:
                last_conn = extracted_data['last_connection']
                # Handle common relative dates
                if isinstance(last_conn, str):
                    lowered = last_conn.strip().lower()
                    if lowered == 'yesterday':
                        dt = datetime.now(timezone.utc) - timedelta(days=1)
                        last_conn = dt.replace(hour=12, minute=0, second=0, microsecond=0).isoformat()
                    elif lowered == 'today':
                        dt = datetime.now(timezone.utc)
                        last_conn = dt.replace(hour=12, minute=0, second=0, microsecond=0).isoformat()
                    else:
                        try:
                            dt = datetime.fromisoformat(last_conn)
                            last_conn = dt.astimezone(timezone.utc).isoformat()
                        except Exception:
                            print(f"Could not parse last_connection string as ISO datetime: {last_conn}")
                            last_conn = None
                elif hasattr(last_conn, 'isoformat'):
                    last_conn = last_conn.astimezone(timezone.utc).isoformat()
                if last_conn:
                    self.contact_service.update_contact(contact_id, {"last_connection": last_conn})
            except Exception as e:
                print(f"Failed to update last_connection for contact {contact_id} from AI extraction: {e}")
        # --- End update ---

        return {
            "contact_id": contact_id,
            "user_message": user_message,
            "bot_response": bot_response_text,
            "contact_details": contact, # Return contact details for context if needed by frontend
            "profile_suggestions": extracted_data # Any structured data we extracted
        }

    async def get_initial_greeting(self, contact_id: str) -> Dict[str, Any]:
        """
        Provides an initial greeting focused on building the contact's profile.
        """
        contact = self.contact_service.get_contact(contact_id)
        if not contact:
            return {"error": "Contact not found", "status_code": 404}
        
        # Check how complete the contact's profile is
        profile_completeness = self._calculate_profile_completeness(contact)
        
        # Use GeminiClient for greeting generation
        try:
            greeting_text = await self.client.get_initial_greeting(contact, profile_completeness)
        except Exception as e:
            print(f"Error getting initial greeting: {e}")
            greeting_text = "Hello! I'm here to help you keep in touch with your contacts."
        
        return {
            "contact_id": contact_id,
            "greeting": greeting_text,
            "contact_details": contact
        }
        
    def _calculate_profile_completeness(self, contact: Dict) -> int:
        """
        Calculate how complete a contact's profile is based on filled fields.
        Returns a percentage from 0-100.
        """
        # Define fields that constitute a complete profile based on your contact model
        important_fields = [
            'name', 'relationship_type', 'interests', 'conversation_topics', 
            'important_dates', 'last_connection', 'preferences', 
            'family_details', 'personality', 'relationship_strength', 'recommended_contact_freq_days'
        ]
        
        # Count filled fields, checking for nested fields too
        filled_fields = 0
        for field in important_fields:
            value = contact.get(field)
            if value:
                # Check for empty lists or dictionaries
                if isinstance(value, list) and len(value) > 0:
                    filled_fields += 1
                elif isinstance(value, dict) and len(value) > 0:
                    filled_fields += 1
                else:
                    filled_fields += 1
        
        # Calculate percentage
        completeness = int((filled_fields / len(important_fields)) * 100)
        return min(100, completeness)  # Cap at 100%
    
    async def _update_contact_with_extracted_data(self, contact_id: str, extracted_data: Dict[str, Any]) -> None:
        """
        Updates the contact record with data extracted from messages
        
        Args:
            contact_id: The ID of the contact to update
            extracted_data: Dictionary containing extracted fields like birthday, interests, etc.
        """
        if not extracted_data:
            return
            
        # Get the current contact data
        contact = self.contact_service.get_contact(contact_id)
        if not contact:
            print(f"Cannot update contact {contact_id}: not found")
            return
            
        # Create an update payload
        update_payload = {}
        
        # Process nickname
        if 'nickname' in extracted_data and extracted_data['nickname']:
            update_payload['nickname'] = extracted_data['nickname']
            print(f"Updating nickname to {extracted_data['nickname']}")
        
        # Process birthday
        if 'birthday' in extracted_data and extracted_data['birthday']:
            update_payload['birthday'] = extracted_data['birthday']
            print(f"Updating birthday to {extracted_data['birthday']}")
            
        # Process interests - merge with existing interests if any
        if 'interests' in extracted_data and extracted_data['interests']:
            current_interests = contact.get('interests', []) or []
            # Convert to set to remove duplicates and back to list
            merged_interests = list(set(current_interests + extracted_data['interests']))
            update_payload['interests'] = merged_interests
            print(f"Updating interests to {merged_interests}")
            
        # Also check if we have preferences.likes that should be added to interests
        if 'preferences' in extracted_data and extracted_data['preferences']:
            if 'likes' in extracted_data['preferences'] and extracted_data['preferences']['likes']:
                # Add likes to interests as well for consistency
                likes_to_add = extracted_data['preferences']['likes']
                current_interests = update_payload.get('interests', contact.get('interests', []) or [])
                # Convert to set to remove duplicates and back to list
                merged_interests = list(set(current_interests + likes_to_add))
                update_payload['interests'] = merged_interests
                print(f"Added preferences.likes to interests: {merged_interests}")
            
        # Process important dates - add new ones
        if 'important_dates' in extracted_data and extracted_data['important_dates']:
            current_dates = contact.get('important_dates', []) or []
            # Check for duplicates by comparing date and description
            new_dates = []
            for new_date in extracted_data['important_dates']:
                if not any(d.get('date') == new_date.get('date') and 
                          d.get('description') == new_date.get('description') 
                          for d in current_dates):
                    new_dates.append(new_date)
            
            if new_dates:
                update_payload['important_dates'] = current_dates + new_dates
                print(f"Adding new important dates: {new_dates}")
                
        # Process relationship type
        if 'relationship_type' in extracted_data and extracted_data['relationship_type']:
            update_payload['relationship_type'] = extracted_data['relationship_type']
            print(f"Updating relationship type to {extracted_data['relationship_type']}")
            
        # Process preferences (likes and dislikes)
        if 'preferences' in extracted_data and extracted_data['preferences']:
            current_preferences = contact.get('preferences', {}) or {}
            if not current_preferences:
                current_preferences = {'likes': [], 'dislikes': []}
                
            # Update likes
            if 'likes' in extracted_data['preferences'] and extracted_data['preferences']['likes']:
                current_likes = current_preferences.get('likes', []) or []
                merged_likes = list(set(current_likes + extracted_data['preferences']['likes']))
                current_preferences['likes'] = merged_likes
                
            # Update dislikes
            if 'dislikes' in extracted_data['preferences'] and extracted_data['preferences']['dislikes']:
                current_dislikes = current_preferences.get('dislikes', []) or []
                merged_dislikes = list(set(current_dislikes + extracted_data['preferences']['dislikes']))
                current_preferences['dislikes'] = merged_dislikes
                
            update_payload['preferences'] = current_preferences
            print(f"Updating preferences to {current_preferences}")
            
        # Process family details
        if 'family_details' in extracted_data and extracted_data['family_details']:
            update_payload['family_details'] = extracted_data['family_details']
            print(f"Updating family details")
            
        # Process personality information
        if 'personality' in extracted_data and extracted_data['personality']:
            # If there's existing personality data, append new information
            if contact.get('personality'):
                update_payload['personality'] = f"{contact.get('personality')}\n\n{extracted_data['personality']}"
            else:
                update_payload['personality'] = extracted_data['personality']
            print(f"Updating personality information")
        
        # Update the contact if we have data to update
        if update_payload:
            # Make sure we have valid JSON for all fields and no timestamp fields
            if 'created_at' in update_payload:
                del update_payload['created_at']
            if 'updated_at' in update_payload:
                del update_payload['updated_at']
            
            # For adding family_details field as a JSON string if needed
            import json
            if 'family_details' in update_payload and isinstance(update_payload['family_details'], dict):
                update_payload['family_details'] = json.dumps(update_payload['family_details'])
            
            print(f"Updating contact {contact_id} with new data: {update_payload}")
            print(f"Original extracted data was: {extracted_data}")
            
            # Extra debug for interests and preferences
            if 'interests' in update_payload:
                print(f"INTERESTS UPDATE: {update_payload['interests']}")
            if 'preferences' in update_payload:
                print(f"PREFERENCES UPDATE: {update_payload['preferences']}")
                
            try:
                # Try the update with our improved ContactService that handles errors better
                result = self.contact_service.update_contact(contact_id, update_payload)
                if result:
                    print(f"Successfully updated contact {contact_id}")
                    # Show updated contact data
                    updated_contact = self.contact_service.get_contact(contact_id)
                    print(f"Updated contact interests: {updated_contact.get('interests')}")
                    print(f"Updated contact preferences: {updated_contact.get('preferences')}")
                else:
                    print(f"Contact update returned no result. It may not have been updated.")
            except Exception as e:
                print(f"Error updating contact: {e}")
                # Continue gracefully despite errors - don't block the chat functionality
                import traceback
                traceback.print_exc()
                # If this is a PostgreSQL error about updated_at
                if "'updated_at'" in str(e) or "new" in str(e):
                    print("This appears to be a database trigger issue. Trying direct SQL update instead...")
                    # For debugging only - in production you would want a better solution
                    try:
                        # Try one more time with a different approach - direct SQL query could be considered
                        # But for now, just log the error
                        print("Couldn't update through the API. Contact may need manual updating.")
                    except Exception as inner_e:
                        print(f"Alternative update method also failed: {inner_e}")
    
    def _sanitize_contact_data(self, data: Dict) -> Dict:
        """
        Ensure that contact data is in the correct format for Supabase storage.
        Converts objects to strings where needed and removes problematic fields.
        """
        import json
        
        # Create a copy to avoid modifying the original
        sanitized = data.copy() if data else {}
        
        # Remove system fields that might cause conflicts
        for field in ['id', 'created_at', 'updated_at']:
            if field in sanitized:
                del sanitized[field]
                
        # Ensure nested JSON structures are properly serialized
        for field in ['preferences', 'important_dates', 'contact_methods']:
            if field in sanitized and isinstance(sanitized[field], dict):
                sanitized[field] = json.dumps(sanitized[field])
                
        # Ensure arrays are properly formatted
        for field in ['interests', 'conversation_topics']:
            if field in sanitized and isinstance(sanitized[field], list):
                # Make sure we don't have any empty strings in the list
                sanitized[field] = [item for item in sanitized[field] if item]
                
        return sanitized
    
    def get_feedback_summary(self, top_n: int = 5) -> dict:
        """
        Summarizes feedback trends for model improvement analysis.
        Returns total count, per-contact count, recent feedback, and common keywords.
        """
        from collections import Counter
        import re
        
        # Defensive: feedback_store may be empty
        if not feedback_store:
            return {
                "total_feedback": 0,
                "feedback_per_contact": {},
                "recent_feedback": [],
                "common_words": []
            }
        
        # Total feedback
        total_feedback = len(feedback_store)
        
        # Feedback per contact
        feedback_per_contact = {}
        for fb in feedback_store:
            cid = fb.get("contact_id", "unknown")
            feedback_per_contact[cid] = feedback_per_contact.get(cid, 0) + 1
        
        # Most recent feedback
        recent_feedback = sorted(feedback_store, key=lambda x: x.get("timestamp", ""), reverse=True)[:top_n]
        
        # Common words (very basic, not NLP)
        all_text = " ".join(fb.get("message", "") for fb in feedback_store)
        words = re.findall(r"\b\w{4,}\b", all_text.lower())  # 4+ letter words
        stopwords = set(["this", "that", "with", "have", "from", "your", "just", "like", "about", "would", "could", "should", "doing", "good", "bad", "very", "more", "less", "than", "what", "when", "where", "which", "their", "them", "they", "been", "some", "much", "well", "even", "only", "also", "into", "over", "such", "most", "many", "other", "because", "after", "before", "while", "still", "make", "made", "want", "need", "know", "time", "help", "thanks", "thank"])
        filtered_words = [w for w in words if w not in stopwords]
        common_words = Counter(filtered_words).most_common(top_n)
        
        return {
            "total_feedback": total_feedback,
            "feedback_per_contact": feedback_per_contact,
            "recent_feedback": recent_feedback,
            "common_words": common_words
        }
