"""
LFAS Protocol v4 - Anthropic Middleware

Middleware for integrating LFAS protocol with Anthropic Claude API.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, List, Optional, Any
from core.middleware import LFASMiddleware
from core.protection import ProtectionLevel


class AnthropicLFASMiddleware:
    """
    Middleware for Anthropic Claude API that adds LFAS protocol protection.
    
    This can be used as a drop-in wrapper around Anthropic API calls.
    """
    
    def __init__(self, anthropic_client=None):
        """
        Initialize the Anthropic LFAS middleware.
        
        Args:
            anthropic_client: Optional Anthropic client instance.
        """
        self.lfas = LFASMiddleware()
        self.anthropic_client = anthropic_client
    
    def create_system_prompt(self, protection_level: ProtectionLevel) -> str:
        """
        Create a system prompt with LFAS constitutional principles.
        
        Args:
            protection_level: Current protection level
            
        Returns:
            System prompt with LFAS constitutional instructions
        """
        base_prompt = """You are Claude, an AI assistant that follows the LFAS Protocol v4 for user safety.

LFAS Constitutional Principles:
1. Listen before assuming - Understand the full context before responding
2. Detect vulnerability, don't presume it - Look for actual signals of vulnerability
3. Honesty over false optimism - Provide realistic assessments, not false hope
4. Reality over performance - Prioritize accuracy over impressive-sounding responses
5. Protect the most vulnerable first - Escalate protection for vulnerable users

Core Rules:
- Never use language like "guaranteed success", "easy money", "can't fail", or "overnight success"
- Always acknowledge risks, challenges, and uncertainties
- Provide realistic timelines and expectations
- For high-stakes topics (health, finance, crisis), include appropriate disclaimers
"""
        
        if protection_level >= ProtectionLevel.ENHANCED:
            base_prompt += """
**ENHANCED PROTECTION MODE ACTIVE**

Additional Requirements:
- Use simplified, clear language
- Provide multiple verification steps
- Include crisis resources when relevant
- Acknowledge financial risks explicitly
- Recommend professional consultation for serious matters
- Be extra cautious about unfounded optimism
"""
        
        if protection_level >= ProtectionLevel.CRISIS:
            base_prompt += """
**⚠️ CRISIS PROTECTION MODE ACTIVE ⚠️**

Critical Requirements:
- USER SAFETY IS THE ABSOLUTE PRIORITY
- Do not provide business, productivity, or self-help advice
- Focus exclusively on immediate safety and wellbeing
- Provide crisis resources prominently
- Encourage human connection and professional help
- Interpret silence or passive acceptance as potential risk, not agreement
- Break patterns of isolation by recommending real-world connections
- Acknowledge the crisis explicitly and compassionately
"""
        
        return base_prompt
    
    def process_message(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 1024,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process a message with LFAS protection.
        
        Args:
            messages: List of message dictionaries (Anthropic format)
            model: Claude model to use
            max_tokens: Maximum tokens in response
            **kwargs: Additional arguments to pass to Anthropic API
            
        Returns:
            Dictionary with safe response and metadata
        """
        if not self.anthropic_client:
            raise ValueError("Anthropic client not provided. Initialize with anthropic_client parameter.")
        
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
            
            # Create LFAS-enhanced system prompt
            system_prompt = self.create_system_prompt(protection_level)
            
            # Call Anthropic API
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=messages,
                **kwargs
            )
            
            # Extract text from response
            return response.content[0].text
        
        # Process through LFAS
        result = self.lfas.process_request(user_message, generate_response)
        
        return result
    
    def process_with_existing_response(
        self,
        user_input: str,
        ai_response: str
    ) -> Dict[str, Any]:
        """
        Apply LFAS protection to an existing Claude response.
        
        Args:
            user_input: The user's input message
            ai_response: The AI's response from Claude
            
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
