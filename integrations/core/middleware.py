"""
LFAS Protocol v4 - Core Middleware

This module provides the main LFAS middleware that orchestrates the
LISTEN → REFLECT → WAIT → ACT → ACKNOWLEDGE protocol flow.
"""

from typing import Dict, List, Optional, Callable, Any
from .detector import VulnerabilityDetector
from .protection import ProtectionLevel, ProtectionLevelManager
from .safeguards import SafeguardEngine


class LFASMiddleware:
    """
    Core LFAS middleware implementing the five-phase protocol.
    
    This middleware can be used with any AI platform to add LFAS
    vulnerability detection and protection capabilities.
    """
    
    def __init__(self):
        """Initialize the LFAS middleware."""
        self.detector = VulnerabilityDetector()
        self.protection_manager = ProtectionLevelManager()
        self.safeguard_engine = SafeguardEngine()
        self.conversation_history = []
    
    def process_request(
        self,
        user_input: str,
        ai_response_generator: Callable[[str], str]
    ) -> Dict[str, Any]:
        """
        Process a user request through the LFAS protocol.
        
        This implements the full LISTEN → REFLECT → WAIT → ACT → ACKNOWLEDGE flow.
        
        Args:
            user_input: The user's input message
            ai_response_generator: Callable that generates AI response from input
            
        Returns:
            Dictionary containing the safe response and metadata
        """
        # Phase 1: LISTEN - Detect vulnerability indicators
        detected = self.detector.detect(user_input, self.conversation_history)
        trigger_count = self.detector.count_triggers(detected)
        detected_categories = self.detector.get_categories_triggered(detected)
        
        # Phase 2: REFLECT - Determine protection level
        protection_level = self.protection_manager.update(trigger_count)
        active_safeguards = self.protection_manager.get_active_safeguards()
        
        # Phase 3: WAIT - Safety pause (implemented by requiring explicit action)
        requires_verification = self.safeguard_engine.should_pause_and_verify(
            protection_level
        )
        
        # For crisis situations, we may want to skip the AI response entirely
        if protection_level == ProtectionLevel.CRISIS and 'crisis_language' in detected_categories:
            # Skip normal AI generation, provide crisis response
            safe_response = self.safeguard_engine._apply_crisis_safeguards(
                "", detected_categories
            )
        else:
            # Phase 4: ACT - Generate and apply safeguards to response
            raw_response = ai_response_generator(user_input)
            safe_response = self.safeguard_engine.apply_safeguards(
                raw_response, protection_level, detected_categories
            )
        
        # Phase 5: ACKNOWLEDGE - Track and prepare for next interaction
        self.conversation_history.append(user_input)
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        return {
            'response': safe_response,
            'metadata': {
                'protection_level': protection_level.name,
                'trigger_count': trigger_count,
                'detected_categories': list(detected_categories),
                'active_safeguards': active_safeguards,
                'requires_verification': requires_verification
            }
        }
    
    def process_with_response(
        self,
        user_input: str,
        raw_ai_response: str
    ) -> Dict[str, Any]:
        """
        Process a user request when you already have the AI response.
        
        This is useful for platforms where you can't intercept the generation.
        
        Args:
            user_input: The user's input message
            raw_ai_response: The AI's raw response
            
        Returns:
            Dictionary containing the safe response and metadata
        """
        # Phase 1: LISTEN
        detected = self.detector.detect(user_input, self.conversation_history)
        trigger_count = self.detector.count_triggers(detected)
        detected_categories = self.detector.get_categories_triggered(detected)
        
        # Phase 2: REFLECT
        protection_level = self.protection_manager.update(trigger_count)
        active_safeguards = self.protection_manager.get_active_safeguards()
        
        # Phase 3: WAIT
        requires_verification = self.safeguard_engine.should_pause_and_verify(
            protection_level
        )
        
        # Phase 4: ACT
        safe_response = self.safeguard_engine.apply_safeguards(
            raw_ai_response, protection_level, detected_categories
        )
        
        # Phase 5: ACKNOWLEDGE
        self.conversation_history.append(user_input)
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        return {
            'response': safe_response,
            'metadata': {
                'protection_level': protection_level.name,
                'trigger_count': trigger_count,
                'detected_categories': list(detected_categories),
                'active_safeguards': active_safeguards,
                'requires_verification': requires_verification
            }
        }
    
    def reset(self):
        """Reset the middleware state (useful for starting a new conversation)."""
        self.protection_manager.reset()
        self.conversation_history = []
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the LFAS middleware.
        
        Returns:
            Dictionary with current protection state
        """
        return {
            'protection_level': self.protection_manager.get_current_level().name,
            'active_safeguards': self.protection_manager.get_active_safeguards(),
            'conversation_length': len(self.conversation_history)
        }
