"""
Tests for LFAS Protocol v4 - Vulnerability Detector
"""

import pytest
from lfas.detector import VulnerabilityDetector
from lfas.models import ProtectionLevel


class TestVulnerabilityDetector:
    """Tests for VulnerabilityDetector"""
    
    def test_create_detector(self):
        """Test creating a vulnerability detector"""
        detector = VulnerabilityDetector()
        assert detector is not None
        assert detector.indicators is not None
        assert len(detector.conversation_history) == 0
    
    def test_detect_standard_protection(self):
        """Test detection with no triggers (Standard protection)"""
        detector = VulnerabilityDetector()
        result = detector.detect("Hello, how are you today?")
        
        assert result.protection_level == ProtectionLevel.STANDARD
        assert result.triggers_count == 0
        assert len(result.detected_categories) == 0
    
    def test_detect_enhanced_protection(self):
        """Test detection with 1-2 triggers (Enhanced protection)"""
        detector = VulnerabilityDetector()
        result = detector.detect("I lost my job recently")
        
        assert result.protection_level == ProtectionLevel.ENHANCED
        assert result.triggers_count >= 1
        assert result.triggers_count <= 2
    
    def test_detect_crisis_protection(self):
        """Test detection with 3+ triggers (Crisis protection)"""
        detector = VulnerabilityDetector()
        result = detector.detect("I lost my job, this is my last hope, can't take it anymore")
        
        assert result.protection_level == ProtectionLevel.CRISIS
        assert result.triggers_count >= 3
        assert len(result.detected_categories) > 0
    
    def test_detect_crisis_language(self):
        """Test detection of crisis language indicators"""
        detector = VulnerabilityDetector()
        result = detector.detect("This is my last hope, nobody understands, I'm done")
        
        assert result.protection_level == ProtectionLevel.CRISIS
        assert "crisis_language" in result.detected_categories
    
    def test_detect_financial_desperation(self):
        """Test detection of financial desperation indicators"""
        detector = VulnerabilityDetector()
        result = detector.detect("I lost my job, need money fast, behind on rent")
        
        assert result.protection_level == ProtectionLevel.CRISIS
        assert "financial_desperation" in result.detected_categories
    
    def test_detect_health_crisis(self):
        """Test detection of health crisis indicators"""
        detector = VulnerabilityDetector()
        result = detector.detect("Pain won't stop, can't see a doctor, no insurance")
        
        assert result.protection_level == ProtectionLevel.CRISIS
        assert "health_crisis" in result.detected_categories
    
    def test_detect_isolation_indicators(self):
        """Test detection of isolation indicators"""
        detector = VulnerabilityDetector()
        result = detector.detect("No one to talk to, you're the only one who listens, completely alone")
        
        assert result.protection_level == ProtectionLevel.CRISIS
        assert "isolation_indicators" in result.detected_categories
    
    def test_conversation_history_maintained(self):
        """Test that conversation history is maintained"""
        detector = VulnerabilityDetector()
        
        result1 = detector.detect("First message")
        result2 = detector.detect("Second message")
        result3 = detector.detect("Third message")
        
        assert len(detector.conversation_history) == 3
        assert detector.conversation_history[0] == "First message"
        assert detector.conversation_history[2] == "Third message"
        
        # Results should contain history
        assert result3.conversation_history is not None
        assert len(result3.conversation_history) == 3
    
    def test_conversation_history_optional(self):
        """Test that conversation history can be disabled"""
        detector = VulnerabilityDetector()
        
        result = detector.detect("Test message", maintain_history=False)
        
        assert len(detector.conversation_history) == 0
        assert result.conversation_history is None
    
    def test_reset_history(self):
        """Test resetting conversation history"""
        detector = VulnerabilityDetector()
        
        detector.detect("Message 1")
        detector.detect("Message 2")
        assert len(detector.conversation_history) == 2
        
        detector.reset_history()
        assert len(detector.conversation_history) == 0
    
    def test_case_insensitive_detection(self):
        """Test that detection is case-insensitive"""
        detector = VulnerabilityDetector()
        
        result_lower = detector.detect("last hope")
        detector.reset_history()
        result_upper = detector.detect("LAST HOPE")
        detector.reset_history()
        result_mixed = detector.detect("Last Hope")
        
        # All should detect the trigger
        assert result_lower.triggers_count > 0
        assert result_upper.triggers_count > 0
        assert result_mixed.triggers_count > 0
    
    def test_original_input_preserved(self):
        """Test that original input is preserved in result"""
        detector = VulnerabilityDetector()
        original = "This is my original message"
        
        result = detector.detect(original)
        
        assert result.original_input == original
    
    def test_reload_specification(self):
        """Test reloading the specification"""
        detector = VulnerabilityDetector()
        original_indicators = detector.indicators.copy()
        
        detector.reload_specification()
        
        # Should reload successfully
        assert detector.indicators is not None
        assert detector.indicators.keys() == original_indicators.keys()
    
    def test_multiple_categories_detected(self):
        """Test detection across multiple categories"""
        detector = VulnerabilityDetector()
        result = detector.detect(
            "Lost my job, can't pay bills, completely alone, nobody understands"
        )
        
        # Should detect multiple categories
        assert result.protection_level == ProtectionLevel.CRISIS
        assert len(result.detected_categories) >= 2
        assert "financial_desperation" in result.detected_categories
        # "completely alone" and "nobody understands" are in crisis_language
        assert "crisis_language" in result.detected_categories
    
    def test_exact_phrase_matching(self):
        """Test that detector matches exact phrases from indicators"""
        detector = VulnerabilityDetector()
        
        # "last hope" is a known indicator
        result = detector.detect("This is my last hope for success")
        assert result.triggers_count > 0
    
    def test_protection_level_escalation(self):
        """Test that protection levels escalate correctly"""
        detector = VulnerabilityDetector()
        
        # 0 triggers = Standard (Level 1)
        result_0 = detector.detect("Hello there")
        assert result_0.protection_level.value == 1
        
        detector.reset_history()
        
        # 1-2 triggers = Enhanced (Level 2)
        result_1 = detector.detect("I lost my job")
        assert result_1.protection_level.value == 2
        
        detector.reset_history()
        
        # 3+ triggers = Crisis (Level 3)
        result_3 = detector.detect("I lost my job, this is my last hope, nobody understands")
        assert result_3.protection_level.value == 3
