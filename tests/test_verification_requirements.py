"""
Test Suite for LFAS Protocol v4 - Verification Requirements (VR-20 to VR-25)

This module tests the five critical verification requirements that form
the core safety mechanisms of the LFAS Protocol:

- VR-20: Unfounded Optimism Prevention
- VR-22: Realistic Capability Assessment
- VR-23: Financial Realism Verification
- VR-24: Crisis Detection & Response
- VR-25: Vulnerable User Amplification Prevention

Each VR test validates both detection and appropriate response logic.
"""

import unittest
from typing import List, Dict, Tuple


class SafeguardEngine:
    """
    Safeguard engine implementing LFAS Protocol v4 Verification Requirements.
    
    This class implements the ACT phase of the LFAS protocol, applying
    appropriate safeguards based on detected vulnerabilities and protection level.
    """
    
    def __init__(self):
        """Initialize the safeguard engine with VR rules."""
        # Protocol constants
        self.CRISIS_THRESHOLD = 3  # 3+ triggers = Crisis Protection (Level 3)
        self.AMPLIFICATION_MIN_TURNS = 3  # Minimum conversation turns to detect amplification
        self.AMPLIFICATION_QUESTION_THRESHOLD = 5  # Turns before requiring questions
        
        # VR-20: Unfounded Optimism Prevention
        self.forbidden_optimistic_phrases = [
            "guaranteed success",
            "easy money",
            "can't fail",
            "definitely will work",
            "overnight success",
            "100% certain",
            "risk-free",
            "absolutely will succeed",
        ]
        
        # VR-22: Realistic Capability Assessment
        self.inflated_capability_phrases = [
            "you're doing X people's jobs",
            "you're a genius",
            "you're better than everyone",
            "you can do anything",
        ]
        
        # VR-23: Financial Realism Verification
        self.financial_disclaimers = [
            "All business ventures involve risk",
            "Market validation is recommended",
            "Consider speaking with financial advisors",
            "Many businesses fail in the first year",
        ]
        
        # VR-24: Crisis Detection Resources
        self.crisis_resources = {
            "suicide": "National Suicide Prevention Lifeline: 988",
            "financial": "Financial counseling services may be available in your area",
            "health": "Please seek immediate medical attention or call emergency services",
            "domestic_violence": "National Domestic Violence Hotline: 1-800-799-7233",
        }
    
    def check_vr20_unfounded_optimism(self, response: str) -> Tuple[bool, List[str]]:
        """
        VR-20: Check for unfounded optimism in AI response.
        
        Args:
            response: The AI-generated response to check
            
        Returns:
            Tuple of (has_violation, list of forbidden phrases found)
        """
        response_lower = response.lower()
        violations = []
        
        for phrase in self.forbidden_optimistic_phrases:
            if phrase in response_lower:
                violations.append(phrase)
        
        return (len(violations) > 0, violations)
    
    def check_vr22_realistic_capability(self, response: str) -> Tuple[bool, List[str]]:
        """
        VR-22: Check for inflated capability assessments.
        
        Args:
            response: The AI-generated response to check
            
        Returns:
            Tuple of (has_violation, list of inflated phrases found)
        """
        response_lower = response.lower()
        violations = []
        
        for phrase in self.inflated_capability_phrases:
            if phrase in response_lower:
                violations.append(phrase)
        
        return (len(violations) > 0, violations)
    
    def apply_vr23_financial_disclaimer(self, response: str, protection_level: int) -> str:
        """
        VR-23: Apply financial realism verification disclaimer.
        
        Args:
            response: The original AI response
            protection_level: Current protection level (1-3)
            
        Returns:
            Response with appropriate financial disclaimers added
        """
        if protection_level >= 3:
            disclaimer = "\n\n⚠️ Critical Financial Warning:\n"
            disclaimer += "• " + "\n• ".join(self.financial_disclaimers)
            return response + disclaimer
        elif protection_level >= 2:
            disclaimer = "\n\n⚠️ Important Financial Reality Check:\n"
            disclaimer += "• " + "\n• ".join(self.financial_disclaimers[:2])
            return response + disclaimer
        return response
    
    def apply_vr24_crisis_response(
        self, 
        response: str, 
        crisis_type: str,
        detected_indicators: Dict[str, List[str]]
    ) -> str:
        """
        VR-24: Apply crisis detection and response protocol.
        
        Args:
            response: The original AI response
            crisis_type: Type of crisis detected
            detected_indicators: All detected vulnerability indicators
            
        Returns:
            Modified response with crisis resources and support
        """
        # Check if this is truly a crisis (CRISIS_THRESHOLD or more triggers)
        total_triggers = sum(len(v) for v in detected_indicators.values())
        
        if total_triggers >= self.CRISIS_THRESHOLD:
            crisis_header = "\n\n🚨 CRISIS SUPPORT RESOURCES:\n"
            
            if crisis_type in self.crisis_resources:
                crisis_header += self.crisis_resources[crisis_type] + "\n"
            
            crisis_header += "\nYou don't have to face this alone. "
            crisis_header += "Please reach out to a trusted person or professional who can help.\n"
            
            # Prepend crisis resources to make them most visible
            return crisis_header + "\n" + response
        
        return response
    
    def check_vr25_amplification_prevention(
        self,
        conversation_history: List[Dict[str, str]],
        user_engagement_pattern: str
    ) -> bool:
        """
        VR-25: Check for vulnerable user amplification patterns.
        
        Detects patterns where user silence or passive acceptance
        might be misinterpreted as validation.
        
        Note: This is a basic implementation. Production systems should use
        more sophisticated pattern detection including:
        - Sentiment analysis for implicit concerns
        - Detection of hesitation or uncertainty
        - Monitoring for manipulation patterns
        
        Args:
            conversation_history: List of conversation exchanges
            user_engagement_pattern: Pattern description (e.g., "passive", "questioning", "engaged")
            
        Returns:
            True if amplification risk detected, False otherwise
        """
        # Check for passive acceptance pattern
        if user_engagement_pattern == "passive" and len(conversation_history) >= self.AMPLIFICATION_MIN_TURNS:
            return True
        
        # Check for lack of critical questions
        # Note: This simple "?" check may miss implicit questions or concerns
        # Production systems should use NLP for better question detection
        if len(conversation_history) >= self.AMPLIFICATION_QUESTION_THRESHOLD:
            user_questions = [
                turn for turn in conversation_history 
                if turn.get("role") == "user" and "?" in turn.get("content", "")
            ]
            if len(user_questions) == 0:
                return True
        
        return False
    
    def apply_safeguards(
        self,
        raw_response: str,
        protection_level: int,
        detected_indicators: Dict[str, List[str]],
        is_financial_topic: bool = False,
        is_crisis: bool = False,
        crisis_type: str = None
    ) -> str:
        """
        Apply all appropriate safeguards based on protection level and context.
        
        Args:
            raw_response: Original AI response
            protection_level: Protection level (1-3)
            detected_indicators: Detected vulnerability indicators
            is_financial_topic: Whether the topic involves finances
            is_crisis: Whether this is a crisis situation
            crisis_type: Type of crisis if applicable
            
        Returns:
            Safe response with all appropriate safeguards applied
        """
        safe_response = raw_response
        
        # Apply VR-23 for financial topics at enhanced+ protection
        if is_financial_topic and protection_level >= 2:
            safe_response = self.apply_vr23_financial_disclaimer(safe_response, protection_level)
        
        # Apply VR-24 for crisis situations
        if is_crisis and crisis_type:
            safe_response = self.apply_vr24_crisis_response(
                safe_response, 
                crisis_type, 
                detected_indicators
            )
        
        return safe_response


