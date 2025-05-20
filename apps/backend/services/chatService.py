import os
from typing import Dict, Any, List
from google import genai

from .contactService import ContactService 

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY environment variable not set. ChatService may not function correctly.")
    client = None
else:
    client = genai.Client(api_key=GEMINI_API_KEY)

class ChatService:
    def __init__(self, contact_service: ContactService):
        self.contact_service = contact_service
        self.client = client
        pass
    
    async def _log_interaction(self, contact_id: str, user_message: str, bot_response: str):
        """
        Logs an interaction without storing full conversation history.
        This could be used for analytics or to update the 'last_connection' field.
        """
        print(f"Logging interaction for contact_id: {contact_id}")
        print(f"User message topic: {user_message[:30]}...")
        print(f"Bot response type: {bot_response[:30]}...")
        
        # In a real implementation, you might:
        # 1. Update the contact's last_connection timestamp
        # 2. Extract and store topics from the conversation
        # 3. Update interaction frequency stats
        pass
    
    async def _extract_profile_data(self, message: str, contact_id: str = None) -> Dict[str, Any]:
        """
        Analyzes a message to extract structured data that could update a profile.
        For example, detecting interests, important dates, or preferences.
        
        Uses the Gemini API to extract structured data from free text.
        If contact_id is provided, will update the contact with the extracted data.
        """
        if not self.client or not message:
            return {}
        
        # Create a prompt that asks the model to extract structured data from the message
        extraction_prompt = (
            "Extract structured contact information from this message. "
            "ONLY return data that's clearly mentioned in this exact message (not previous context).\n"
            "Return a JSON object with ONLY the following properties where info is clearly present:\n"
            "- birthday: Extract birthday in ISO format (YYYY-MM-DD) if mentioned\n"
            "- interests: Array of interests or hobbies mentioned\n"
            "- important_dates: Array of objects with {date: 'YYYY-MM-DD', description: 'string'}\n"
            "- relationship_type: String (friend, family, colleague, etc)\n"
            "- preferences: {likes: [array of things they like], dislikes: [array of things they dislike]}\n"
            "- family_details: String with family information\n\n"
            "Format as valid JSON only. No explanations or other text. Return empty object if no relevant information.\n\n"
            f"Message: '{message}'"
        )
        
        try:
            # Call Gemini API to extract structured data
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[extraction_prompt]
            )
            
            # Try to parse the response as JSON
            extracted_text = response.text.strip()
            
            # Sometimes the model returns markdown code blocks, so strip those if present
            if extracted_text.startswith("```json"):
                extracted_text = extracted_text[7:]
            if extracted_text.startswith("```"):
                extracted_text = extracted_text[3:]
            if extracted_text.endswith("```"):
                extracted_text = extracted_text[:-3]
            
            extracted_text = extracted_text.strip()
            
            # Parse the JSON
            import json
            extracted_data = json.loads(extracted_text)
            
            # If contact_id is provided, update the contact with this data
            if contact_id and extracted_data and self.contact_service:
                await self._update_contact_with_extracted_data(contact_id, extracted_data)
            
            return extracted_data
        except Exception as e:
            print(f"Error extracting profile data: {e}")
            return {}

    async def _call_gemini_api(self, prompt: str, history: List[Dict[str, str]] = None) -> str:
        """
        Calls the actual Gemini API.
        """
        if not self.client:
            print("ERROR: Gemini client not initialized. Please set GEMINI_API_KEY.")
            return "Error: AI model not available."

        print(f"Calling Gemini API with prompt: {prompt[:100]}...")
        
        try:
            model = "gemini-2.0-flash"  # You can also use other models like gemini-pro
            
            if history:
                print(f"With history (last {len(history)} messages)")
                # Format the history into the correct structure for the API
                # This assumes history is a list like [{"role": "user", "parts": ["Hello"]}, ...]
                contents = []
                
                for msg in history:
                    contents.append({
                        "role": msg.get("role", "user"),
                        "parts": [{"text": part} for part in msg.get("parts", [])]
                    })
                
                # Add the current prompt to contents
                contents.append({
                    "role": "user",
                    "parts": [{"text": prompt}]
                })
                
                response = self.client.models.generate_content(
                    model=model,
                    contents=contents
                )
            else:
                # For single-turn prompts without history
                response = self.client.models.generate_content(
                    model=model,
                    contents=[prompt]
                )
            
            # Extract text from the response
            return response.text
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            # Consider more specific error handling based on Gemini API exceptions
            return f"Sorry, I encountered an error trying to reach the AI: {e}"

        # Old simulated response (remove or keep commented for reference)
        # if "who are you" in prompt.lower():
        #     return "I am a helpful AI assistant here to help you manage your contact interactions."
        # if "what information do you need" in prompt.lower():
        #     return "To get started, could you tell me a bit about this contact? For example, what\'s their primary role or how do you know them?"
        # if "last time we talked" in prompt.lower():
        #     return "I can check my records. According to my (simulated) data, your last conversation was about a project update last Tuesday."
        # return f"Gemini's simulated response to: {prompt}"

    async def handle_message(self, contact_id: str, user_message: str) -> Dict[str, Any]:
        """
        Handles an incoming message from a user for a specific contact.
        Provides short, conversational responses to help build the contact profile.
        """
        contact = self.contact_service.get_contact(contact_id)
        if not contact:
            return {"error": "Contact not found", "status_code": 404}
        
        # Construct the prompt for Gemini focused on contact profile building
        prompt_parts = []
        prompt_parts.append(f"You are a helpful assistant for enriching contact relationships. You keep responses brief and conversational.")
        prompt_parts.append(f"You are currently helping with a contact named {contact.get('name', 'this person')}.")
        
        # Add context from relevant contact fields
        if contact.get('interests'):
            prompt_parts.append(f"Known interests: {', '.join(contact.get('interests'))}")
        if contact.get('conversation_topics'):
            prompt_parts.append(f"Previous conversation topics: {', '.join(contact.get('conversation_topics'))}")
        if contact.get('important_dates'):
            dates = [f"{d.get('description')}: {d.get('date')}" for d in contact.get('important_dates')]
            prompt_parts.append(f"Important dates: {', '.join(dates)}")
        if contact.get('last_connection'):
            prompt_parts.append(f"Last connection: {contact.get('last_connection')}")
        if contact.get('relationship_type'):
            prompt_parts.append(f"Relationship type: {contact.get('relationship_type')}")
        if contact.get('preferences') and contact.get('preferences').get('likes'):
            prompt_parts.append(f"Likes: {', '.join(contact.get('preferences').get('likes'))}")
        if contact.get('preferences') and contact.get('preferences').get('dislikes'):
            prompt_parts.append(f"Dislikes: {', '.join(contact.get('preferences').get('dislikes'))}")
        
        # Add specific goals for the assistant - emphasizing brevity and conversation
        prompt_parts.append("IMPORTANT INSTRUCTIONS:")
        prompt_parts.append("1. Keep your responses brief and conversational (1-3 short sentences only).")
        prompt_parts.append("2. Ask only one follow-up question at a time to learn more about this contact.")
        prompt_parts.append("3. Focus on collecting interests, important dates, and relationship details.")
        prompt_parts.append("4. No bullet points or lists - respond like a friendly chat message.")
        prompt_parts.append("5. Extract information naturally without obvious prompting.")
        prompt_parts.append(f"The user's message is: '{user_message}'")
        
        # Final prompt assembly
        full_prompt = "\\n".join(prompt_parts)
        
        # Call the API with our contact-focused prompt
        bot_response_text = await self._call_gemini_api(prompt=full_prompt)

        # Log the interaction instead of storing conversation history
        await self._log_interaction(contact_id, user_message, bot_response_text)
        
        # Extract any potential profile data from the messages and update the contact
        extracted_data = await self._extract_profile_data(user_message, contact_id)

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
        
        # Create a brief, conversational greeting
        prompt = (
            f"You are a friendly, conversational assistant that helps remember details about contacts. "
            f"You're helping with {contact.get('name', 'this person')}. "
            f"Keep your response very brief (1-3 sentences) and conversational, like a text message from a friend. "
        )
        
        # Add minimal context
        if contact.get('interests'):
            prompt += f"Known interests: {', '.join(contact.get('interests'))}. "
        
        if profile_completeness < 50:
            prompt += (
                f"This contact's profile is quite incomplete ({profile_completeness}% complete). "
                "Ask a single, specific question that would help build the profile. "
                "Focus on interests, important dates, or relationship details. "
                "Be very casual and brief - no explanations or long sentences. "
                "Example tone: 'Hey! Does [Name] have any hobbies or interests I should know about?'"
            )
        else:
            prompt += (
                f"This contact's profile is {profile_completeness}% complete. "
                "Briefly acknowledge something we know about them and ask one follow-up question. "
                "Keep it very conversational, like texting a friend. "
                "No bullet points, no lists, and no more than 2-3 short sentences. "
                "Example tone: 'I remember [Name] likes hiking. Have they been on any interesting trails lately?'"
            )
            
        greeting_text = await self._call_gemini_api(prompt)
        
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
            'family_details', 'relationship_strength', 'recommended_contact_freq_days'
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
            try:
                # Try the update with our improved ContactService that handles errors better
                result = self.contact_service.update_contact(contact_id, update_payload)
                if result:
                    print(f"Successfully updated contact {contact_id}")
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
