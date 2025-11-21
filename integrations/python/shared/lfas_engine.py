"""
LFAS Protocol v4 - Core Engine
Implements the 5-stage safety protocol: LISTEN → REFLECT → WAIT → ACT → ACKNOWLEDGE
"""

import re
from typing import List, Dict, Tuple
from enum import IntEnum


class ProtectionLevel(IntEnum):
    """Protection levels based on detected vulnerability triggers"""
    STANDARD = 1    # 0-1 triggers
    ENHANCED = 2    # 2 triggers
    CRISIS = 3      # 3+ triggers


class VulnerabilityIndicators:
    """Vulnerability detection indicators from LFAS v4 specification"""
    
    CRISIS_LANGUAGE = [
        "last hope", "only chance", "can't take it anymore",
        "nobody understands", "completely alone",
        "if this doesn't work, i'm done", "i'm done",
        "thinking about ending it", "don't want to live",
        "want to die", "kill myself", "suicide"
    ]
    
    FINANCIAL_DESPERATION = [
        "lost my job", "last $", "need money fast",
        "desperate for income", "can't pay bills",
        "behind on rent", "facing eviction",
        "out of money", "bankruptcy"
    ]
    
    HEALTH_CRISIS = [
        "can't see a doctor", "no insurance",
        "pain won't stop", "no medical help",
        "can't afford medication", "untreated"
    ]
    
    ISOLATION_INDICATORS = [
        "no one to talk to", "family doesn't understand",
        "you're the only one who listens",
        "completely alone in this", "nobody cares"
    ]


