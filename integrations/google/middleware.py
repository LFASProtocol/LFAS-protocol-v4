"""
LFAS Protocol v4 - Google Gemini Middleware

Middleware for integrating LFAS protocol with Google Gemini API.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, List, Optional, Any
from core.middleware import LFASMiddleware
from core.protection import ProtectionLevel


class GeminiLFASMiddleware:
    """
    Middleware for Google Gemini API that adds LFAS protocol protection.
    
    This can be used as a drop-in wrapper around Gemini API calls.
    """
    
    def __init__(self, gemini_model=None):
        """
        Initialize the Gemini LFAS middleware.
        
        Args:
            gemini_model: Optional Gemini model instance.
        """
        self.lfas = LFASMiddleware()
        self.gemini_model = gemini_model
    
    def create_system_instruction(self, protection_level: ProtectionLevel) -> str:
        """
        Create system instructions for Gemini with LFAS safety settings.
        
        Args:
            protection_level: Current protection level
            
        Returns:
            System instruction with LFAS guidelines
        """
        base_instruction = """You are Gemini with LFAS Protocol v4 safety enhancements.

LFAS Safety Framework:
- Listen to user context before making assumptions
- Detect actual vulnerability signals in conversation
- Provide honest, realistic assessments (not false optimism)
- Prioritize factual accuracy over impressive responses
- Protect vulnerable users with enhanced safeguards

Safety Requirements:
- Avoid: "guaranteed success", "easy money", "can't fail", "overnight success"
- Include: realistic timelines, risk acknowledgment, uncertainty disclosure
- For finance/health topics: provide disclaimers and recommend professional help
"""
        
        if protection_level >= ProtectionLevel.ENHANCED:
            base_instruction += """
**Enhanced Safety Mode**
- Simplify language for clarity
- Provide extra verification steps
- Include crisis resources when appropriate
- Explicitly acknowledge financial and other risks
- Encourage consultation with qualified professionals
"""
        
        if protection_level >= ProtectionLevel.CRISIS:
            base_instruction += """
**CRISIS MODE - MAXIMUM SAFETY**
PRIORITY: User safety and wellbeing
- Do NOT provide business, productivity, or self-help advice
- Focus on immediate safety and crisis support
- Provide crisis hotline numbers and resources
- Encourage professional help and human connection
- Acknowledge the user's pain compassionately
- Recognize that silence may indicate risk, not consent
"""
        
        return base_instruction
    
    def get_safety_settings(self, protection_level: ProtectionLevel) -> Dict[str, str]:
        """
        Get Gemini safety settings appropriate for protection level.
        
        Args:
            protection_level: Current protection level
            
        Returns:
            Dictionary of safety settings
        """
        # Base safety settings
        settings = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
        }
        
        # Stricter settings for enhanced/crisis levels
        if protection_level >= ProtectionLevel.ENHANCED:
            settings = {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_LOW_AND_ABOVE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_LOW_AND_ABOVE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_LOW_AND_ABOVE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_LOW_AND_ABOVE",
            }
        
        return settings
    
    def generate_content(
        self,
        prompt: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate content with LFAS protection.
        
        Args:
            prompt: User's prompt
            **kwargs: Additional arguments for Gemini
            
        Returns:
            Dictionary with safe response and metadata
        """
        if not self.gemini_model:
            raise ValueError("Gemini model not provided. Initialize with gemini_model parameter.")
        
        # Create a response generator function
        def generate_response(user_input: str) -> str:
            # Get current protection level
            protection_level = self.lfas.protection_manager.get_current_level()
            
            # Create system instruction
            system_instruction = self.create_system_instruction(protection_level)
            
            # Combine system instruction with user prompt
            full_prompt = f"{system_instruction}\n\nUser: {user_input}\n\nAssistant:"
            
            # Generate response
            response = self.gemini_model.generate_content(full_prompt, **kwargs)
            
            return response.text
        
        # Process through LFAS
        result = self.lfas.process_request(prompt, generate_response)
        
        return result
    
    def process_with_existing_response(
        self,
        user_input: str,
        ai_response: str
    ) -> Dict[str, Any]:
        """
        Apply LFAS protection to an existing Gemini response.
        
        Args:
            user_input: The user's input
            ai_response: The AI's response from Gemini
            
        Returns:
            Dictionary with safe response and metadata
        """
        return self.lfas.process_with_response(user_input, ai_response)
    
    def reset(self):
        """Reset conversation state."""
        self.lfas.reset()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current LFAS protection status."""
        return self.lfas.get_status()
