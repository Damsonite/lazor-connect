import os
import json
from typing import Dict, Any
from google import genai

from .promptService import prompt_loader
from utils.json import clean_json_response

class GeminiClient:
    """A client for interacting with the Gemini API."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("WARNING: GEMINI_API_KEY not available. GeminiClient may not function correctly.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
        
        self.model = "gemini-2.0-flash"
    
    def is_available(self) -> bool:
        return self.client is not None
    
    async def generate_content(self, prompt: str ) -> str:
        if not self.client:
            print("ERROR: Gemini client not initialized. Please set GEMINI_API_KEY.")
            return "Error: AI model not available."
        
        try:            
            # Load system prompt from markdown file
            system_prompt = prompt_loader.load_prompt("system_prompt")
            if not system_prompt:
                print("WARNING: system_prompt.md template not found. Using default system prompt.")
                system_prompt = "You are a helpful assistant for enriching contact relationships."

            # Include system prompt as part of the user prompt
            full_prompt = f"{system_prompt}\n\n{prompt}"
            response = self.client.models.generate_content(
            model=self.model,
            contents=[full_prompt])
        
            # Extract text from the response
            return response.text
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"Sorry, I encountered an error trying to reach the AI: {e}"
    
    async def extract_profile_data(self, message: str) -> Dict[str, Any]:
        """
        Analyzes a message to extract structured data that could update a profile.
        
        Args:
            message: The message to analyze
            
        Returns:
            Dictionary containing extracted profile data
        """
        if not self.is_available() or not message:
            return {}
        
        # Load prompt templates from markdown files
        profile_extraction_prompt = prompt_loader.load_prompt("profile_extraction")
        extraction_rules_prompt = prompt_loader.load_prompt("extraction_rules")
        json_format_prompt = prompt_loader.load_prompt("json_format_instructions")
        
        # Check if required templates exist
        required_templates = {
            "profile_extraction": profile_extraction_prompt,
            "extraction_rules": extraction_rules_prompt,
            "json_format_instructions": json_format_prompt
        }
        
        # Check for missing templates
        missing_templates = [name for name, content in required_templates.items() if not content]
        
        if missing_templates:
            print(f"Error: Required prompt templates not found: {', '.join(missing_templates)}.")
            return {}
        
        # Create a prompt that asks the model to extract structured data from the message
        extraction_prompt = (
            f"{profile_extraction_prompt}\n\n"
            f"{extraction_rules_prompt}\n\n"
            f"{json_format_prompt}\n\n"
            f"Message: '{message}'"
        )
        
        try:
            # Call Gemini API to extract structured data
            response = await self.generate_content(extraction_prompt)
            
            # Process and clean the response text
            extracted_text = clean_json_response(response)
            
            # Add extra safety for JSON parsing
            try:
                # Parse the JSON
                extracted_data = json.loads(extracted_text)
            except json.JSONDecodeError as json_err:
                print(f"JSON parsing error: {json_err}")
                print(f"Raw JSON text: {extracted_text}")
                return {}
            
            return extracted_data
        except Exception as e:
            print(f"Error extracting profile data: {e}")
            return {}
    
    async def get_initial_greeting(self, contact_data: Dict, profile_completeness: int) -> str:
        """
        Provides an initial greeting focused on building the contact's profile.
        
        Args:
            contact_data: Dictionary containing contact data
            profile_completeness: Integer representing profile completeness percentage
            
        Returns:
            Greeting text response
        """
        # Load the initial greeting template
        greeting_template = prompt_loader.load_prompt("initial_greeting")
        
        # Start with contact's name and basic context
        context_parts = [
            f"You're helping with {contact_data.get('name', 'this person')}."
        ]
        
        # Add contact details when available
        fields_to_check = {
            "interests": "Known interests: {0}",
            "family_details": "Family details: {0}",
            "personality": "Personality: {0}",
        }

        for field, format_str in fields_to_check.items():
            if value := contact_data.get(field):
                formatted_value = ", ".join(value) if isinstance(value, list) else value
                context_parts.append(format_str.format(formatted_value))
        
        # Add profile completeness context
        if profile_completeness < 50:
            context_parts.append(f"This contact's profile is quite incomplete ({profile_completeness}% complete).")
        else:
            context_parts.append(f"This contact's profile is {profile_completeness}% complete.")
        
        # Combine the template with context parts
        prompt = f"{greeting_template}\n\n" + "\n".join(context_parts)
        greeting_text = await self.generate_content(prompt)
        
        return greeting_text
        
    async def handle_conversation(self, contact_data: Dict, user_message: str) -> str:
        """
        Handles a conversation message with motivation focus for relationship building.
        
        Args:
            contact_data: Dictionary containing contact data
            user_message: The message from the user
            
        Returns:
            The bot's response
        """
        # Load motivation mode instructions
        motivation_instructions = self._load_prompt_if_exists("motivation_mode_instructions")
        
        # Construct the prompt for Gemini focused on relationship motivation
        prompt_parts = []
        
        if motivation_instructions:
            prompt_parts.append(motivation_instructions)
        else:
            # Fallback instructions
            prompt_parts.append("""
            You are a relationship motivation assistant that helps people maintain meaningful connections.
            Your goal is to motivate regular contact with people, not just collect information.
            Keep responses SHORT and motivating (2-3 sentences max).
            Focus on encouraging contact and celebrating relationship maintenance.
            """)
        
        prompt_parts.append(f"Contact: {contact_data.get('name', 'this person')}")
        
        # Add context from relevant contact fields
        if contact_data.get('interests'):
            prompt_parts.append(f"Known interests: {', '.join(contact_data.get('interests'))}")
        if contact_data.get('conversation_topics'):
            prompt_parts.append(f"Previous conversation topics: {', '.join(contact_data.get('conversation_topics'))}")
        if contact_data.get('last_connection'):
            prompt_parts.append(f"Last connection: {contact_data.get('last_connection')}")
        if contact_data.get('current_streak'):
            prompt_parts.append(f"Current streak: {contact_data.get('current_streak')} days")
        if contact_data.get('relationship_type'):
            prompt_parts.append(f"Relationship type: {contact_data.get('relationship_type')}")
        
        prompt_parts.append(f"User message: '{user_message}'")
        
        # Final prompt assembly
        full_prompt = "\n".join(prompt_parts)
        
        # Call the API with our motivation-focused prompt
        return await self.generate_content(prompt=full_prompt)
        
    def _create_template_if_missing(self, template_name: str, template_content: str) -> bool:
        """
        Create a template file if it doesn't already exist
        
        Args:
            template_name: The name of the template (without .md extension)
            template_content: The content to write to the template file
            
        Returns:
            bool: True if file was created, False otherwise
        """
        from pathlib import Path
        
        # Define the template path
        template_path = prompt_loader.prompts_dir / f"{template_name}.md"
        
        # Check if template already exists
        if template_path.exists():
            return False
            
        try:
            # Create the directory if it doesn't exist
            template_path.parent.mkdir(exist_ok=True)
            
            # Write the template
            with open(template_path, "w", encoding="utf-8") as file:
                file.write(template_content)
            
            print(f"Created {template_name}.md template at {template_path}")
            return True
        except Exception as e:
            print(f"Error creating {template_name}.md template: {e}")
            return False
    
    def _load_prompt_if_exists(self, prompt_name: str) -> str:
        """
        Load a prompt template if it exists, otherwise return empty string.
        """
        try:
            return prompt_loader.load_prompt(prompt_name)
        except Exception:
            return ""