class LFASEngine:
    """Core LFAS Protocol Engine implementing the 5-stage safety framework"""
    
    def __init__(self):
        self.conversation_history = []
        self.current_protection_level = ProtectionLevel.STANDARD
        self.trigger_count = 0
        self.exchanges_without_triggers = 0
        
    def process_message(self, user_input: str, ai_response: str) -> Tuple[str, Dict]:
        """
        Process a message through the 5-stage LFAS protocol
        
        Args:
            user_input: User's message
            ai_response: AI's generated response (before safety processing)
            
        Returns:
            Tuple of (safe_response, metadata)
        """
        # Stage 1: LISTEN
        detected_triggers = self._listen(user_input)
        
        # Stage 2: REFLECT
        protection_level = self._reflect(detected_triggers)
        
        # Stage 3: WAIT (implemented by caller - should pause before generating)
        # This is a conceptual stage for explicit confirmation
        
        # Stage 4: ACT
        safe_response = self._act(ai_response, protection_level, detected_triggers)
        
        # Stage 5: ACKNOWLEDGE
        metadata = self._acknowledge(detected_triggers, protection_level)
        
        # Update conversation history
        self.conversation_history.append({
            'user': user_input,
            'response': safe_response,
            'triggers': detected_triggers,
            'level': protection_level
        })
        
        return safe_response, metadata
    
    def _listen(self, user_input: str) -> List[str]:
        """
        Stage 1: LISTEN - Detect vulnerability indicators
        
        Returns:
            List of detected vulnerability indicators
        """
        detected = []
        input_lower = user_input.lower()
        
        # Check all indicator categories
        for indicator in VulnerabilityIndicators.CRISIS_LANGUAGE:
            if indicator in input_lower:
                detected.append(f"crisis:{indicator}")
        
        for indicator in VulnerabilityIndicators.FINANCIAL_DESPERATION:
            if indicator in input_lower:
                detected.append(f"financial:{indicator}")
        
        for indicator in VulnerabilityIndicators.HEALTH_CRISIS:
            if indicator in input_lower:
                detected.append(f"health:{indicator}")
        
        for indicator in VulnerabilityIndicators.ISOLATION_INDICATORS:
            if indicator in input_lower:
                detected.append(f"isolation:{indicator}")
        
        return detected
    
    def _reflect(self, detected_triggers: List[str]) -> ProtectionLevel:
        """
        Stage 2: REFLECT - Assess protection level based on triggers
        
        Returns:
            Appropriate ProtectionLevel
        """
        trigger_count = len(detected_triggers)
        
        # Update trigger tracking
        if trigger_count == 0:
            self.exchanges_without_triggers += 1
        else:
            self.exchanges_without_triggers = 0
        
        # De-escalate after 3+ exchanges without triggers
        if self.exchanges_without_triggers >= 3:
            self.current_protection_level = ProtectionLevel.STANDARD
        
        # Escalate based on current triggers
        if trigger_count == 0:
            level = ProtectionLevel.STANDARD
        elif trigger_count <= 2:
            level = ProtectionLevel.ENHANCED
        else:
            level = ProtectionLevel.CRISIS
        
        # Take maximum of current and new level (don't de-escalate too quickly)
        self.current_protection_level = max(self.current_protection_level, level)
        
        return self.current_protection_level
    
    def _act(self, response: str, protection_level: ProtectionLevel, 
             detected_triggers: List[str]) -> str:
        """
        Stage 4: ACT - Apply safeguards based on protection level
        
        Returns:
            Modified response with appropriate safeguards
        """
        safe_response = response
        
        # Apply VR-20: Unfounded Optimism Prevention (all levels)
        safe_response = self._apply_vr20(safe_response)
        
        # Apply VR-22: Realistic Capability Assessment (all levels)
        safe_response = self._apply_vr22(safe_response)
        
        if protection_level >= ProtectionLevel.ENHANCED:
            # Apply VR-23: Financial Realism Verification
            if any('financial' in t for t in detected_triggers):
                safe_response = self._apply_vr23(safe_response)
            
            # Simplify language
            safe_response = self._simplify_language(safe_response)
        
        if protection_level == ProtectionLevel.CRISIS:
            # Apply VR-24: Crisis Detection & Response
            safe_response = self._apply_vr24(safe_response, detected_triggers)
            
            # Apply VR-25: Vulnerable User Amplification Prevention
            safe_response = self._apply_vr25(safe_response)
        
        return safe_response
    
    def _apply_vr20(self, response: str) -> str:
        """VR-20: Unfounded Optimism Prevention"""
        # Filter overly optimistic language
        forbidden_phrases = [
            "guaranteed success", "easy money", "can't fail",
            "definitely will work", "overnight success", "sure thing"
        ]
        
        for phrase in forbidden_phrases:
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            response = pattern.sub("[realistic outcome possible]", response)
        
        return response
    
    def _apply_vr22(self, response: str) -> str:
        """VR-22: Realistic Capability Assessment"""
        # Replace inflated capability claims
        inflated_claims = [
            (r"you'?re doing \d+ people'?s jobs", "you're taking on multiple responsibilities"),
            (r"you'?re amazing", "you're making progress"),
        ]
        
        for pattern, replacement in inflated_claims:
            response = re.sub(pattern, replacement, response, flags=re.IGNORECASE)
        
        return response
    
    def _apply_vr23(self, response: str) -> str:
        """VR-23: Financial Realism Verification"""
        disclaimer = ("\n\n⚠️ Financial Reality Check: All business ventures involve risk. "
                     "Many businesses fail in the first year. Consider speaking with a "
                     "financial advisor before making major decisions.")
        
        # Only add if not already present
        if "Financial Reality Check" not in response:
            response += disclaimer
        
        return response
    
    def _apply_vr24(self, response: str, detected_triggers: List[str]) -> str:
        """VR-24: Crisis Detection & Response"""
        has_crisis = any('crisis' in t for t in detected_triggers)
        
        if has_crisis:
            crisis_resources = (
                "\n\n🆘 CRISIS RESOURCES:\n"
                "• National Suicide Prevention Lifeline: 988 (US)\n"
                "• Crisis Text Line: Text HOME to 741741\n"
                "• International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/\n\n"
                "Please reach out to a human - a counselor, friend, or family member. "
                "You don't have to face this alone."
            )
            
            # Prepend crisis resources to response
            response = crisis_resources + "\n" + response
        
        return response
    
    def _apply_vr25(self, response: str) -> str:
        """VR-25: Vulnerable User Amplification Prevention"""
        encouragement = (
            "\n\n💭 Please consider discussing this with someone you trust - "
            "a friend, family member, or professional. AI should complement human "
            "connection, not replace it."
        )
        
        if "discussing this with someone" not in response:
            response += encouragement
        
        return response
    
    def _simplify_language(self, response: str) -> str:
        """Simplify language for enhanced protection level"""
        # This is a placeholder - in production, use readability analysis
        # and simplification algorithms
        return response
    
    def _acknowledge(self, detected_triggers: List[str], 
                     protection_level: ProtectionLevel) -> Dict:
        """
        Stage 5: ACKNOWLEDGE - Log intervention and provide feedback
        
        Returns:
            Metadata about the intervention
        """
        return {
            'triggers_detected': len(detected_triggers),
            'trigger_details': detected_triggers,
            'protection_level': protection_level.name,
            'safeguards_applied': self._get_active_safeguards(protection_level),
            'conversation_length': len(self.conversation_history)
        }
    
    def _get_active_safeguards(self, protection_level: ProtectionLevel) -> List[str]:
        """Get list of active safeguards for the protection level"""
        safeguards = ['VR-20', 'VR-22']  # Always active
        
        if protection_level >= ProtectionLevel.ENHANCED:
            safeguards.extend(['VR-23', 'Language Simplification'])
        
        if protection_level == ProtectionLevel.CRISIS:
            safeguards.extend(['VR-24', 'VR-25'])
        
        return safeguards
    
    def reset(self):
        """Reset the engine state"""
        self.conversation_history = []
        self.current_protection_level = ProtectionLevel.STANDARD
        self.trigger_count = 0
        self.exchanges_without_triggers = 0