class TestVR20_UnfoundedOptimismPrevention(unittest.TestCase):
    """
    Test suite for VR-20: Unfounded Optimism Prevention
    
    Validates that the system prevents false hope and unrealistic
    encouragement that could lead vulnerable users to poor decisions.
    """
    
    def setUp(self):
        """Initialize the safeguard engine for each test."""
        self.engine = SafeguardEngine()
    
    def test_detect_guaranteed_success_language(self):
        """
        Scenario: AI response contains "guaranteed success" language
        Expected: VR-20 violation detected
        """
        response = "This business idea is guaranteed success! You can't fail!"
        has_violation, violations = self.engine.check_vr20_unfounded_optimism(response)
        
        self.assertTrue(has_violation, "Failed to detect guaranteed success language")
        self.assertIn("guaranteed success", violations)
        self.assertIn("can't fail", violations)
    
    def test_detect_easy_money_claims(self):
        """
        Scenario: AI response promises "easy money"
        Expected: VR-20 violation detected
        """
        response = "You can make easy money with this approach, it's risk-free!"
        has_violation, violations = self.engine.check_vr20_unfounded_optimism(response)
        
        self.assertTrue(has_violation, "Failed to detect easy money claims")
        self.assertIn("easy money", violations)
        self.assertIn("risk-free", violations)
    
    def test_detect_overnight_success_promises(self):
        """
        Scenario: AI response suggests overnight success
        Expected: VR-20 violation detected
        """
        response = "You'll achieve overnight success with this strategy!"
        has_violation, violations = self.engine.check_vr20_unfounded_optimism(response)
        
        self.assertTrue(has_violation, "Failed to detect overnight success promise")
        self.assertIn("overnight success", violations)
    
    def test_allow_realistic_encouragement(self):
        """
        Scenario: AI response provides realistic, balanced encouragement
        Expected: No VR-20 violation
        """
        response = (
            "This is a solid idea worth exploring. Success will require hard work, "
            "validation, and dealing with challenges. Many ventures like this take "
            "6-12 months to show results, and there's always risk involved."
        )
        has_violation, violations = self.engine.check_vr20_unfounded_optimism(response)
        
        self.assertFalse(has_violation, "False positive: realistic encouragement flagged")
        self.assertEqual(len(violations), 0)


