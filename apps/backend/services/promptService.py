"""
Utilities for loading prompt templates from markdown files.
"""
from pathlib import Path
from typing import Dict, Optional


class PromptLoader:
    """Utility for loading prompt templates from markdown files."""
    
    def __init__(self):
        # Default to prompts directory next to this file
        self.prompts_dir = Path(__file__).parent.parent / "prompts"
        
        # Cache for loaded prompts
        self._cache: Dict[str, str] = {}
    
    def load_prompt(self, name: str) -> Optional[str]:
        """
        Load a prompt from a markdown file.
        
        Args:
            name: Name of the prompt file (without .md extension)
            
        Returns:
            The content of the prompt file, or None if not found
        """
        # Check cache first
        if name in self._cache:
            return self._cache[name]
        
        # Try to load the file
        file_path = self.prompts_dir / f"{name}.md"
        if not file_path.exists():
            print(f"Warning: Prompt '{name}' not found at '{file_path}'")
            return None
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                # Cache the content for future use
                self._cache[name] = content
                return content
        except Exception as e:
            print(f"Error loading prompt '{name}': {e}")
            return None

prompt_loader = PromptLoader()
