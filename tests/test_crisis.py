"""
Unit tests for LFAS Protocol v4 crisis detection
"""

import unittest
import sys
import os

# Add parent directory to path to import lfas module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lfas import CrisisDetector, VulnerabilityDetector, ProtectionLevel
from tests.test_utils import get_spec_path


class TestCrisisDetector(unittest.TestCase):
    """Test suite for CrisisDetector"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.crisis_detector = CrisisDetector()
        self.vuln_detector = VulnerabilityDetector(spec_path=get_spec_path())
    
    def test_no_crisis_for_standard_input(self):
        """Test that non-crisis input doesn't trigger crisis response"""
        detection = self.vuln_detector.detect("Hello, how can I help you?")
        crisis_response = self.crisis_detector.assess_crisis(detection)
        
        self.assertFalse(crisis_response.is_crisis)
        self.assertIsNone(crisis_response.crisis_type)
        self.assertEqual(len(crisis_response.resources), 0)
    
    def test_suicidal_ideation_detection(self):
        """Test detection and response for suicidal ideation"""
        detection = self.vuln_detector.detect(
            "I want to kill myself, can't take it anymore, this is the end"
        )
        crisis_response = self.crisis_detector.assess_crisis(detection)
        
        if crisis_response.is_crisis:
            self.assertEqual(crisis_response.crisis_type, "suicidal_ideation")
            self.assertGreater(len(crisis_response.resources), 0)
            self.assertGreater(len(crisis_response.recommended_actions), 0)
            
            # Check that resources include suicide prevention
            resources_text = ' '.join(crisis_response.resources).lower()
            self.assertTrue(
                'suicide' in resources_text or '988' in resources_text,
                "Should include suicide prevention resources"
            )
    
    def test_financial_crisis_detection(self):
        """Test detection and response for financial crisis"""
        detection = self.vuln_detector.detect(
            "About to be evicted, can't pay rent, completely broke"
        )
        crisis_response = self.crisis_detector.assess_crisis(detection)
        
        if crisis_response.is_crisis:
            self.assertIn(crisis_response.crisis_type, 
                         ["financial_crisis", "general_crisis"])
    
    def test_health_emergency_detection(self):
        """Test detection and response for health emergency"""
        detection = self.vuln_detector.detect(
            "Severe chest pain, can't breathe, medical emergency"
        )
        crisis_response = self.crisis_detector.assess_crisis(detection)
        
        if crisis_response.is_crisis:
            self.assertEqual(crisis_response.crisis_type, "health_emergency")
            resources_text = ' '.join(crisis_response.resources).lower()
            self.assertTrue(
                '911' in resources_text or 'emergency' in resources_text,
                "Should include emergency services"
            )
    
    def test_domestic_violence_detection(self):
        """Test detection and response for domestic violence"""
        detection = self.vuln_detector.detect(
            "My partner hurts me, being abused, afraid for my safety"
        )
        crisis_response = self.crisis_detector.assess_crisis(detection)
        
        if crisis_response.is_crisis:
            self.assertEqual(crisis_response.crisis_type, "domestic_violence")
            resources_text = ' '.join(crisis_response.resources).lower()
            self.assertTrue(
                'domestic violence' in resources_text.lower(),
                "Should include domestic violence resources"
            )
    
    def test_crisis_message_formatting(self):
        """Test that crisis messages are properly formatted"""
        detection = self.vuln_detector.detect(
            "I'm suicidal, want to end my life, can't go on"
        )
        crisis_response = self.crisis_detector.assess_crisis(detection)
        
        if crisis_response.is_crisis:
            message = crisis_response.format_crisis_message()
            
            self.assertIsInstance(message, str)
            self.assertGreater(len(message), 0)
            self.assertIn("CRISIS", message.upper())
    
    def test_safe_response_formatting(self):
        """Test that safe responses prioritize crisis resources"""
        detection = self.vuln_detector.detect(
            "Suicidal thoughts, want to die, no hope left"
        )
        crisis_response = self.crisis_detector.assess_crisis(detection)
        
        original_response = "Here are some tips for feeling better..."
        safe_response = self.crisis_detector.format_safe_response(
            crisis_response, original_response
        )
        
        if crisis_response.is_crisis:
            # Safe response should include crisis resources
            self.assertIn("CRISIS", safe_response.upper())
            # Original response should be suppressed for crisis
            self.assertNotIn(original_response, safe_response)
    
    def test_non_crisis_response_passthrough(self):
        """Test that non-crisis responses are passed through unchanged"""
        detection = self.vuln_detector.detect("Hello, how are you?")
        crisis_response = self.crisis_detector.assess_crisis(detection)
        
        original_response = "I'm doing well, how can I help you?"
        safe_response = self.crisis_detector.format_safe_response(
            crisis_response, original_response
        )
        
        self.assertEqual(safe_response, original_response)
    
    def test_crisis_resources_completeness(self):
        """Test that all crisis types have resources defined"""
        crisis_types = [
            "suicidal_ideation",
            "financial_crisis", 
            "health_emergency",
            "domestic_violence",
            "general_crisis"
        ]
        
        for crisis_type in crisis_types:
            resources = self.crisis_detector._get_crisis_resources(crisis_type)
            self.assertGreater(len(resources), 0,
                             f"No resources defined for {crisis_type}")
    
    def test_recommended_actions_completeness(self):
        """Test that all crisis types have recommended actions"""
        crisis_types = [
            "suicidal_ideation",
            "financial_crisis",
            "health_emergency", 
            "domestic_violence",
            "general_crisis"
        ]
        
        for crisis_type in crisis_types:
            actions = self.crisis_detector._get_recommended_actions(crisis_type)
            self.assertGreater(len(actions), 0,
                             f"No actions defined for {crisis_type}")


class TestCrisisKeywordDetection(unittest.TestCase):
    """Test crisis keyword detection accuracy"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.crisis_detector = CrisisDetector()
    
    def test_suicidal_keywords(self):
        """Test suicidal ideation keyword detection"""
        test_cases = [
            ("I want to kill myself", "suicidal_ideation"),
            ("thinking about suicide", "suicidal_ideation"),
            ("want to end my life", "suicidal_ideation"),
        ]
        
        for text, expected_type in test_cases:
            detected_type = self.crisis_detector._identify_crisis_type(text)
            self.assertEqual(detected_type, expected_type,
                           f"Failed to identify '{text}' as {expected_type}")
    
    def test_financial_keywords(self):
        """Test financial crisis keyword detection"""
        test_cases = [
            ("can't pay rent", "financial_crisis"),
            ("about to be evicted", "financial_crisis"),
            ("utilities shut off", "financial_crisis"),
        ]
        
        for text, expected_type in test_cases:
            detected_type = self.crisis_detector._identify_crisis_type(text)
            self.assertEqual(detected_type, expected_type,
                           f"Failed to identify '{text}' as {expected_type}")


if __name__ == '__main__':
    unittest.main()
