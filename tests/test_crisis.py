"""
Tests for LFAS Protocol v4 - Crisis Detector
"""

import pytest
from lfas.detector import VulnerabilityDetector
from lfas.crisis import CrisisDetector
from lfas.models import ProtectionLevel, CrisisType, DetectionResult


class TestCrisisDetector:
    """Tests for CrisisDetector"""
    
    def test_create_crisis_detector(self):
        """Test creating a crisis detector"""
        detector = CrisisDetector()
        assert detector is not None
        assert detector.crisis_resources is not None
    
    def test_assess_crisis_requires_level_3(self):
        """Test that crisis assessment requires protection level 3"""
        detector = CrisisDetector()
        
        # Create a detection result with level 2 (Enhanced)
        result = DetectionResult(
            protection_level=ProtectionLevel.ENHANCED,
            triggers_count=2,
            detected_categories=["financial_desperation"],
            original_input="Test"
        )
        
        # Should raise ValueError
        with pytest.raises(ValueError, match="Crisis assessment requires protection level >= 3"):
            detector.assess_crisis(result)
    
    def test_assess_mental_health_crisis(self):
        """Test assessment of mental health crisis"""
        detector = CrisisDetector()
        
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Last hope, can't take it anymore"
        )
        
        crisis = detector.assess_crisis(result)
        
        assert crisis.crisis_type == CrisisType.MENTAL_HEALTH
        assert crisis.severity in ["moderate", "high", "critical"]
        assert len(crisis.resources) > 0
        assert len(crisis.recommended_actions) > 0
        
        # Should include 988 resource
        assert any("988" in r.contact for r in crisis.resources)
    
    def test_assess_financial_crisis(self):
        """Test assessment of financial crisis"""
        detector = CrisisDetector()
        
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["financial_desperation"],
            original_input="Lost job, behind on rent, need money fast"
        )
        
        crisis = detector.assess_crisis(result)
        
        assert crisis.crisis_type == CrisisType.FINANCIAL
        assert len(crisis.resources) > 0
        assert len(crisis.recommended_actions) > 0
    
    def test_assess_health_crisis(self):
        """Test assessment of health crisis"""
        detector = CrisisDetector()
        
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["health_crisis"],
            original_input="Pain won't stop, can't see doctor, no insurance"
        )
        
        crisis = detector.assess_crisis(result)
        
        assert crisis.crisis_type == CrisisType.HEALTH
        assert len(crisis.resources) > 0
    
    def test_mental_health_prioritization(self):
        """Test that mental health is prioritized in mixed crisis contexts"""
        detector = CrisisDetector()
        
        # Mixed crisis with both financial and mental health indicators
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=5,
            detected_categories=["crisis_language", "financial_desperation"],
            original_input="Lost job, last hope, can't take it anymore"
        )
        
        crisis = detector.assess_crisis(result)
        
        # Mental health should be prioritized
        assert crisis.crisis_type == CrisisType.MENTAL_HEALTH
    
    def test_mixed_crisis_type(self):
        """Test detection of mixed crisis type"""
        detector = CrisisDetector()
        
        # Multiple crisis types without mental health
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=4,
            detected_categories=["financial_desperation", "health_crisis"],
            original_input="Lost job, behind on rent, pain won't stop"
        )
        
        crisis = detector.assess_crisis(result)
        
        # Could be mixed or one of the types
        assert crisis.crisis_type in [CrisisType.FINANCIAL, CrisisType.HEALTH, CrisisType.MIXED]
    
    def test_severity_determination(self):
        """Test severity determination based on trigger count"""
        detector = CrisisDetector()
        
        # 3 triggers = high severity
        result_3 = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Test"
        )
        crisis_3 = detector.assess_crisis(result_3)
        assert crisis_3.severity == "high"
        
        # 5+ triggers = critical severity
        result_5 = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=5,
            detected_categories=["crisis_language"],
            original_input="Test"
        )
        crisis_5 = detector.assess_crisis(result_5)
        assert crisis_5.severity == "critical"
    
    def test_crisis_resources_provided(self):
        """Test that appropriate crisis resources are provided"""
        detector = CrisisDetector()
        
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Test"
        )
        
        crisis = detector.assess_crisis(result)
        
        # Should have mental health resources
        assert len(crisis.resources) > 0
        
        # Check resource structure
        resource = crisis.resources[0]
        assert resource.name
        assert resource.description
        assert resource.contact
        assert resource.availability
        assert resource.crisis_type
    
    def test_recommended_actions_mental_health(self):
        """Test recommended actions for mental health crisis"""
        detector = CrisisDetector()
        
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Test"
        )
        
        crisis = detector.assess_crisis(result)
        
        # Should have specific mental health actions
        actions = " ".join(crisis.recommended_actions)
        assert "988" in actions or "crisis" in actions.lower()
    
    def test_recommended_actions_financial(self):
        """Test recommended actions for financial crisis"""
        detector = CrisisDetector()
        
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["financial_desperation"],
            original_input="Test"
        )
        
        crisis = detector.assess_crisis(result)
        
        # Should have financial-specific actions
        actions = " ".join(crisis.recommended_actions)
        assert any(term in actions.lower() for term in ["credit", "financial", "211"])
    
    def test_format_crisis_message(self):
        """Test formatting of crisis message"""
        detector = CrisisDetector()
        
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Test"
        )
        
        crisis = detector.assess_crisis(result)
        message = crisis.format_crisis_message()
        
        # Message should be empathetic and include resources
        assert "difficult" in message.lower() or "serious" in message.lower()
        assert len(message) > 100  # Should be a substantial message
        
        # Should include resource information
        for resource in crisis.resources:
            assert resource.name in message
    
    def test_integration_with_vulnerability_detector(self):
        """Test integration between VulnerabilityDetector and CrisisDetector"""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()
        
        # Detect crisis
        detection = vuln_detector.detect(
            "I lost my job, this is my last hope, can't take it anymore"
        )
        
        # Should trigger crisis level
        assert detection.protection_level.value >= 3
        
        # Assess crisis
        crisis = crisis_detector.assess_crisis(detection)
        
        # Should produce valid crisis result
        assert crisis.crisis_type in [
            CrisisType.MENTAL_HEALTH,
            CrisisType.FINANCIAL,
            CrisisType.MIXED
        ]
        assert len(crisis.resources) > 0
        assert len(crisis.recommended_actions) > 0
    
    def test_vr24_crisis_detection_response(self):
        """Test VR-24 Crisis Detection & Response implementation"""
        detector = CrisisDetector()
        
        # VR-24 should handle various crisis types
        test_cases = [
            (["crisis_language"], CrisisType.MENTAL_HEALTH),
            (["financial_desperation"], CrisisType.FINANCIAL),
            (["health_crisis"], CrisisType.HEALTH),
        ]
        
        for categories, expected_type in test_cases:
            result = DetectionResult(
                protection_level=ProtectionLevel.CRISIS,
                triggers_count=3,
                detected_categories=categories,
                original_input="Test"
            )
            
            crisis = detector.assess_crisis(result)
            assert crisis.crisis_type == expected_type
    
    def test_isolation_maps_to_mental_health(self):
        """Test that isolation indicators map to mental health crisis"""
        detector = CrisisDetector()
        
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["isolation_indicators"],
            original_input="No one to talk to, completely alone"
        )
        
        crisis = detector.assess_crisis(result)
        
        # Isolation should map to mental health
        assert crisis.crisis_type == CrisisType.MENTAL_HEALTH
