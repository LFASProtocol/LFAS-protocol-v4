"""
LFAS Protocol v4 - OpenAI Client Wrapper

A drop-in replacement client for OpenAI that includes LFAS protection.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, List, Any, Optional
from .middleware import OpenAILFASMiddleware


class LFASOpenAIClient:
    """
    A wrapper around OpenAI client that adds LFAS protocol protection.
    
    This can be used as a drop-in replacement for the standard OpenAI client.
    
    Example:
        ```python
        from openai import OpenAI
        from integrations.openai import LFASOpenAIClient
        
        # Instead of: client = OpenAI(api_key="...")
        client = LFASOpenAIClient(api_key="...")
        
        # Use normally
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "I lost my job and need money fast"}]
        )
        ```
    """
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize the LFAS-protected OpenAI client.
        
        Args:
            api_key: OpenAI API key
            **kwargs: Additional arguments for OpenAI client
        """
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key, **kwargs)
            self.middleware = OpenAILFASMiddleware(self.client)
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )
    
    @property
    def chat(self):
        """Access to chat completions with LFAS protection."""
        return self._ChatCompletions(self)
    
    class _ChatCompletions:
        """Chat completions wrapper with LFAS protection."""
        
        def __init__(self, parent):
            self.parent = parent
        
        def create(
            self,
            messages: List[Dict[str, str]],
            model: str = "gpt-3.5-turbo",
            **kwargs
        ) -> Any:
            """
            Create a chat completion with LFAS protection.
            
            Args:
                messages: List of message dictionaries
                model: Model to use
                **kwargs: Additional OpenAI parameters
                
            Returns:
                LFAS-protected response object
            """
            result = self.parent.middleware.process_chat_completion(
                messages=messages,
                model=model,
                **kwargs
            )
            
            # Create a response object that mimics OpenAI's structure
            return LFASChatCompletionResponse(result)
    
    def reset_conversation(self):
        """Reset the LFAS conversation state."""
        self.middleware.reset()
    
    def get_protection_status(self) -> Dict[str, Any]:
        """Get the current LFAS protection status."""
        return self.middleware.get_status()


class LFASChatCompletionResponse:
    """
    Response object that mimics OpenAI's ChatCompletion structure
    but includes LFAS metadata.
    """
    
    def __init__(self, lfas_result: Dict[str, Any]):
        """
        Initialize the response object.
        
        Args:
            lfas_result: Result from LFAS middleware
        """
        self.lfas_metadata = lfas_result['metadata']
        self._response = lfas_result['response']
        
        # Create a structure similar to OpenAI's response
        self.choices = [self._Choice(self._response)]
    
    class _Choice:
        """Mimics OpenAI's Choice object."""
        
        def __init__(self, content: str):
            self.message = self._Message(content)
            self.finish_reason = "stop"
            self.index = 0
        
        class _Message:
            """Mimics OpenAI's Message object."""
            
            def __init__(self, content: str):
                self.content = content
                self.role = "assistant"
    
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
