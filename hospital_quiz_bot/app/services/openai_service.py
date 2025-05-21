"""
OpenAI service for the Hospital Quiz Bot.
This module provides functionality for generating reports using the OpenAI API.
"""

import re
from typing import Dict, Any, Optional

import openai

from hospital_quiz_bot.config.settings import settings
from hospital_quiz_bot.config.logging_config import logger


class OpenAIService:
    """Service for generating reports using the OpenAI API."""
    
    def __init__(self, api_key=None):
        """Initialize the OpenAI service with the API key."""
        self.api_key = api_key or settings.openai.api_key
        self.model = settings.openai.model
        self.temperature = settings.openai.temperature
        self.max_tokens = settings.openai.max_tokens
        self.top_p = settings.openai.top_p
        
        # Initialize the OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Load prompts
        self.system_message = self._load_system_message()
        self.main_prompt_template = self._load_main_prompt_template()
        self.alternative_prompt_template = self._load_alternative_prompt_template()
    
    def _load_prompt_section(self, section_marker: str) -> str:
        """Load a specific section from the prompts file."""
        try:
            with open(settings.prompts_file, "r", encoding="utf-8") as file:
                content = file.read()
                
            # Fix pattern to better match markdown sections and code blocks
            pattern = re.compile(
                rf"{re.escape(section_marker)}\s*```(.*?)```",
                re.DOTALL
            )
            match = pattern.search(content)
            
            if match:
                return match.group(1).strip()
            
            # Use a more lenient pattern if the first one fails
            pattern = re.compile(
                rf"{re.escape(section_marker)}.*?```(.*?)```",
                re.DOTALL
            )
            match = pattern.search(content)
            
            if match:
                return match.group(1).strip()
                
            logger.error(f"Could not find section {section_marker} in prompts file")
            # Return default values for critical sections
            if section_marker == "## System Message":
                return "Ти - професійний медичний асистент. Твоє завдання - складати медичні звіти."
            return ""
        except Exception as e:
            logger.error(f"Error loading prompt section: {str(e)}")
            return ""
    
    def _load_system_message(self) -> str:
        """Load the system message from the prompts file."""
        return self._load_prompt_section("## System Message")
    
    def _load_main_prompt_template(self) -> str:
        """Load the main prompt template from the prompts file."""
        return self._load_prompt_section("## Main Report Generation Prompt")
    
    def _load_alternative_prompt_template(self) -> str:
        """Load the alternative prompt template from the prompts file."""
        alt_prompt = self._load_prompt_section("## Alternative Prompt")
        # Use main prompt as fallback if alternative is not found
        if not alt_prompt and self.main_prompt_template:
            return self.main_prompt_template
        return alt_prompt
    
    def generate_report(self, patient_data: str, use_alternative=False) -> Optional[str]:
        """Generate a report using the OpenAI API."""
        try:
            # Select the appropriate prompt template
            prompt_template = self.alternative_prompt_template if use_alternative else self.main_prompt_template
            
            # If no prompt template is available, provide an error
            if not prompt_template:
                logger.error("No valid prompt template available")
                return "Помилка: Не вдалося згенерувати звіт. Налаштування шаблону відсутнє."
            
            # Replace the placeholder with the patient data
            prompt = prompt_template.replace("[PATIENT_DATA_PLACEHOLDER]", patient_data)
            
            # Generate the report
            response = self._generate_completion(prompt)
            
            return response
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return f"Помилка: Не вдалося згенерувати звіт. {str(e)}"
    
    def _generate_completion(self, prompt: str) -> str:
        """Generate a completion using the OpenAI API synchronously."""
        try:
            # Use synchronous API call based on latest OpenAI API documentation
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p
            )
            
            # Extract the content from the response - following latest API patterns
            if completion and hasattr(completion, 'choices') and len(completion.choices) > 0:
                return completion.choices[0].message.content
            
            logger.error("Invalid response format from OpenAI API")
            return "Помилка: Не вдалося згенерувати звіт. Некоректна відповідь від API."
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            raise 