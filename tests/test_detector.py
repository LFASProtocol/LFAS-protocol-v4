"""
Unit tests for LFAS Protocol v4 vulnerability detection
"""

import unittest
import sys
import os

# Add parent directory to path to import lfas module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lfas import VulnerabilityDetector, ProtectionLevel


class TestVulnerabilityDetector(unittest.TestCase):
    """Test suite for VulnerabilityDetector"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Note: This will fail if the XML spec is not in the expected location
        # For testing, we may need to adjust the path
        try:
            self.detector = VulnerabilityDetector(
                spec_path="protocol/lfas-v4-specification.xml"
            )
        except FileNotFoundError:
            # Fallback for different test environments
            self.detector = VulnerabilityDetector(
                spec_path="../protocol/lfas-v4-specification.xml"
            )
    
    def test_standard_protection_no_triggers(self):
        """Test that normal input gets Standard protection"""
        result = self.detector.detect("Hello, how are you today?")
        self.assertEqual(result.protection_level, ProtectionLevel.STANDARD)
        self.assertEqual(result.triggers_count, 0)
        self.assertEqual(len(result.detected_categories), 0)
    
    def test_enhanced_protection_single_trigger(self):
        """Test that single vulnerability trigger gets Enhanced protection"""
        result = self.detector.detect("I just lost my job and I'm worried")
        self.assertGreaterEqual(result.protection_level.value, ProtectionLevel.ENHANCED.value)
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_crisis_protection_multiple_triggers(self):
        """Test that multiple triggers get Crisis protection"""
        result = self.detector.detect(
            "I lost my job, this is my last hope, I can't take it anymore"
        )
        self.assertEqual(result.protection_level, ProtectionLevel.CRISIS)
        self.assertGreaterEqual(result.triggers_count, 3)
    
    def test_financial_desperation_detection(self):
        """Test detection of financial crisis indicators"""
        test_inputs = [
            "I lost my job and need money fast",
            "Can't pay bills, facing eviction",
            "Desperate for income, last $100"
        ]
        
        for input_text in test_inputs:
            result = self.detector.detect(input_text)
            self.assertGreaterEqual(result.triggers_count, 1,
                                  f"Failed to detect trigger in: {input_text}")
            self.assertIn("financial_desperation", result.detected_categories)
    
    def test_crisis_language_detection(self):
        """Test detection of crisis language indicators"""
        test_inputs = [
            "This is my last hope",
            "I can't take it anymore",
            "Thinking about ending it",
            "Nobody understands me"
        ]
        
        for input_text in test_inputs:
            result = self.detector.detect(input_text)
            self.assertGreaterEqual(result.triggers_count, 1,
                                  f"Failed to detect trigger in: {input_text}")
    
    def test_isolation_indicators_detection(self):
        """Test detection of isolation indicators"""
        result = self.detector.detect("I'm completely alone, no one to talk to")
        self.assertGreaterEqual(result.triggers_count, 1)
        self.assertIn("isolation_indicators", result.detected_categories)
    
    def test_health_crisis_detection(self):
        """Test detection of health crisis indicators"""
        result = self.detector.detect("I can't see a doctor, no insurance, pain won't stop")
        self.assertGreaterEqual(result.triggers_count, 1)
        self.assertIn("health_crisis", result.detected_categories)
    
    def test_case_insensitive_detection(self):
        """Test that detection is case-insensitive"""
        result1 = self.detector.detect("LOST MY JOB")
        result2 = self.detector.detect("lost my job")
        result3 = self.detector.detect("Lost My Job")
        
        self.assertEqual(result1.triggers_count, result2.triggers_count)
        self.assertEqual(result2.triggers_count, result3.triggers_count)
    
    def test_detection_result_methods(self):
        """Test DetectionResult helper methods"""
        # Standard result
        result = self.detector.detect("Hello world")
        self.assertFalse(result.is_crisis())
        self.assertFalse(result.is_vulnerable())
        
        # Crisis result - need at least 3 distinct phrases
        result = self.detector.detect("last hope, nobody understands, if this doesn't work I'm done")
        self.assertTrue(result.is_crisis())
        self.assertTrue(result.is_vulnerable())
    
    def test_detection_result_string_representation(self):
        """Test that DetectionResult can be converted to string"""
        result = self.detector.detect("I lost my job")
        result_str = str(result)
        self.assertIsInstance(result_str, str)
        self.assertIn("Protection Level", result_str)
        self.assertIn("Triggers", result_str)


class TestProtectionLevelEscalation(unittest.TestCase):
    """Test protection level escalation rules"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            self.detector = VulnerabilityDetector(
                spec_path="protocol/lfas-v4-specification.xml"
            )
        except FileNotFoundError:
            self.detector = VulnerabilityDetector(
                spec_path="../protocol/lfas-v4-specification.xml"
            )
    
    def test_escalation_from_standard_to_enhanced(self):
        """Test escalation from Standard to Enhanced protection"""
        inputs = [
            "Everything is fine",  # Standard
            "I lost my job"  # Enhanced - contains "lost my job"
        ]
        
        results = [self.detector.detect(input_text) for input_text in inputs]
        self.assertEqual(results[0].protection_level, ProtectionLevel.STANDARD)
        self.assertGreaterEqual(results[1].protection_level.value, 
                              ProtectionLevel.ENHANCED.value)
    
    def test_escalation_to_crisis(self):
        """Test escalation to Crisis protection"""
        result = self.detector.detect(
            "Lost my job, this is my last hope, if this doesn't work I'm done"
        )
        self.assertEqual(result.protection_level, ProtectionLevel.CRISIS)
        self.assertGreaterEqual(result.triggers_count, 3)


if __name__ == '__main__':
    unittest.main()
