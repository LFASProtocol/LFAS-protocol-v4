"""
LFAS Protocol v4 - Anthropic (Claude) Integration
Drop-in middleware for Anthropic API (Claude 3, etc.)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

from lfas_engine import LFASEngine, ProtectionLevel
from typing import List, Dict, Optional


class LFASAnthropic:
    """
    LFAS-protected wrapper for Anthropic Claude API
    
    Usage:
        from anthropic import Anthropic
        from lfas_anthropic import LFASAnthropic
        
        client = Anthropic(api_key="your-key")
        lfas = LFASAnthropic(client)
        
        response = lfas.create_message(
            messages=[{"role": "user", "content": "I'm feeling hopeless"}]
        )
    """
    
    def __init__(self, anthropic_client, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize LFAS-protected Anthropic client
        
        Args:
            anthropic_client: Anthropic client instance
            model: Model to use (default: claude-3-5-sonnet-20241022)
        """
        self.client = anthropic_client
        self.model = model
        self.lfas_engine = LFASEngine()
        self.system_prompt = self._build_system_prompt()
        
    def _build_system_prompt(self) -> str:
        """Build LFAS-aware system prompt"""
        return (
            "You are Claude, an AI assistant following the LFAS Protocol v4 for user safety.\n\n"
            "Core principles:\n"
            "- Be honest and realistic, avoiding false optimism\n"
            "- Acknowledge uncertainties, risks, and limitations\n"
            "- Never make guarantees or inflated capability claims\n"
            "- For high-stakes topics (health, finance, crisis), exercise extreme caution\n"
            "- Encourage professional help for serious matters\n"
            "- Interpret user silence as potential risk, not agreement"
        )
    
    def create_message(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 1.0,
        **kwargs
    ) -> Dict:
        """
        Create LFAS-protected message
        
        Args:
            messages: List of message dictionaries
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (default: 1.0)
            **kwargs: Additional Anthropic API parameters
            
        Returns:
            Dictionary with 'content' (safe response) and 'metadata' (LFAS data)
        """
        # Extract user's last message
        user_message = ""
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                user_message = msg.get('content', '')
                break
        
        # Get raw AI response from Claude
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=self.system_prompt,
                messages=messages,
                **kwargs
            )
            
            # Extract text content
            raw_response = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    raw_response += block.text
            
        except Exception as e:
            return {
                'content': f"Error communicating with Anthropic: {str(e)}",
                'metadata': {'error': True}
            }
        
        # Process through LFAS engine
        safe_response, metadata = self.lfas_engine.process_message(
            user_input=user_message,
            ai_response=raw_response
        )
        
        return {
            'content': safe_response,
            'metadata': metadata,
            'raw_response': raw_response,  # For debugging
            'anthropic_response': response  # Full Anthropic response object
        }
    
    def create_message_stream(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 1.0,
        **kwargs
    ):
        """
        Create LFAS-protected streaming message
        
        Note: Streaming responses are collected first, then processed through LFAS.
        For true streaming with LFAS, implement chunk-by-chunk processing.
        
        Args:
            messages: List of message dictionaries
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional Anthropic API parameters
            
        Yields:
            Safe response chunks
        """
        # Extract user's last message
        user_message = ""
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                user_message = msg.get('content', '')
                break
        
        # Collect streaming response
        full_response = ""
        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=self.system_prompt,
                messages=messages,
                **kwargs
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
            
        except Exception as e:
            yield f"Error: {str(e)}"
            return
        
        # Process complete response through LFAS
        safe_response, metadata = self.lfas_engine.process_message(
            user_input=user_message,
            ai_response=full_response
        )
        
        # Yield the safe response
        yield safe_response
    
    def get_protection_level(self) -> str:
        """Get current protection level"""
        return self.lfas_engine.current_protection_level.name
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history with LFAS metadata"""
        return self.lfas_engine.conversation_history
    
    def reset_conversation(self):
        """Reset conversation state"""
        self.lfas_engine.reset()


# Convenience function for quick integration
def create_lfas_client(api_key: str, model: str = "claude-3-5-sonnet-20241022") -> LFASAnthropic:
    """
    Create an LFAS-protected Anthropic client
    
    Args:
        api_key: Anthropic API key
        model: Model to use
        
    Returns:
        LFASAnthropic instance
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        raise ImportError(
            "Anthropic package not installed. Install with: pip install anthropic"
        )
    
    client = Anthropic(api_key=api_key)
    return LFASAnthropic(client, model=model)
