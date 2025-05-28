from typing import Dict, Any
import random
import json
from datetime import datetime, timezone

from .contactService import ContactService 
from .geminiClient import GeminiClient
from utils.json import normalize_extracted_data

# Import feedback_store for logging user feedback
try:
    from routers.feedback import feedback_store
except ImportError:
    # Fallback if feedback module is not available
    feedback_store = []  

class ChatService:
    def __init__(self, contact_service: ContactService):
        self.contact_service = contact_service
        self.client = GeminiClient()
    
    async def _log_interaction(self, contact_id: str, user_message: str, bot_response: str):
        """
        Logs an interaction and updates streak automatically.
        This updates the contact's last_connection timestamp and streak data.
        """
        try:
            user_preview = user_message[:30] + "..." if user_message and len(user_message) > 30 else user_message
            bot_preview = bot_response[:30] + "..." if bot_response and len(bot_response) > 30 else bot_response
            
            print(f"Logging interaction for contact_id: {contact_id}")
            print(f"User message topic: {user_preview}")
            print(f"Bot response type: {bot_preview}")
            
            # Update streak on meaningful interaction
            from .streakService import StreakService
            updated_contact = StreakService.update_streak_on_contact(contact_id)
            
            if updated_contact:
                print(f"Updated streak - Current: {updated_contact.get('current_streak', 0)}, Longest: {updated_contact.get('longest_streak', 0)}")
            else:
                print(f"Failed to update streak for contact {contact_id}")
                
        except Exception as e:
            print(f"Error in _log_interaction: {e}")
            # Don't let logging errors affect the main flow

    async def handle_message(self, contact_id: str, user_message: str) -> Dict[str, Any]:
        """
        Handles an incoming message from a user for a specific contact.
        Focuses on motivating regular contact like Duolingo, rather than just collecting information.
        """
        contact = self.contact_service.get_contact(contact_id)
        if not contact:
            return {"error": "Contact not found", "status_code": 404}

        # Check if user is confirming they contacted someone
        contact_confirmation = await self._check_contact_confirmation(user_message)
        if contact_confirmation["is_confirmation"]:
            return await self._handle_contact_confirmation(contact_id, user_message, contact_confirmation)

        # Check if user is providing information about preference changes
        preference_changes = await self._extract_preference_changes(user_message, contact)
        if preference_changes:
            await self._handle_preference_changes(contact_id, preference_changes)

        # Get contact status to determine response type
        contact_status = self._get_contact_status(contact)
        
        # Generate appropriate response based on status
        if contact_status["message_type"] == "motivate":
            bot_response_text = await self._generate_motivation_message(contact, contact_status)
        elif contact_status["message_type"] == "check":
            bot_response_text = await self._generate_check_message(contact, contact_status)
        else:  # celebrate
            bot_response_text = await self._generate_celebration_message(contact, contact_status)

        # Extract any potential profile data from the message
        extracted_data = {}
        if self.client.is_available() and user_message:
            try:
                extracted_data = await self.client.extract_profile_data(user_message)
                from utils.json import normalize_extracted_data
                extracted_data = normalize_extracted_data(extracted_data)
                if contact_id and extracted_data:
                    await self._update_contact_with_extracted_data(contact_id, extracted_data)
            except Exception as e:
                print(f"Error extracting profile data: {e}")
                extracted_data = {}

        # Log the interaction
        await self._log_interaction(contact_id, user_message, bot_response_text)

        return {
            "contact_id": contact_id,
            "user_message": user_message,
            "bot_response": bot_response_text,
            "contact_details": contact,
            "contact_status": contact_status,
            "profile_suggestions": extracted_data
        }

    def _get_contact_status(self, contact: Dict) -> Dict[str, Any]:
        """
        Determine the current status of a contact based on last connection and recommended frequency.
        """
        current_date = datetime.now(timezone.utc)
        last_connection = contact.get("last_connection")
        recommended_freq = contact.get("recommended_contact_freq_days") or 7  # Default to 7 days if None
        
        if not last_connection:
            return {
                "status": "OVERDUE",
                "days_since_contact": 999,
                "recommended_frequency": recommended_freq,
                "message_type": "motivate",
                "urgency_level": "high"
            }
        
        # Parse last connection date with better error handling
        try:
            # Remove any Z suffix and add UTC timezone
            clean_date_str = last_connection.replace('Z', '').replace('UTC', '')
            
            # Try to parse as ISO format
            last_conn_date = datetime.fromisoformat(clean_date_str)
            
            # Make timezone-aware if it isn't already
            if last_conn_date.tzinfo is None:
                last_conn_date = last_conn_date.replace(tzinfo=timezone.utc)
                
            days_since = (current_date - last_conn_date).days
            print(f"Successfully parsed date. Days since contact: {days_since}")
            
        except Exception as e:
            print(f"Error parsing last_connection date '{last_connection}': {e}")
            # If we can't parse the date, assume it's overdue
            days_since = 999
            
        # Determine status
        if days_since == 0:
            status = "CONTACTED_TODAY"
            message_type = "celebrate"
            urgency_level = "low"
        elif days_since >= recommended_freq:
            status = "OVERDUE"
            message_type = "motivate"
            urgency_level = "high"
        elif days_since == recommended_freq - 1:
            status = "DUE_TODAY"
            message_type = "motivate"
            urgency_level = "medium"
        elif days_since <= 2:
            status = "RECENT_BUT_CHECK"
            message_type = "check"
            urgency_level = "low"
        else:
            status = "OVERDUE"
            message_type = "motivate"
            urgency_level = "medium"
            
        return {
            "status": status,
            "days_since_contact": days_since,
            "recommended_frequency": recommended_freq,
            "message_type": message_type,
            "urgency_level": urgency_level
        }

    async def _check_contact_confirmation(self, user_message: str) -> Dict[str, Any]:
        """
        Check if the user is confirming they contacted someone.
        """
        confirmation_keywords = [
            "yes", "yeah", "yep", "si", "sí", "talked", "spoke", "called", "texted", 
            "messaged", "met", "saw", "visited", "contacted", "reached out", "hablé", "llamé"
        ]
        
        message_lower = user_message.lower()
        is_confirmation = any(keyword in message_lower for keyword in confirmation_keywords)
        
        # Check for negative responses
        negative_keywords = ["no", "not", "haven't", "didn't", "nope"]
        is_negative = any(keyword in message_lower for keyword in negative_keywords)
        
        return {
            "is_confirmation": is_confirmation and not is_negative,
            "is_negative": is_negative,
            "confidence": 0.8 if is_confirmation else 0.3
        }

    async def _handle_contact_confirmation(self, contact_id: str, user_message: str, confirmation: Dict) -> Dict[str, Any]:
        """
        Handle when user confirms they contacted someone.
        """
        # Update streak and last connection
        from .streakService import StreakService
        updated_contact = StreakService.update_streak_on_contact(contact_id)
        
        if not updated_contact:
            return {"error": "Contact not found", "status_code": 404}
        
        # Generate celebration response
        current_streak = updated_contact.get("current_streak", 0)
        longest_streak = updated_contact.get("longest_streak", 0)
        
        celebration_messages = [
            f"¡Fantástico! Tu racha con {updated_contact.get('name')} ahora es de {current_streak} días. ¡Sigue así!",
            f"¡Excelente! Has mantenido el contacto {current_streak} días seguidos. ¡Qué buena conexión!",
            f"¡Increíble! Tu racha es de {current_streak} días. Realmente valoras esta relación."
        ]
        
        if current_streak == longest_streak and current_streak > 1:
            celebration_messages.append(f"¡Nuevo récord! {current_streak} días es tu racha más larga con {updated_contact.get('name')}!")
        
        import random
        bot_response = random.choice(celebration_messages)
        
        # Ask about the interaction
        bot_response += " ¿De qué hablaron? Me ayudará a sugerir temas para la próxima vez."
        
        # Extract information from the user's description
        extracted_data = {}
        if self.client.is_available():
            try:
                extracted_data = await self.client.extract_profile_data(user_message)
                from utils.json import normalize_extracted_data
                extracted_data = normalize_extracted_data(extracted_data)
                if extracted_data:
                    await self._update_contact_with_extracted_data(contact_id, extracted_data)
            except Exception as e:
                print(f"Error extracting data from confirmation: {e}")
        
        return {
            "contact_id": contact_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "contact_details": updated_contact,
            "streak_updated": True,
            "current_streak": current_streak,
            "profile_suggestions": extracted_data
        }

    async def _generate_motivation_message(self, contact: Dict, status: Dict) -> str:
        """
        Generate a motivational message to encourage contacting someone.
        """
        name = contact.get('name', 'esta persona')
        days_since = status["days_since_contact"]
        
        if self.client.is_available():
            try:
                # Use Gemini to generate personalized conversation starters
                duolingo_prompt = self._build_duolingo_prompt(contact, status, "motivate")
                return await self.client.generate_content(duolingo_prompt)
            except Exception as e:
                print(f"Error generating motivation message: {e}")
        
        # Fallback messages
        if days_since >= 14:
            return f"¡Han pasado {days_since} días desde que contactaste a {name}! Es momento de reconectarse. ¿Qué tal si les preguntas cómo están?"
        elif days_since >= 7:
            return f"Han pasado {days_since} días desde tu última conexión con {name}. ¿Has hablado con ellos hoy?"
        else:
            return f"¿Ya contactaste a {name} hoy? ¡Mantén esa racha activa!"

    async def _generate_check_message(self, contact: Dict, status: Dict) -> str:
        """
        Generate a message to check if user has contacted someone recently.
        """
        name = contact.get('name', 'esta persona')
        
        if self.client.is_available():
            try:
                duolingo_prompt = self._build_duolingo_prompt(contact, status, "check")
                return await self.client.generate_content(duolingo_prompt)
            except Exception as e:
                print(f"Error generating check message: {e}")
        
        return f"¿Has hablado con {name} hoy? Si no, ¡es un buen momento para contactarlos!"

    async def _generate_celebration_message(self, contact: Dict, status: Dict) -> str:
        """
        Generate a celebration message for recent contact.
        """
        name = contact.get('name', 'esta persona')
        current_streak = contact.get('current_streak', 0)
        
        if self.client.is_available():
            try:
                duolingo_prompt = self._build_duolingo_prompt(contact, status, "celebrate")
                return await self.client.generate_content(duolingo_prompt)
            except Exception as e:
                print(f"Error generating celebration message: {e}")
        
        return f"¡Excelente! Ya contactaste a {name} hoy. Tu racha actual es de {current_streak} días. ¿Cómo estuvo la conversación?"

    def _build_duolingo_prompt(self, contact: Dict, status: Dict, message_type: str) -> str:
        """
        Build a prompt for Duolingo-style messaging.
        """
        # Load Duolingo mode instructions
        duolingo_instructions = self.client._load_prompt_if_exists("duolingo_mode_instructions")
        
        prompt_parts = [duolingo_instructions or "You are a relationship motivation assistant like Duolingo for connections."]
        
        # Add contact context
        name = contact.get('name', 'esta persona')
        prompt_parts.append(f"Contact: {name}")
        
        if contact.get('interests'):
            prompt_parts.append(f"Interests: {', '.join(contact.get('interests'))}")
        if contact.get('conversation_topics'):
            prompt_parts.append(f"Previous topics: {', '.join(contact.get('conversation_topics'))}")
        if contact.get('relationship_type'):
            prompt_parts.append(f"Relationship: {contact.get('relationship_type')}")
        
        # Add status information
        prompt_parts.append(f"Days since last contact: {status['days_since_contact']}")
        prompt_parts.append(f"Recommended frequency: every {status['recommended_frequency']} days")
        prompt_parts.append(f"Current streak: {contact.get('current_streak', 0)} days")
        prompt_parts.append(f"Message type needed: {message_type}")
        
        return "\n".join(prompt_parts)

    async def _extract_preference_changes(self, user_message: str, contact: Dict) -> Dict[str, Any]:
        """
        Extract changes in preferences (like "they don't like X anymore").
        """
        if not self.client.is_available():
            return {}
        
        change_indicators = ["doesn't like", "don't like", "no longer", "stopped", "quit", "gave up", "used to like"]
        message_lower = user_message.lower()
        
        if not any(indicator in message_lower for indicator in change_indicators):
            return {}
        
        try:
            # Use AI to extract preference changes
            change_prompt = f"""
            Analyze this message for preference changes about a contact:
            "{user_message}"
            
            Look for things they NO LONGER like or do. Return JSON with:
            {{
                "removed_interests": ["list of interests to remove"],
                "removed_likes": ["list of likes to remove"], 
                "added_dislikes": ["list of new dislikes"],
                "changes_detected": true/false
            }}
            """
            
            response = await self.client.generate_content(change_prompt)
            from utils.json import clean_json_response
            import json
            
            cleaned_response = clean_json_response(response)
            return json.loads(cleaned_response)
            
        except Exception as e:
            print(f"Error extracting preference changes: {e}")
            return {}

    async def _handle_preference_changes(self, contact_id: str, changes: Dict[str, Any]) -> None:
        """
        Handle preference changes by updating the contact.
        """
        if not changes.get("changes_detected"):
            return
        
        contact = self.contact_service.get_contact(contact_id)
        if not contact:
            return
        
        update_payload = {}
        
        # Remove interests
        if changes.get("removed_interests"):
            current_interests = contact.get('interests', []) or []
            updated_interests = [i for i in current_interests if i not in changes["removed_interests"]]
            update_payload['interests'] = updated_interests
        
        # Update preferences
        if changes.get("removed_likes") or changes.get("added_dislikes"):
            current_prefs = contact.get('preferences', {}) or {}
            
            if changes.get("removed_likes"):
                current_likes = current_prefs.get('likes', []) or []
                updated_likes = [l for l in current_likes if l not in changes["removed_likes"]]
                current_prefs['likes'] = updated_likes
            
            if changes.get("added_dislikes"):
                current_dislikes = current_prefs.get('dislikes', []) or []
                new_dislikes = list(set(current_dislikes + changes["added_dislikes"]))
                current_prefs['dislikes'] = new_dislikes
            
            update_payload['preferences'] = current_prefs
        
        if update_payload:
            self.contact_service.update_contact(contact_id, update_payload)
            print(f"Updated contact {contact_id} with preference changes: {update_payload}")

    async def get_initial_greeting(self, contact_id: str) -> Dict[str, Any]:
        """
        Provides an initial greeting focused on motivating contact like Duolingo.
        """
        try:
            print(f"Getting greeting for contact: {contact_id}")
            contact = self.contact_service.get_contact(contact_id)
            if not contact:
                return {"error": "Contact not found", "status_code": 404}
            
            print(f"Contact found: {contact.get('name')}")
            
            # Get contact status to determine the type of greeting
            print("Getting contact status...")
            contact_status = self._get_contact_status(contact)
            print(f"Contact status: {contact_status}")
            
            # Generate appropriate greeting based on status
            print(f"Generating {contact_status['message_type']} message...")
            try:
                if contact_status["message_type"] == "motivate":
                    greeting_text = await self._generate_motivation_message(contact, contact_status)
                elif contact_status["message_type"] == "check":
                    greeting_text = await self._generate_check_message(contact, contact_status)
                else:  # celebrate
                    greeting_text = await self._generate_celebration_message(contact, contact_status)
                print(f"Generated greeting: {greeting_text[:50]}...")
            except Exception as e:
                print(f"Error generating greeting message: {e}")
                import traceback
                traceback.print_exc()
                name = contact.get('name', 'esta persona')
                greeting_text = f"¡Hola! Te ayudo a mantener el contacto con {name}."
            
            return {
                "contact_id": contact_id,
                "greeting": greeting_text,
                "contact_details": contact,
                "contact_status": contact_status
            }
        except Exception as e:
            print(f"Error in get_initial_greeting: {e}")
            import traceback
            traceback.print_exc()
            raise e
        
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
