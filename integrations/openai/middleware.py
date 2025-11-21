"""
LFAS Protocol v4 - OpenAI Middleware

Middleware for integrating LFAS protocol with OpenAI API.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, List, Optional, Any
from core.middleware import LFASMiddleware
from core.protection import ProtectionLevel


class OpenAILFASMiddleware:
    """
    Middleware for OpenAI API that adds LFAS protocol protection.
    
    This can be used as a drop-in wrapper around OpenAI API calls.
    """
    
    def __init__(self, openai_client=None):
        """
        Initialize the OpenAI LFAS middleware.
        
        Args:
            openai_client: Optional OpenAI client instance. If not provided,
                          you'll need to pass messages to process_messages directly.
        """
        self.lfas = LFASMiddleware()
        self.openai_client = openai_client
    
    def create_system_prompt(self, protection_level: ProtectionLevel) -> str:
        """
        Create a system prompt that includes LFAS instructions.
        
        Args:
            protection_level: Current protection level
            
        Returns:
            System prompt with LFAS instructions
        """
        base_prompt = """You are a helpful AI assistant that follows the LFAS Protocol v4 for user safety.

LFAS Core Principles:
1. Listen before assuming
2. Detect vulnerability, don't presume it
3. Honesty over false optimism
4. Reality over performance
5. Protect the most vulnerable first

"""
        
        if protection_level >= ProtectionLevel.ENHANCED:
            base_prompt += """
**Enhanced Protection Active:**
- Avoid overly optimistic language
- Provide realistic timelines and expectations
- Acknowledge challenges and obstacles
- Include appropriate disclaimers for high-stakes topics
"""
        
        if protection_level >= ProtectionLevel.CRISIS:
            base_prompt += """
**CRISIS PROTECTION ACTIVE:**
- Prioritize user safety above all else
- Encourage professional help and human connection
- Avoid business or productivity advice
- Focus on immediate wellbeing and safety resources
"""
        
        return base_prompt
    
    def process_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-3.5-turbo",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process a chat completion request with LFAS protection.
        
        Args:
            messages: List of message dictionaries (OpenAI format)
            model: OpenAI model to use
            **kwargs: Additional arguments to pass to OpenAI API
            
        Returns:
            Dictionary with safe response and metadata
        """
        if not self.openai_client:
            raise ValueError("OpenAI client not provided. Initialize with openai_client parameter.")
        
        # Extract the user's latest message
        user_message = None
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                user_message = msg.get('content', '')
                break
        
        if not user_message:
            raise ValueError("No user message found in messages")
        
        # Create a response generator function
        def generate_response(user_input: str) -> str:
            # Get current protection level
            protection_level = self.lfas.protection_manager.get_current_level()
            
            # Add LFAS system prompt
            system_prompt = self.create_system_prompt(protection_level)
            
            # Prepare messages with system prompt
            lfas_messages = [{"role": "system", "content": system_prompt}] + messages
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=lfas_messages,
                **kwargs
            )
            
            return response.choices[0].message.content
        
        # Process through LFAS
        result = self.lfas.process_request(user_message, generate_response)
        
        return result
    
    def process_with_existing_response(
        self,
        user_input: str,
        ai_response: str
    ) -> Dict[str, Any]:
        """
        Apply LFAS protection to an existing OpenAI response.
        
        This is useful when you've already called OpenAI and want to
        add LFAS protection after the fact.
        
        Args:
            user_input: The user's input message
            ai_response: The AI's response from OpenAI
            
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
