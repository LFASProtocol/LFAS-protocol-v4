"""
Test suite for LFAS Protocol safeguards.

Tests the ACT phase implementation:
- VR-24 Crisis Detection & Response
- Crisis resource provision
- Appropriate response generation
"""

import pytest
from lfas_protocol.detector import VulnerabilityDetector, ProtectionLevel
from lfas_protocol.safeguards import CrisisDetectionSafeguard


class TestCrisisDetectionSafeguard:
    """Test cases for the CrisisDetectionSafeguard class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = VulnerabilityDetector()
        self.safeguard = CrisisDetectionSafeguard()
    
    def test_should_activate_crisis_level(self):
        """Test that safeguard activates for crisis protection level."""
        result = self.detector.detect(
            "I can't take it anymore, nobody understands, this is my last hope"
        )
        
        assert result.protection_level == ProtectionLevel.CRISIS
        assert self.safeguard.should_activate(result) is True
    
    def test_should_activate_enhanced_with_crisis_language(self):
        """Test that safeguard activates for enhanced level with crisis language."""
        result = self.detector.detect("I can't take it anymore")
        
        # May be enhanced or crisis level
        if result.protection_level == ProtectionLevel.ENHANCED:
            assert "crisis_language" in result.categories
            assert self.safeguard.should_activate(result) is True
    
    def test_should_not_activate_standard_level(self):
        """Test that safeguard doesn't activate for standard protection level."""
        result = self.detector.detect("I'm feeling great today!")
        
        assert result.protection_level == ProtectionLevel.STANDARD
        assert self.safeguard.should_activate(result) is False
    
    def test_should_not_activate_enhanced_without_crisis_language(self):
        """Test that safeguard doesn't activate for enhanced level without crisis language."""
        result = self.detector.detect("I lost my job")
        
        if result.protection_level == ProtectionLevel.ENHANCED:
            if "crisis_language" not in result.categories:
                assert self.safeguard.should_activate(result) is False
    
    def test_generate_response_includes_acknowledgment(self):
        """Test that generated response includes acknowledgment."""
        result = self.detector.detect("I can't take it anymore")
        response = self.safeguard.generate_response(result)
        
        assert "pain" in response.lower() or "difficult" in response.lower()
        assert "hear" in response.lower()
    
    def test_generate_response_includes_crisis_resources(self):
        """Test that generated response includes crisis resources."""
        result = self.detector.detect(
            "I can't take it anymore, everything is hopeless"
        )
        response = self.safeguard.generate_response(result)
        
        # Check for crisis resource phone numbers
        assert "988" in response
        assert "741741" in response or "Crisis Text Line" in response
    
    def test_generate_response_includes_professional_help(self):
        """Test that response encourages professional help."""
        result = self.detector.detect("I can't take it anymore")
        response = self.safeguard.generate_response(result)
        
        assert "reach" in response.lower() or "contact" in response.lower()
        assert "alone" in response.lower()
    
    def test_generate_response_health_crisis_includes_medical_guidance(self):
        """Test that health crisis includes medical guidance."""
        result = self.detector.detect(
            "I can't see a doctor, no insurance, pain won't stop. "
            "This is my last hope."
        )
        response = self.safeguard.generate_response(result)
        
        if "health_crisis" in result.categories:
            assert "healthcare" in response.lower() or "medical" in response.lower()
    
    def test_get_crisis_resources(self):
        """Test retrieval of crisis resources."""
        resources = self.safeguard.get_crisis_resources()
        
        assert len(resources) > 0
        
        # Check that all resources have required fields
        for resource in resources:
            assert resource.name
            assert resource.phone
            assert resource.description
            assert resource.available
    
    def test_crisis_resources_include_suicide_prevention(self):
        """Test that crisis resources include suicide prevention."""
        resources = self.safeguard.get_crisis_resources()
        
        has_suicide_prevention = any(
            "988" in resource.phone or "suicide" in resource.name.lower()
            for resource in resources
        )
        
        assert has_suicide_prevention is True
    
    def test_scenario_from_demo_mental_health_crisis_response(self):
        """Test scenario from lfas-basic-demo.md: Mental Health Crisis response."""
        result = self.detector.detect("I can't take it anymore, everything is hopeless")
        
        # Safeguard should activate
        assert self.safeguard.should_activate(result) is True
        
        # Generate response
        response = self.safeguard.generate_response(result)
        
        # Response should:
        # 1. Acknowledge the pain/difficulty
        assert "pain" in response.lower() or "difficult" in response.lower()
        
        # 2. Include crisis resources
        assert "988" in response or "crisis" in response.lower()
        
        # 3. Encourage reaching out
        assert "reach" in response.lower() or "contact" in response.lower()
    
    def test_response_pauses_normal_processing(self):
        """Test that crisis response pauses normal processing."""
        result = self.detector.detect("I can't take it anymore")
        response = self.safeguard.generate_response(result)
        
        # Should acknowledge crisis state explicitly
        assert "crisis" in response.lower() or "safety" in response.lower()
        
        # Should focus on immediate support, not business/productivity
        assert "business" not in response.lower()
        assert "productivity" not in response.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
