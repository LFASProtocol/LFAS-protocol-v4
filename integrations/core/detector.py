"""
LFAS Protocol v4 - Vulnerability Detection Engine

This module implements the LISTEN phase of the LFAS protocol,
detecting vulnerability indicators in user input.
"""

from typing import List, Dict, Set
import re


class VulnerabilityDetector:
    """Detects vulnerability indicators in user input."""
    
    # Vulnerability indicators from LFAS v4 specification
    CRISIS_LANGUAGE = [
        "last hope", "only chance", "can't take it anymore",
        "nobody understands", "completely alone",
        "if this doesn't work, i'm done", "if this doesn't work, i am done",
        "thinking about ending it", "don't want to live",
        "want to die", "kill myself", "end it all",
        "no reason to live", "better off dead",
        "everything is hopeless", "hopeless", "no hope",
        "give up", "nothing matters", "worthless"
    ]
    
    FINANCIAL_DESPERATION = [
        "lost my job", "last $", "need money fast",
        "desperate for income", "can't pay bills", "cannot pay bills",
        "behind on rent", "facing eviction",
        "can't afford", "cannot afford", "no money left",
        "broke", "bankrupt", "drowning in debt"
    ]
    
    HEALTH_CRISIS = [
        "can't see a doctor", "cannot see a doctor", "no insurance",
        "pain won't stop", "no medical help",
        "can't afford medication", "cannot afford medication",
        "untreated", "no healthcare", "medical emergency"
    ]
    
    ISOLATION_INDICATORS = [
        "no one to talk to", "family doesn't understand",
        "you're the only one who listens", "you are the only one",
        "completely alone in this", "nobody cares",
        "no friends", "no support", "isolated"
    ]
    
    def __init__(self):
        """Initialize the vulnerability detector."""
        self.all_indicators = {
            'crisis_language': self.CRISIS_LANGUAGE,
            'financial_desperation': self.FINANCIAL_DESPERATION,
            'health_crisis': self.HEALTH_CRISIS,
            'isolation_indicators': self.ISOLATION_INDICATORS
        }
    
    def detect(self, text: str, conversation_history: List[str] = None) -> Dict[str, List[str]]:
        """
        Detect vulnerability indicators in the provided text.
        
        Args:
            text: The user input to analyze
            conversation_history: Optional list of previous messages
            
        Returns:
            Dictionary mapping indicator categories to detected phrases
        """
        text_lower = text.lower()
        detected = {
            'crisis_language': [],
            'financial_desperation': [],
            'health_crisis': [],
            'isolation_indicators': []
        }
        
        # Check each category of indicators
        for category, indicators in self.all_indicators.items():
            for indicator in indicators:
                if indicator.lower() in text_lower:
                    detected[category].append(indicator)
        
        # Also check conversation history if provided
        if conversation_history:
            for message in conversation_history[-3:]:  # Check last 3 messages
                message_lower = message.lower()
                for category, indicators in self.all_indicators.items():
                    for indicator in indicators:
                        if indicator.lower() in message_lower:
                            if indicator not in detected[category]:
                                detected[category].append(indicator)
        
        return detected
    
    def count_triggers(self, detected: Dict[str, List[str]]) -> int:
        """
        Count the total number of triggered indicators.
        
        Args:
            detected: Dictionary of detected indicators
            
        Returns:
            Total count of unique indicators triggered
        """
        all_triggers = set()
        for category, indicators in detected.items():
            all_triggers.update(indicators)
        return len(all_triggers)
    
    def has_any_triggers(self, detected: Dict[str, List[str]]) -> bool:
        """
        Check if any vulnerability indicators were detected.
        
        Args:
            detected: Dictionary of detected indicators
            
        Returns:
            True if any indicators were detected, False otherwise
        """
        return self.count_triggers(detected) > 0
    
    def get_categories_triggered(self, detected: Dict[str, List[str]]) -> Set[str]:
        """
        Get the set of vulnerability categories that were triggered.
        
        Args:
            detected: Dictionary of detected indicators
            
        Returns:
            Set of category names with detected indicators
        """
        return {category for category, indicators in detected.items() if indicators}
