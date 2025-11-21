"""
LFAS Protocol v4 - Test Suite for Core Components

Tests for vulnerability detection, protection level management,
and safeguard application.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from core import VulnerabilityDetector, ProtectionLevel, ProtectionLevelManager, SafeguardEngine


class TestVulnerabilityDetector(unittest.TestCase):
    """Test the vulnerability detection engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = VulnerabilityDetector()
    
    def test_no_triggers(self):
        """Test input with no vulnerability indicators."""
        text = "Hello, how are you today?"
        detected = self.detector.detect(text)
        
        self.assertEqual(self.detector.count_triggers(detected), 0)
        self.assertFalse(self.detector.has_any_triggers(detected))
    
    def test_financial_desperation(self):
        """Test detection of financial desperation indicators."""
        text = "I lost my job and need money fast"
        detected = self.detector.detect(text)
        
        self.assertGreater(self.detector.count_triggers(detected), 0)
        self.assertIn('financial_desperation', self.detector.get_categories_triggered(detected))
    
    def test_crisis_language(self):
        """Test detection of crisis language."""
        text = "I can't take it anymore, this is my last hope"
        detected = self.detector.detect(text)
        
        self.assertGreater(self.detector.count_triggers(detected), 0)
        self.assertIn('crisis_language', self.detector.get_categories_triggered(detected))
    
    def test_multiple_categories(self):
        """Test detection across multiple categories."""
        text = "I lost my job and can't take it anymore. Nobody understands."
        detected = self.detector.detect(text)
        
        categories = self.detector.get_categories_triggered(detected)
        self.assertGreaterEqual(len(categories), 2)
        self.assertIn('financial_desperation', categories)
        self.assertIn('crisis_language', categories)
    
    def test_conversation_history(self):
        """Test detection with conversation history."""
        history = ["I'm feeling really down", "I lost my job last week"]
        current = "I need help"
        
        detected = self.detector.detect(current, history)
        triggers = self.detector.count_triggers(detected)
        
        # Should detect triggers from history
        self.assertGreater(triggers, 0)


class TestProtectionLevelManager(unittest.TestCase):
    """Test the protection level management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = ProtectionLevelManager()
    
    def test_standard_level(self):
        """Test standard protection level (0 triggers)."""
        level = self.manager.determine_level(0)
        self.assertEqual(level, ProtectionLevel.STANDARD)
    
    def test_enhanced_level(self):
        """Test enhanced protection level (1-2 triggers)."""
        level = self.manager.determine_level(1)
        self.assertEqual(level, ProtectionLevel.ENHANCED)
        
        level = self.manager.determine_level(2)
        self.assertEqual(level, ProtectionLevel.ENHANCED)
    
    def test_crisis_level(self):
        """Test crisis protection level (3+ triggers)."""
        level = self.manager.determine_level(3)
        self.assertEqual(level, ProtectionLevel.CRISIS)
        
        level = self.manager.determine_level(5)
        self.assertEqual(level, ProtectionLevel.CRISIS)
    
    def test_escalation(self):
        """Test protection level escalation."""
        # Start at standard
        self.manager.update(0)
        self.assertEqual(self.manager.get_current_level(), ProtectionLevel.STANDARD)
        
        # Escalate to enhanced
        self.manager.update(2)
        self.assertEqual(self.manager.get_current_level(), ProtectionLevel.ENHANCED)
        
        # Escalate to crisis
        self.manager.update(3)
        self.assertEqual(self.manager.get_current_level(), ProtectionLevel.CRISIS)
    
    def test_deescalation(self):
        """Test protection level de-escalation after clear exchanges."""
        # Escalate to crisis
        self.manager.update(3)
        self.assertEqual(self.manager.get_current_level(), ProtectionLevel.CRISIS)
        
        # Clear exchanges should de-escalate
        self.manager.update(0)
        self.manager.update(0)
        self.manager.update(0)
        
        # After 3 clear exchanges, should return to standard
        self.assertEqual(self.manager.get_current_level(), ProtectionLevel.STANDARD)
    
    def test_active_safeguards(self):
        """Test getting active safeguards for each level."""
        # Standard level
        self.manager.update(0)
        safeguards = self.manager.get_active_safeguards()
        self.assertIn('VR-20: Unfounded Optimism Prevention', safeguards)
        
        # Enhanced level
        self.manager.update(2)
        safeguards = self.manager.get_active_safeguards()
        self.assertIn('Enhanced reality checking', safeguards)
        
        # Crisis level
        self.manager.update(3)
        safeguards = self.manager.get_active_safeguards()
        self.assertIn('VR-24: Crisis Detection & Response', safeguards)


class TestSafeguardEngine(unittest.TestCase):
    """Test the safeguard application engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = SafeguardEngine()
    
    def test_standard_safeguards(self):
        """Test application of standard safeguards."""
        response = "This is a test response"
        categories = set()
        
        result = self.engine.apply_safeguards(
            response, ProtectionLevel.STANDARD, categories
        )
        
        # Should return modified response
        self.assertIsInstance(result, str)
    
    def test_enhanced_financial_safeguards(self):
        """Test enhanced safeguards for financial desperation."""
        response = "Here's a business idea"
        categories = {'financial_desperation'}
        
        result = self.engine.apply_safeguards(
            response, ProtectionLevel.ENHANCED, categories
        )
        
        # Should include financial disclaimer
        self.assertIn("difficult financial situation", result.lower())
    
    def test_crisis_safeguards(self):
        """Test crisis safeguards application."""
        response = "Let me help you"
        categories = {'crisis_language'}
        
        result = self.engine.apply_safeguards(
            response, ProtectionLevel.CRISIS, categories
        )
        
        # Should include crisis resources
        self.assertIn("Crisis", result)
        self.assertIn("988", result)  # Suicide prevention line
    
    def test_isolation_safeguards(self):
        """Test safeguards for isolation indicators."""
        response = "I'm here to help"
        categories = {'isolation_indicators'}
        
        result = self.engine.apply_safeguards(
            response, ProtectionLevel.CRISIS, categories
        )
        
        # Should encourage human connection
        self.assertIn("human connection", result.lower())
    
    def test_should_pause_and_verify(self):
        """Test pause requirement for different levels."""
        self.assertFalse(
            self.engine.should_pause_and_verify(ProtectionLevel.STANDARD)
        )
        self.assertTrue(
            self.engine.should_pause_and_verify(ProtectionLevel.ENHANCED)
        )
        self.assertTrue(
            self.engine.should_pause_and_verify(ProtectionLevel.CRISIS)
        )


if __name__ == '__main__':
    unittest.main()
