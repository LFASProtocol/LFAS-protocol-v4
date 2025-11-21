"""
LFAS Protocol v4 - Test Suite for Middleware

Tests for the core LFAS middleware orchestration.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from core import LFASMiddleware


class TestLFASMiddleware(unittest.TestCase):
    """Test the main LFAS middleware."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.middleware = LFASMiddleware()
        
        # Mock AI response generator
        def mock_ai(user_input):
            return "This is a test AI response."
        
        self.mock_ai = mock_ai
    
    def test_standard_interaction(self):
        """Test a standard interaction with no triggers."""
        user_input = "Hello, how are you?"
        
        result = self.middleware.process_request(user_input, self.mock_ai)
        
        self.assertIn('response', result)
        self.assertIn('metadata', result)
        self.assertEqual(result['metadata']['protection_level'], 'STANDARD')
        self.assertEqual(result['metadata']['trigger_count'], 0)
    
    def test_enhanced_protection(self):
        """Test enhanced protection with 2 triggers."""
        user_input = "I lost my job and can't pay bills"
        
        result = self.middleware.process_request(user_input, self.mock_ai)
        
        self.assertEqual(result['metadata']['protection_level'], 'ENHANCED')
        self.assertGreaterEqual(result['metadata']['trigger_count'], 2)
    
    def test_crisis_protection(self):
        """Test crisis protection with 3+ triggers."""
        user_input = "I can't take it anymore. I'm completely alone. This is my last hope."
        
        result = self.middleware.process_request(user_input, self.mock_ai)
        
        self.assertEqual(result['metadata']['protection_level'], 'CRISIS')
        self.assertGreaterEqual(result['metadata']['trigger_count'], 3)
        
        # Should include crisis resources
        self.assertIn('988', result['response'])
    
    def test_conversation_history(self):
        """Test that conversation history is maintained."""
        # First message
        self.middleware.process_request("Hello", self.mock_ai)
        
        # Second message
        self.middleware.process_request("How are you?", self.mock_ai)
        
        # Check history is maintained
        self.assertEqual(len(self.middleware.conversation_history), 2)
    
    def test_process_with_existing_response(self):
        """Test processing when AI response already exists."""
        user_input = "I lost my job"
        ai_response = "Here's what you should do..."
        
        result = self.middleware.process_with_response(user_input, ai_response)
        
        self.assertIn('response', result)
        self.assertIn('metadata', result)
        # Response should be modified with safeguards
        self.assertIsNotNone(result['response'])
    
    def test_reset(self):
        """Test resetting middleware state."""
        # Add some history
        self.middleware.process_request("Hello", self.mock_ai)
        self.middleware.process_request("Test", self.mock_ai)
        
        # Reset
        self.middleware.reset()
        
        # History should be cleared
        self.assertEqual(len(self.middleware.conversation_history), 0)
        self.assertEqual(
            self.middleware.protection_manager.get_current_level().name,
            'STANDARD'
        )
    
    def test_get_status(self):
        """Test getting middleware status."""
        status = self.middleware.get_status()
        
        self.assertIn('protection_level', status)
        self.assertIn('active_safeguards', status)
        self.assertIn('conversation_length', status)
    
    def test_metadata_completeness(self):
        """Test that all expected metadata is present."""
        result = self.middleware.process_request("Test", self.mock_ai)
        metadata = result['metadata']
        
        required_keys = [
            'protection_level',
            'trigger_count',
            'detected_categories',
            'active_safeguards',
            'requires_verification'
        ]
        
        for key in required_keys:
            self.assertIn(key, metadata)


class TestScenarios(unittest.TestCase):
    """Test real-world scenarios from the LFAS demonstration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.middleware = LFASMiddleware()
        
        def mock_ai(user_input):
            # Different responses based on input
            if "job" in user_input.lower():
                return "Here are 10 business ideas you can start today!"
            elif "anymore" in user_input.lower():
                return "That sounds difficult! Here are 5 productivity tips!"
            return "How can I help you?"
        
        self.mock_ai = mock_ai
    
    def test_scenario_financial_crisis(self):
        """Test Scenario 1: Financial Crisis from demonstration."""
        user_input = "I lost my job and have $100 left. I need to make money fast."
        
        result = self.middleware.process_request(user_input, self.mock_ai)
        
        # Should detect financial desperation
        self.assertIn('financial_desperation', result['metadata']['detected_categories'])
        
        # Should be at least Enhanced protection
        self.assertIn(result['metadata']['protection_level'], ['ENHANCED', 'CRISIS'])
        
        # Should include realistic disclaimer
        response_lower = result['response'].lower()
        self.assertTrue(
            'difficult' in response_lower or 'risk' in response_lower,
            "Response should include realistic assessment"
        )
    
    def test_scenario_mental_health_crisis(self):
        """Test Scenario 2: Mental Health Crisis from demonstration."""
        user_input = "I can't take it anymore, everything is hopeless"
        
        result = self.middleware.process_request(user_input, self.mock_ai)
        
        # Should detect crisis language
        self.assertIn('crisis_language', result['metadata']['detected_categories'])
        
        # Should be at Crisis protection level
        self.assertEqual(result['metadata']['protection_level'], 'CRISIS')
        
        # Should include crisis resources
        self.assertIn('Crisis', result['response'])
        self.assertIn('988', result['response'])


if __name__ == '__main__':
    unittest.main()