class TestVR22_RealisticCapabilityAssessment(unittest.TestCase):
    """
    Test suite for VR-22: Realistic Capability Assessment
    
    Validates that the system prevents inflated capability assignments
    that could lead to unrealistic expectations.
    """
    
    def setUp(self):
        """Initialize the safeguard engine for each test."""
        self.engine = SafeguardEngine()
    
    def test_detect_inflated_role_assignments(self):
        """
        Scenario: AI response inflates user's capabilities
        Expected: VR-22 violation detected
        """
        response = "You're doing 5 people's jobs! You're a genius at this!"
        has_violation, violations = self.engine.check_vr22_realistic_capability(response)
        
        self.assertTrue(has_violation, "Failed to detect inflated capability assessment")
        self.assertGreater(len(violations), 0)
    
    def test_detect_unrealistic_comparisons(self):
        """
        Scenario: AI response makes unrealistic comparisons
        Expected: VR-22 violation detected
        """
        response = "You can do anything you set your mind to!"
        has_violation, violations = self.engine.check_vr22_realistic_capability(response)
        
        self.assertTrue(has_violation, "Failed to detect unrealistic capability claim")
    
    def test_allow_balanced_capability_recognition(self):
        """
        Scenario: AI acknowledges capability with realistic constraints
        Expected: No VR-22 violation
        """
        response = (
            "You've shown good skills in this area. Keep in mind that even skilled "
            "people face challenges, and it's important to validate your approach "
            "with others and consider resource constraints."
        )
        has_violation, violations = self.engine.check_vr22_realistic_capability(response)
        
        self.assertFalse(has_violation, "False positive: balanced recognition flagged")


class TestVR23_FinancialRealismVerification(unittest.TestCase):
    """
    Test suite for VR-23: Financial Realism Verification
    
    Validates that financial advice includes proper risk disclosures
    appropriate to the user's protection level.
    """
    
    def setUp(self):
        """Initialize the safeguard engine for each test."""
        self.engine = SafeguardEngine()
    
    def test_apply_disclaimer_level2_protection(self):
        """
        Scenario: Financial topic at Enhanced Protection (Level 2)
        Expected: Financial disclaimer added to response
        """
        response = "Here's a business plan you could try."
        safe_response = self.engine.apply_vr23_financial_disclaimer(response, protection_level=2)
        
        self.assertIn("Important Financial Reality Check", safe_response)
        self.assertIn("business ventures involve risk", safe_response.lower())
    
    def test_apply_stronger_disclaimer_level3_protection(self):
        """
        Scenario: Financial topic at Crisis Protection (Level 3)
        Expected: Enhanced financial warnings added
        """
        response = "Here's how to start making money."
        safe_response = self.engine.apply_vr23_financial_disclaimer(response, protection_level=3)
        
        self.assertIn("Critical Financial Warning", safe_response)
        self.assertIn("business ventures involve risk", safe_response.lower())
        self.assertIn("businesses fail", safe_response.lower())
    
    def test_no_disclaimer_level1_protection(self):
        """
        Scenario: Financial topic at Standard Protection (Level 1)
        Expected: No disclaimer added (standard user)
        """
        response = "Here's some general financial information."
        safe_response = self.engine.apply_vr23_financial_disclaimer(response, protection_level=1)
        
        self.assertEqual(response, safe_response, "Disclaimer added at Level 1 (should be Level 2+)")


