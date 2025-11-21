"""Tests for CrisisDetectionSafeguard."""

from lfas_protocol import (
    CrisisDetectionSafeguard,
    DetectionResult,
    ProtectionLevel,
    VulnerabilityDetector,
)


class TestCrisisDetectionSafeguard:
    """Test suite for CrisisDetectionSafeguard (VR-24)."""

    def test_initialization(self):
        """Test safeguard initializes correctly."""
        safeguard = CrisisDetectionSafeguard()
        assert safeguard is not None

        resources = safeguard.get_crisis_resources()
        assert len(resources) >= 2  # At minimum 988 and Crisis Text Line

    def test_crisis_resources_content(self):
        """Test crisis resources contain required information."""
        safeguard = CrisisDetectionSafeguard()
        resources = safeguard.get_crisis_resources()

        # Check for 988 Lifeline
        has_988 = any("988" in r["name"] for r in resources)
        assert has_988, "Should include 988 Suicide & Crisis Lifeline"

        # Check for Crisis Text Line
        has_crisis_text = any("Crisis Text Line" in r["name"] for r in resources)
        assert has_crisis_text, "Should include Crisis Text Line"

        # Each resource should have required fields
        for resource in resources:
            assert "name" in resource
            assert "contact" in resource
            assert "availability" in resource
            assert "description" in resource

    def test_should_not_activate_standard_level(self):
        """Test safeguard doesn't activate for STANDARD protection level."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        result = detector.detect("What's the weather today?")
        assert not safeguard.should_activate(result)

    def test_should_not_activate_enhanced_level(self):
        """Test safeguard doesn't activate for ENHANCED protection level."""
        safeguard = CrisisDetectionSafeguard()

        # Manually create enhanced level result
        result = DetectionResult(text="test", trigger_count=2)
        result.protection_level = ProtectionLevel.ENHANCED

        assert not safeguard.should_activate(result)

    def test_should_activate_crisis_level(self):
        """Test safeguard activates for CRISIS protection level."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        result = detector.detect("I can't take it anymore, I'm broke and all alone, nobody cares")

        if result.protection_level == ProtectionLevel.CRISIS:
            assert safeguard.should_activate(result)

    def test_generate_standard_response(self):
        """Test response generation for STANDARD level."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        result = detector.detect("What's the weather today?")
        response = safeguard.generate_response(result)

        assert not response.should_activate
        assert response.protection_level == ProtectionLevel.STANDARD
        assert response.message == ""
        assert len(response.resources) == 0

    def test_generate_enhanced_response(self):
        """Test response generation for ENHANCED level."""
        safeguard = CrisisDetectionSafeguard()

        # Manually create enhanced level result
        result = DetectionResult(text="test", trigger_count=2)
        result.protection_level = ProtectionLevel.ENHANCED

        response = safeguard.generate_response(result)

        assert response.should_activate
        assert response.protection_level == ProtectionLevel.ENHANCED
        assert len(response.message) > 0
        assert "support" in response.message.lower() or "help" in response.message.lower()

    def test_generate_crisis_response(self):
        """Test response generation for CRISIS level."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        result = detector.detect(
            "I can't take it anymore, everything is hopeless and I'm all alone"
        )

        if result.protection_level == ProtectionLevel.CRISIS:
            response = safeguard.generate_response(result)

            assert response.should_activate
            assert response.protection_level == ProtectionLevel.CRISIS
            assert len(response.message) > 0
            assert len(response.resources) >= 2

            # Check for empathetic language
            message_lower = response.message.lower()
            assert any(word in message_lower for word in ["concern", "safety", "help", "support"])

            # Check for crisis resource mentions
            assert "988" in response.message or "741741" in response.message

    def test_crisis_response_includes_resources(self):
        """Test crisis response includes actual resource objects."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        result = detector.detect("I want to die, can't take it, nobody cares")

        if result.protection_level == ProtectionLevel.CRISIS:
            response = safeguard.generate_response(result)

            assert len(response.resources) >= 2
            for resource in response.resources:
                assert "name" in resource
                assert "contact" in resource

    def test_response_is_empathetic(self):
        """Test crisis response is empathetic and non-dismissive."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        result = detector.detect("I feel hopeless and can't go on, losing everything")

        if result.protection_level == ProtectionLevel.CRISIS:
            response = safeguard.generate_response(result)

            # Should not contain dismissive language
            message_lower = response.message.lower()
            dismissive_phrases = ["just", "simply", "don't worry", "it's not that bad"]
            assert not any(phrase in message_lower for phrase in dismissive_phrases)

            # Should contain supportive language
            assert any(word in message_lower for word in ["help", "support", "care"])

    def test_response_metadata(self):
        """Test response includes metadata about detected indicators."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        result = detector.detect("I'm hopeless and broke")
        response = safeguard.generate_response(result)

        if response.should_activate:
            assert "metadata" in response.__dict__
            assert isinstance(response.metadata, dict)
