"""
LFAS Protocol v4 - Google Gemini Client Wrapper

A wrapper for Google Gemini that includes LFAS protection.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, Any, Optional, List
from .middleware import GeminiLFASMiddleware


class LFASGeminiClient:
    """
    A wrapper around Google Gemini that adds LFAS protocol protection.
    
    Example:
        ```python
        import google.generativeai as genai
        from integrations.google import LFASGeminiClient
        
        # Configure Gemini
        genai.configure(api_key="...")
        
        # Create LFAS-protected client
        client = LFASGeminiClient(model_name="gemini-pro")
        
        # Use normally
        response = client.generate_content("I lost my job and need money fast")
        print(response.text)
        ```
    """
    
    def __init__(self, model_name: str = "gemini-pro", api_key: Optional[str] = None):
        """
        Initialize the LFAS-protected Gemini client.
        
        Args:
            model_name: Gemini model name
            api_key: Optional Google API key
        """
        try:
            import google.generativeai as genai
            
            if api_key:
                genai.configure(api_key=api_key)
            
            self.model = genai.GenerativeModel(model_name)
            self.middleware = GeminiLFASMiddleware(self.model)
        except ImportError:
            raise ImportError(
                "Google Generative AI package not installed. "
                "Install with: pip install google-generativeai"
            )
    
    def generate_content(self, prompt: str, **kwargs) -> Any:
        """
        Generate content with LFAS protection.
        
        Args:
            prompt: User's prompt
            **kwargs: Additional Gemini parameters
            
        Returns:
            LFAS-protected response object
        """
        result = self.middleware.generate_content(prompt, **kwargs)
        return LFASGeminiResponse(result)
    
    def reset_conversation(self):
        """Reset the LFAS conversation state."""
        self.middleware.reset()
    
    def get_protection_status(self) -> Dict[str, Any]:
        """Get the current LFAS protection status."""
        return self.middleware.get_status()


class LFASGeminiResponse:
    """
    Response object that mimics Gemini's response structure
    but includes LFAS metadata.
    """
    
    def __init__(self, lfas_result: Dict[str, Any]):
        """
        Initialize the response object.
        
        Args:
            lfas_result: Result from LFAS middleware
        """
        self.lfas_metadata = lfas_result['metadata']
        self._text = lfas_result['response']
    
    @property
    def text(self) -> str:
        """Get the response text."""
        return self._text
    
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
    
    def __str__(self) -> str:
        """String representation returns the response text."""
        return self._text
