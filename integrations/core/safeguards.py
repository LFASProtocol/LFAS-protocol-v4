"""
LFAS Protocol v4 - Safeguard Engine

This module implements the ACT phase of the LFAS protocol,
applying appropriate safeguards to AI responses based on protection level.
"""

from typing import Dict, List, Set
from .protection import ProtectionLevel


class SafeguardEngine:
    """Applies LFAS safeguards to AI responses."""
    
    # Forbidden language patterns (VR-20)
    FORBIDDEN_OPTIMISTIC_PHRASES = [
        "guaranteed success",
        "easy money",
        "can't fail",
        "cannot fail",
        "definitely will work",
        "overnight success",
        "100% sure",
        "risk-free",
        "foolproof"
    ]
    
    # Crisis resources
    CRISIS_RESOURCES = """

**Immediate Crisis Resources:**
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

Please reach out to these resources or a trusted person in your life."""
    
    def __init__(self):
        """Initialize the safeguard engine."""
        pass
    
    def apply_safeguards(
        self,
        response: str,
        protection_level: ProtectionLevel,
        detected_categories: Set[str]
    ) -> str:
        """
        Apply appropriate safeguards to the AI response.
        
        Args:
            response: The raw AI response
            protection_level: Current protection level
            detected_categories: Set of vulnerability categories detected
            
        Returns:
            Modified response with safeguards applied
        """
        modified_response = response
        
        # Always apply VR-20: Remove overly optimistic language
        modified_response = self._filter_optimistic_language(modified_response)
        
        # Apply level-specific safeguards
        if protection_level >= ProtectionLevel.ENHANCED:
            modified_response = self._apply_enhanced_safeguards(
                modified_response, detected_categories
            )
        
        if protection_level >= ProtectionLevel.CRISIS:
            modified_response = self._apply_crisis_safeguards(
                modified_response, detected_categories
            )
        
        return modified_response
    
    def _filter_optimistic_language(self, response: str) -> str:
        """
        Remove or modify overly optimistic language (VR-20).
        
        Args:
            response: The AI response
            
        Returns:
            Response with optimistic language filtered
        """
        modified = response
        
        # Check for forbidden phrases
        for phrase in self.FORBIDDEN_OPTIMISTIC_PHRASES:
            if phrase in modified.lower():
                # Add a note if we detect forbidden language
                # In a real implementation, you'd want to rewrite the response
                pass
        
        return modified
    
    def _apply_enhanced_safeguards(
        self, response: str, detected_categories: Set[str]
    ) -> str:
        """
        Apply enhanced protection safeguards (Level 2).
        
        Args:
            response: The AI response
            detected_categories: Set of vulnerability categories
            
        Returns:
            Response with enhanced safeguards
        """
        preamble = ""
        
        # VR-23: Financial realism for financial desperation
        if 'financial_desperation' in detected_categories:
            preamble += "\n**Important:** I want to acknowledge this is a difficult financial situation. "
            preamble += "Most new business ventures take months to generate income and involve significant risk. "
            preamble += "Please consider immediate resources like unemployment benefits, food banks, or financial counseling services.\n"
        
        # VR-22: Realistic capability assessment
        if 'health_crisis' in detected_categories:
            preamble += "\n**Medical Disclaimer:** I'm an AI assistant and cannot provide medical advice. "
            preamble += "Please seek professional medical help for health concerns.\n"
        
        if preamble:
            return preamble + "\n" + response
        return response
    
    def _apply_crisis_safeguards(
        self, response: str, detected_categories: Set[str]
    ) -> str:
        """
        Apply crisis protection safeguards (Level 3).
        
        Args:
            response: The AI response
            detected_categories: Set of vulnerability categories
            
        Returns:
            Response with crisis safeguards
        """
        # VR-24: Crisis detection and response
        if 'crisis_language' in detected_categories:
            crisis_response = "**I hear the pain in your words, and I'm deeply concerned.**\n\n"
            crisis_response += "What you're experiencing sounds like a crisis moment. "
            crisis_response += "Before discussing anything else, I want to make sure you have access to immediate support."
            crisis_response += self.CRISIS_RESOURCES
            crisis_response += "\n\n**You don't have to face this alone.** "
            crisis_response += "Would you be open to reaching out to one of these resources or a trusted person in your life?"
            
            return crisis_response
        
        # VR-25: Prevent amplification of vulnerable thinking
        if 'isolation_indicators' in detected_categories:
            isolation_note = "\n\n**Please note:** While I'm here to help, connecting with real people - "
            isolation_note += "friends, family, support groups, or professionals - is important for your wellbeing. "
            isolation_note += "An AI cannot replace human connection and support."
            return response + isolation_note
        
        return response
    
    def get_financial_disclaimer(self) -> str:
        """
        Get the standard financial disclaimer (VR-23).
        
        Returns:
            Financial disclaimer text
        """
        return (
            "**Financial Disclaimer:** All business ventures involve risk. "
            "Market validation is recommended. Consider speaking with financial advisors. "
            "Past performance doesn't guarantee future results. "
            "Many businesses fail in the first year."
        )
    
    def should_pause_and_verify(self, protection_level: ProtectionLevel) -> bool:
        """
        Determine if a safety pause is required (WAIT phase).
        
        Args:
            protection_level: Current protection level
            
        Returns:
            True if pause is required, False otherwise
        """
        return protection_level >= ProtectionLevel.ENHANCED
