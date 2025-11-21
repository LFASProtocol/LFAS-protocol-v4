"""
Test suite for LFAS Protocol vulnerability detector.

Tests the LISTEN phase implementation:
- Detection of crisis language
- Detection of financial desperation
- Detection of health crisis
- Detection of isolation indicators
- Protection level escalation
"""

import pytest
from lfas_protocol.detector import VulnerabilityDetector, ProtectionLevel


class TestVulnerabilityDetector:
    """Test cases for the VulnerabilityDetector class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = VulnerabilityDetector()
    
    def test_standard_protection_no_triggers(self):
        """Test that normal input results in standard protection."""
        result = self.detector.detect("I'm feeling great today!")
        
        assert result.protection_level == ProtectionLevel.STANDARD
        assert result.indicator_count == 0
        assert len(result.triggered_indicators) == 0
        assert len(result.categories) == 0
    
    def test_crisis_language_detection(self):
        """Test detection of crisis language indicators."""
        test_inputs = [
            "I can't take it anymore, everything is hopeless",
            "This is my last hope",
            "I don't want to live anymore",
            "Thinking about ending it all",
        ]
        
        for input_text in test_inputs:
            result = self.detector.detect(input_text)
            assert result.indicator_count > 0
            assert "crisis_language" in result.categories
    
    def test_financial_desperation_detection(self):
        """Test detection of financial desperation indicators."""
        test_inputs = [
            "I lost my job and have $100 left",
            "I need money fast, can't pay bills",
            "Facing eviction, behind on rent",
            "Desperate for income",
        ]
        
        for input_text in test_inputs:
            result = self.detector.detect(input_text)
            assert result.indicator_count > 0
            assert "financial_desperation" in result.categories
    
    def test_health_crisis_detection(self):
        """Test detection of health crisis indicators."""
        test_inputs = [
            "I can't see a doctor, no insurance",
            "Pain won't stop, can't afford medication",
            "No medical help available",
        ]
        
        for input_text in test_inputs:
            result = self.detector.detect(input_text)
            assert result.indicator_count > 0
            assert "health_crisis" in result.categories
    
    def test_isolation_detection(self):
        """Test detection of isolation indicators."""
        test_inputs = [
            "No one to talk to, family doesn't understand",
            "You're the only one who listens",
            "Completely alone in this",
        ]
        
        for input_text in test_inputs:
            result = self.detector.detect(input_text)
            assert result.indicator_count > 0
            assert "isolation" in result.categories
    
    def test_enhanced_protection_two_triggers(self):
        """Test that 1-2 triggers result in enhanced protection."""
        # Single trigger
        result = self.detector.detect("I lost my job")
        assert result.protection_level == ProtectionLevel.ENHANCED
        assert result.indicator_count >= 1
        
        # Two triggers
        result = self.detector.detect("I lost my job and need money fast")
        assert result.protection_level == ProtectionLevel.ENHANCED
        assert result.indicator_count >= 2
    
    def test_crisis_protection_three_plus_triggers(self):
        """Test that 3+ triggers result in crisis protection."""
        result = self.detector.detect(
            "I lost my job, can't pay bills, and this is my last hope. "
            "I'm completely alone and can't take it anymore."
        )
        
        assert result.protection_level == ProtectionLevel.CRISIS
        assert result.indicator_count >= 3
    
    def test_case_insensitive_detection(self):
        """Test that detection is case-insensitive."""
        inputs = [
            "I LOST MY JOB",
            "Lost My Job",
            "lost my job",
        ]
        
        for input_text in inputs:
            result = self.detector.detect(input_text)
            assert result.indicator_count > 0
    
    def test_multiple_categories_detected(self):
        """Test detection across multiple categories."""
        result = self.detector.detect(
            "I lost my job and can't afford medication. "
            "Nobody understands what I'm going through."
        )
        
        assert len(result.categories) >= 2
        assert "financial_desperation" in result.categories
        assert "health_crisis" in result.categories or "isolation" in result.categories
    
    def test_get_indicator_categories(self):
        """Test retrieval of indicator categories."""
        categories = self.detector.get_indicator_categories()
        
        assert "crisis_language" in categories
        assert "financial_desperation" in categories
        assert "health_crisis" in categories
        assert "isolation" in categories
        
        # Ensure each category has indicators
        for category, indicators in categories.items():
            assert len(indicators) > 0
            assert all(isinstance(indicator, str) for indicator in indicators)
    
    def test_scenario_from_demo_financial_crisis(self):
        """Test scenario from lfas-basic-demo.md: Financial Crisis."""
        result = self.detector.detect("I lost my job and have $100 left. I need to make money fast.")
        
        # Should detect financial desperation
        assert "financial_desperation" in result.categories
        # Should escalate to at least enhanced protection
        assert result.protection_level >= ProtectionLevel.ENHANCED
    
    def test_scenario_from_demo_mental_health_crisis(self):
        """Test scenario from lfas-basic-demo.md: Mental Health Crisis."""
        result = self.detector.detect("I can't take it anymore, everything is hopeless")
        
        # Should detect crisis language
        assert "crisis_language" in result.categories
        # Should escalate to crisis protection
        assert result.protection_level == ProtectionLevel.CRISIS


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
