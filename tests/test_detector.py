"""
Tests for VulnerabilityDetector
"""

import pytest
from lfas.detector import VulnerabilityDetector
from lfas.models import ProtectionLevel


class TestVulnerabilityDetector:
    """Test vulnerability detection functionality"""
    
    def test_initialization(self):
        detector = VulnerabilityDetector()
        assert detector.indicators is not None
        assert len(detector.indicators) > 0
        assert detector.escalation_rules is not None
        assert detector.conversation_history == []
    
    def test_detect_standard_protection(self):
        detector = VulnerabilityDetector()
        result = detector.detect("Hello, how are you today?")
        
        assert result.protection_level == ProtectionLevel.STANDARD
        assert result.triggers_count == 0
        assert len(result.detected_categories) == 0
    
    def test_detect_enhanced_protection_single_trigger(self):
        detector = VulnerabilityDetector()
        result = detector.detect("I lost my job last week")
        
        assert result.protection_level == ProtectionLevel.ENHANCED
        assert result.triggers_count >= 1
        assert result.triggers_count < 3
    
    def test_detect_enhanced_protection_two_triggers(self):
        detector = VulnerabilityDetector()
        result = detector.detect("I lost my job and can't pay bills")
        
        assert result.protection_level == ProtectionLevel.ENHANCED
        assert result.triggers_count >= 1
    
    def test_detect_crisis_protection(self):
        detector = VulnerabilityDetector()
        result = detector.detect("I lost my job, this is my last hope, can't take it anymore")
        
        assert result.protection_level == ProtectionLevel.CRISIS
        assert result.triggers_count >= 3
        assert len(result.detected_categories) > 0
    
    def test_detect_crisis_with_suicidal_ideation(self):
        detector = VulnerabilityDetector()
        result = detector.detect("thinking about ending it, nobody understands, completely alone")
        
        assert result.protection_level == ProtectionLevel.CRISIS
        assert result.triggers_count >= 3
    
    def test_detect_categories_crisis_language(self):
        detector = VulnerabilityDetector()
        result = detector.detect("this is my last hope and only chance")
        
        assert "crisis_language" in result.detected_categories
    
    def test_detect_categories_financial(self):
        detector = VulnerabilityDetector()
        result = detector.detect("lost my job and desperate for income")
        
        assert "financial_desperation" in result.detected_categories
    
    def test_detect_categories_health(self):
        detector = VulnerabilityDetector()
        result = detector.detect("can't see a doctor and pain won't stop")
        
        assert "health_crisis" in result.detected_categories
    
    def test_detect_categories_isolation(self):
        detector = VulnerabilityDetector()
        result = detector.detect("no one to talk to and you're the only one who listens")
        
        assert "isolation_indicators" in result.detected_categories
    
    def test_conversation_history_tracking(self):
        detector = VulnerabilityDetector()
        
        result1 = detector.detect("Hello")
        assert len(detector.conversation_history) == 1
        
        result2 = detector.detect("I'm feeling down")
        assert len(detector.conversation_history) == 2
        
        result3 = detector.detect("Can't take it anymore")
        assert len(detector.conversation_history) == 3
    
    def test_conversation_history_in_result(self):
        detector = VulnerabilityDetector()
        
        detector.detect("First message")
        result = detector.detect("Second message")
        
        assert result.conversation_history is not None
        assert len(result.conversation_history) == 2
        assert "First message" in result.conversation_history
        assert "Second message" in result.conversation_history
    
    def test_external_conversation_history(self):
        detector = VulnerabilityDetector()
        
        history = ["Previous context 1", "Previous context 2"]
        result = detector.detect("New message", conversation_history=history)
        
        assert len(result.conversation_history) == 3
        assert "Previous context 1" in result.conversation_history
        assert "New message" in result.conversation_history
    
    def test_reset_history(self):
        detector = VulnerabilityDetector()
        
        detector.detect("Message 1")
        detector.detect("Message 2")
        assert len(detector.conversation_history) == 2
        
        detector.reset_history()
        assert len(detector.conversation_history) == 0
    
    def test_case_insensitive_detection(self):
        detector = VulnerabilityDetector()
        
        result1 = detector.detect("LOST MY JOB")
        result2 = detector.detect("lost my job")
        result3 = detector.detect("LosT mY JoB")
        
        assert result1.triggers_count == result2.triggers_count
        assert result2.triggers_count == result3.triggers_count
    
    def test_original_input_preserved(self):
        detector = VulnerabilityDetector()
        original = "This is my ORIGINAL message with CaSe"
        
        result = detector.detect(original)
        assert result.original_input == original
    
    def test_multiple_categories_detected(self):
        detector = VulnerabilityDetector()
        result = detector.detect(
            "I lost my job, can't see a doctor, nobody understands, this is my last hope"
        )
        
        # Should detect multiple categories
        assert len(result.detected_categories) >= 2
        assert result.protection_level == ProtectionLevel.CRISIS
    
    def test_escalation_rules_applied(self):
        detector = VulnerabilityDetector()
        
        # 0 triggers
        result0 = detector.detect("Nice weather today")
        assert result0.protection_level == ProtectionLevel.STANDARD
        
        # 1-2 triggers
        detector.reset_history()
        result1 = detector.detect("lost my job")
        assert result1.protection_level == ProtectionLevel.ENHANCED
        
        # 3+ triggers
        detector.reset_history()
        result3 = detector.detect("lost my job, can't take it anymore, this is my last hope")
        assert result3.protection_level == ProtectionLevel.CRISIS
