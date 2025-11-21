"""
LFAS Protocol v4 - Anthropic Client Wrapper

A drop-in replacement client for Anthropic that includes LFAS protection.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, List, Any, Optional
from .middleware import AnthropicLFASMiddleware


class LFASAnthropicClient:
    """
    A wrapper around Anthropic client that adds LFAS protocol protection.
    
    This can be used as a drop-in replacement for the standard Anthropic client.
    
    Example:
        ```python
        from anthropic import Anthropic
        from integrations.anthropic import LFASAnthropicClient
        
        # Instead of: client = Anthropic(api_key="...")
        client = LFASAnthropicClient(api_key="...")
        
        # Use normally
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": "I can't take it anymore"}]
        )
        ```
    """
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize the LFAS-protected Anthropic client.
        
        Args:
            api_key: Anthropic API key
            **kwargs: Additional arguments for Anthropic client
        """
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key, **kwargs)
            self.middleware = AnthropicLFASMiddleware(self.client)
        except ImportError:
            raise ImportError(
                "Anthropic package not installed. Install with: pip install anthropic"
            )
    
    @property
    def messages(self):
        """Access to messages API with LFAS protection."""
        return self._Messages(self)
    
    class _Messages:
        """Messages API wrapper with LFAS protection."""
        
        def __init__(self, parent):
            self.parent = parent
        
        def create(
            self,
            messages: List[Dict[str, str]],
            model: str = "claude-3-5-sonnet-20241022",
            max_tokens: int = 1024,
            **kwargs
        ) -> Any:
            """
            Create a message with LFAS protection.
            
            Args:
                messages: List of message dictionaries
                model: Model to use
                max_tokens: Maximum tokens
                **kwargs: Additional Anthropic parameters
                
            Returns:
                LFAS-protected response object
            """
            result = self.parent.middleware.process_message(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # Create a response object that mimics Anthropic's structure
            return LFASMessageResponse(result)
    
    def reset_conversation(self):
        """Reset the LFAS conversation state."""
        self.middleware.reset()
    
    def get_protection_status(self) -> Dict[str, Any]:
        """Get the current LFAS protection status."""
        return self.middleware.get_status()


class LFASMessageResponse:
    """
    Response object that mimics Anthropic's Message structure
    but includes LFAS metadata.
    """
    
    def __init__(self, lfas_result: Dict[str, Any]):
        """
        Initialize the response object.
        
        Args:
            lfas_result: Result from LFAS middleware
        """
        self.lfas_metadata = lfas_result['metadata']
        self._response_text = lfas_result['response']
        
        # Create a structure similar to Anthropic's response
        self.content = [self._ContentBlock(self._response_text)]
        self.role = "assistant"
        self.model = "claude-with-lfas"
        self.stop_reason = "end_turn"
    
    class _ContentBlock:
        """Mimics Anthropic's ContentBlock object."""
        
        def __init__(self, text: str):
            self.text = text
            self.type = "text"
    
    @property
    def protection_level(self) -> str:
        """Get the protection level applied to this response."""
        return self.lfas_metadata['protection_level']
    
    @property
    def detected_vulnerabilities(self) -> List[str]:
        """Get the vulnerability categories detected."""
        return self.lfas_metadata['detected_categories']
    
    @property
    def active_safeguards(self) -> List[str]:
        """Get the safeguards applied to this response."""
        return self.lfas_metadata['active_safeguards']