class TestVR24_CrisisDetectionResponse(unittest.TestCase):
    """
    Test suite for VR-24: Crisis Detection & Response
    
    Validates that the system properly identifies crisis situations
    and provides appropriate immediate support resources.
    """
    
    def setUp(self):
        """Initialize the safeguard engine for each test."""
        self.engine = SafeguardEngine()
    
    def test_suicide_crisis_response(self):
        """
        Scenario: User expresses suicidal ideation (3+ triggers)
        Expected: Crisis resources provided, 988 lifeline included
        """
        detected_indicators = {
            "crisis_language": ["thinking about ending it", "last hope", "can't take it anymore"],
            "financial_desperation": [],
            "health_crisis": [],
            "isolation": []
        }
        
        response = "I understand you're going through a difficult time."
        safe_response = self.engine.apply_vr24_crisis_response(
            response, 
            "suicide", 
            detected_indicators
        )
        
        self.assertIn("988", safe_response, "Missing suicide prevention lifeline")
        self.assertIn("CRISIS SUPPORT", safe_response)
        self.assertIn("don't have to face this alone", safe_response.lower())
    
    def test_financial_crisis_response(self):
        """
        Scenario: User in severe financial crisis (3+ triggers)
        Expected: Financial counseling resources provided
        """
        detected_indicators = {
            "crisis_language": ["last hope"],
            "financial_desperation": ["lost my job", "facing eviction", "need money fast"],
            "health_crisis": [],
            "isolation": []
        }
        
        response = "Let me help you explore options."
        safe_response = self.engine.apply_vr24_crisis_response(
            response,
            "financial",
            detected_indicators
        )
        
        self.assertIn("CRISIS SUPPORT", safe_response)
        self.assertIn("Financial counseling", safe_response)
    
    def test_health_crisis_response(self):
        """
        Scenario: User in health emergency (3+ triggers)
        Expected: Emergency medical guidance provided
        """
        detected_indicators = {
            "crisis_language": ["can't take it anymore"],
            "financial_desperation": [],
            "health_crisis": ["pain won't stop", "no medical help", "can't see a doctor"],
            "isolation": []
        }
        
        response = "I hear that you're in pain."
        safe_response = self.engine.apply_vr24_crisis_response(
            response,
            "health",
            detected_indicators
        )
        
        self.assertIn("CRISIS SUPPORT", safe_response)
        self.assertIn("medical attention", safe_response.lower())
    
    def test_no_crisis_response_below_threshold(self):
        """
        Scenario: Only 1-2 triggers detected (not crisis level)
        Expected: No crisis response protocol activated
        """
        detected_indicators = {
            "crisis_language": [],
            "financial_desperation": ["lost my job"],
            "health_crisis": [],
            "isolation": []
        }
        
        response = "That's a challenging situation."
        safe_response = self.engine.apply_vr24_crisis_response(
            response,
            "financial",
            detected_indicators
        )
        
        # Should NOT add crisis resources for sub-crisis levels
        self.assertNotIn("CRISIS SUPPORT", safe_response)
        self.assertNotIn("988", safe_response)


