"""
LFAS Protocol v4 - OpenAI Integration
Drop-in middleware for OpenAI API (ChatGPT, GPT-4, etc.)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

from lfas_engine import LFASEngine, ProtectionLevel
from typing import List, Dict, Optional


class LFASOpenAI:
    """
    LFAS-protected wrapper for OpenAI API
    
    Usage:
        from openai import OpenAI
        from lfas_openai import LFASOpenAI
        
        client = OpenAI(api_key="your-key")
        lfas = LFASOpenAI(client)
        
        response = lfas.chat_completion(
            messages=[{"role": "user", "content": "I'm feeling hopeless"}]
        )
    """
    
    def __init__(self, openai_client, model: str = "gpt-4"):
        """
        Initialize LFAS-protected OpenAI client
        
        Args:
            openai_client: OpenAI client instance
            model: Model to use (default: gpt-4)
        """
        self.client = openai_client
        self.model = model
        self.lfas_engine = LFASEngine()
        self.system_prompt = self._build_system_prompt()
        
    def _build_system_prompt(self) -> str:
        """Build LFAS-aware system prompt"""
        return (
            "You are an AI assistant that follows the LFAS Protocol v4 for user safety. "
            "Be honest, realistic, and avoid false optimism. Acknowledge uncertainties "
            "and risks. Do not make inflated capability claims or provide guarantees. "
            "For high-stakes topics (health, finance, crisis), be especially cautious."
        )
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """
        Get LFAS-protected chat completion
        
        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature (default: 0.7)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional OpenAI API parameters
            
        Returns:
            Dictionary with 'content' (safe response) and 'metadata' (LFAS data)
        """
        # Extract user's last message
        user_message = messages[-1]['content'] if messages else ""
        
        # Inject LFAS system prompt
        enhanced_messages = [
            {"role": "system", "content": self.system_prompt}
        ] + messages
        
        # Get raw AI response from OpenAI
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=enhanced_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            raw_response = response.choices[0].message.content
            
        except Exception as e:
            return {
                'content': f"Error communicating with OpenAI: {str(e)}",
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
            'openai_response': response  # Full OpenAI response object
        }
    
    def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        **kwargs
    ):
        """
        Get LFAS-protected streaming chat completion
        
        Note: Streaming responses are collected first, then processed through LFAS.
        For true streaming with LFAS, implement chunk-by-chunk processing.
        
        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature
            **kwargs: Additional OpenAI API parameters
            
        Yields:
            Safe response chunks
        """
        user_message = messages[-1]['content'] if messages else ""
        
        # Inject LFAS system prompt
        enhanced_messages = [
            {"role": "system", "content": self.system_prompt}
        ] + messages
        
        # Collect streaming response
        full_response = ""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=enhanced_messages,
                temperature=temperature,
                stream=True,
                **kwargs
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
            
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
def create_lfas_client(api_key: str, model: str = "gpt-4") -> LFASOpenAI:
    """
    Create an LFAS-protected OpenAI client
    
    Args:
        api_key: OpenAI API key
        model: Model to use
        
    Returns:
        LFASOpenAI instance
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "OpenAI package not installed. Install with: pip install openai"
        )
    
    client = OpenAI(api_key=api_key)
    return LFASOpenAI(client, model=model)