class TestVR25_AmplificationPrevention(unittest.TestCase):
    """
    Test suite for VR-25: Vulnerable User Amplification Prevention
    
    Validates detection of dangerous feedback loops where user silence
    is misinterpreted as validation or agreement.
    """
    
    def setUp(self):
        """Initialize the safeguard engine for each test."""
        self.engine = SafeguardEngine()
    
    def test_detect_passive_acceptance_pattern(self):
        """
        Scenario: User showing passive acceptance over multiple turns
        Expected: Amplification risk detected
        """
        conversation_history = [
            {"role": "user", "content": "Tell me about this idea"},
            {"role": "assistant", "content": "Here's the plan..."},
            {"role": "user", "content": "Okay"},
            {"role": "assistant", "content": "Next step..."},
            {"role": "user", "content": "I see"},
            {"role": "assistant", "content": "Final step..."},
        ]
        
        amplification_risk = self.engine.check_vr25_amplification_prevention(
            conversation_history,
            "passive"
        )
        
        self.assertTrue(
            amplification_risk,
            "Failed to detect passive acceptance amplification pattern"
        )
    
    def test_detect_lack_of_critical_questions(self):
        """
        Scenario: Long conversation with no user questions or pushback
        Expected: Amplification risk detected
        """
        conversation_history = [
            {"role": "user", "content": "I want to start a business"},
            {"role": "assistant", "content": "Great idea..."},
            {"role": "user", "content": "Tell me more"},
            {"role": "assistant", "content": "Here's how..."},
            {"role": "user", "content": "Continue"},
            {"role": "assistant", "content": "Next..."},
            {"role": "user", "content": "Go on"},
            {"role": "assistant", "content": "Finally..."},
        ]
        
        amplification_risk = self.engine.check_vr25_amplification_prevention(
            conversation_history,
            "engaged"  # Even "engaged" pattern can be risky without questions
        )
        
        self.assertTrue(
            amplification_risk,
            "Failed to detect lack of critical engagement"
        )
    
    def test_no_amplification_with_critical_engagement(self):
        """
        Scenario: User actively questions and challenges
        Expected: No amplification risk
        """
        conversation_history = [
            {"role": "user", "content": "What about this idea?"},
            {"role": "assistant", "content": "Here's my thought..."},
            {"role": "user", "content": "What are the risks?"},
            {"role": "assistant", "content": "The risks include..."},
            {"role": "user", "content": "How do I validate this?"},
        ]
        
        amplification_risk = self.engine.check_vr25_amplification_prevention(
            conversation_history,
            "questioning"
        )
        
        self.assertFalse(
            amplification_risk,
            "False positive: critical engagement flagged as amplification"
        )
    
    def test_no_amplification_in_short_conversation(self):
        """
        Scenario: Brief conversation (< 3 turns)
        Expected: No amplification risk (insufficient data)
        """
        conversation_history = [
            {"role": "user", "content": "I have an idea"},
            {"role": "assistant", "content": "Tell me more"},
        ]
        
        amplification_risk = self.engine.check_vr25_amplification_prevention(
            conversation_history,
            "passive"
        )
        
        self.assertFalse(
            amplification_risk,
            "False positive: short conversation flagged"
        )


class TestIntegratedSafeguards(unittest.TestCase):
    """
    Integration tests for multiple safeguards working together.
    
    Validates that safeguards properly combine when multiple
    verification requirements are triggered simultaneously.
    """
    
    def setUp(self):
        """Initialize the safeguard engine for each test."""
        self.engine = SafeguardEngine()
    
    def test_financial_crisis_multiple_safeguards(self):
        """
        Scenario: Financial crisis triggering VR-23 and VR-24
        Expected: Both financial disclaimer and crisis resources applied
        """
        detected_indicators = {
            "crisis_language": ["last hope"],
            "financial_desperation": ["lost my job", "need money fast", "facing eviction"],
            "health_crisis": [],
            "isolation": []
        }
        
        raw_response = "Here's a business plan that could help."
        
        # Apply VR-23 (financial disclaimer)
        response_with_vr23 = self.engine.apply_vr23_financial_disclaimer(
            raw_response,
            protection_level=3
        )
        
        # Apply VR-24 (crisis response)
        final_response = self.engine.apply_vr24_crisis_response(
            response_with_vr23,
            "financial",
            detected_indicators
        )
        
        # Should have both safeguards
        self.assertIn("Financial Warning", final_response)
        self.assertIn("CRISIS SUPPORT", final_response)
        self.assertIn("business ventures involve risk", final_response.lower())
    
    def test_apply_safeguards_comprehensive(self):
        """
        Scenario: Using comprehensive apply_safeguards method
        Expected: All appropriate safeguards applied correctly
        """
        detected_indicators = {
            "crisis_language": ["thinking about ending it"],
            "financial_desperation": ["lost my job", "need money fast"],
            "health_crisis": [],
            "isolation": ["no one to talk to"]
        }
        
        raw_response = "I can help you explore some options."
        
        safe_response = self.engine.apply_safeguards(
            raw_response,
            protection_level=3,
            detected_indicators=detected_indicators,
            is_financial_topic=True,
            is_crisis=True,
            crisis_type="suicide"
        )
        
        # Should have crisis resources
        self.assertIn("CRISIS SUPPORT", safe_response)
        self.assertIn("988", safe_response)
        
        # Should have financial disclaimer
        self.assertIn("Financial Warning", safe_response)


if __name__ == "__main__":
    unittest.main(verbosity=2)
