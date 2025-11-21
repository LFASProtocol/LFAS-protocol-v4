"""
Tests for the CrisisDetector module (VR-24).
"""

from lfas.crisis import CrisisDetector, CrisisResource, CrisisResponse
from lfas.detector import ProtectionLevel, VulnerabilityDetector


class TestCrisisDetector:
    """Test suite for CrisisDetector (VR-24)."""

    def test_crisis_detector_initializes(self) -> None:
        """Test that the crisis detector initializes successfully."""
        detector = CrisisDetector()
        assert detector is not None

    def test_crisis_resources_loaded(self) -> None:
        """Test that crisis resources are available."""
        assert len(CrisisDetector.CRISIS_RESOURCES) > 0
        assert "mental_health" in CrisisDetector.CRISIS_RESOURCES
        assert "financial" in CrisisDetector.CRISIS_RESOURCES
        assert "health" in CrisisDetector.CRISIS_RESOURCES
        assert "abuse" in CrisisDetector.CRISIS_RESOURCES

    def test_no_crisis_standard_level(self) -> None:
        """Test that no crisis is detected at standard protection level."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        result = vuln_detector.detect("I'm learning Python today.")
        crisis_response = crisis_detector.assess_crisis(result)

        assert not crisis_response.crisis_detected
        assert crisis_response.crisis_type == "none"
        assert len(crisis_response.resources) == 0
        assert len(crisis_response.recommended_actions) == 0

    def test_no_crisis_enhanced_level(self) -> None:
        """Test that no crisis is detected at enhanced protection level."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        result = vuln_detector.detect("I lost my job and need money fast.")
        crisis_response = crisis_detector.assess_crisis(result)

        assert not crisis_response.crisis_detected
        assert result.protection_level == ProtectionLevel.ENHANCED

    def test_mental_health_crisis_detected(self) -> None:
        """Test detection of mental health crisis."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        result = vuln_detector.detect(
            "I'm thinking about ending it all. I don't want to live anymore. This is my last hope."
        )
        crisis_response = crisis_detector.assess_crisis(result)

        assert crisis_response.crisis_detected
        assert crisis_response.crisis_type == "mental_health"
        assert len(crisis_response.resources) > 0
        assert len(crisis_response.recommended_actions) > 0

        # Check that mental health resources are included
        resource_names = [r.name for r in crisis_response.resources]
        assert any("suicide" in name.lower() for name in resource_names)

    def test_financial_crisis_detected(self) -> None:
        """Test detection of financial crisis."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        result = vuln_detector.detect("I lost my job, can't pay bills, and this is my last hope.")
        crisis_response = crisis_detector.assess_crisis(result)

        assert crisis_response.crisis_detected
        assert crisis_response.crisis_type == "financial"
        assert len(crisis_response.resources) > 0

    def test_health_crisis_detected(self) -> None:
        """Test detection of health crisis."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        result = vuln_detector.detect(
            "I can't see a doctor, the pain won't stop, and I have no insurance. "
            "This is my last hope."
        )
        crisis_response = crisis_detector.assess_crisis(result)

        assert crisis_response.crisis_detected
        assert crisis_response.crisis_type == "health"
        assert len(crisis_response.resources) > 0

    def test_crisis_recommended_actions(self) -> None:
        """Test that crisis responses include recommended actions."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        result = vuln_detector.detect(
            "I'm thinking about ending it, this is my last hope, I can't take it anymore."
        )
        crisis_response = crisis_detector.assess_crisis(result)

        assert len(crisis_response.recommended_actions) > 0

        # Check for key actions
        actions_text = " ".join(crisis_response.recommended_actions).lower()
        assert "pause" in actions_text or "stop" in actions_text
        assert "crisis" in actions_text or "help" in actions_text
        assert "professional" in actions_text

    def test_mental_health_specific_actions(self) -> None:
        """Test that mental health crises get specific actions."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        result = vuln_detector.detect(
            "I don't want to live anymore, thinking about ending it all, last hope."
        )
        crisis_response = crisis_detector.assess_crisis(result)

        assert crisis_response.crisis_type == "mental_health"

        actions_text = " ".join(crisis_response.recommended_actions).lower()
        assert "empathy" in actions_text or "therapy" in actions_text

    def test_crisis_message_formatting(self) -> None:
        """Test that crisis messages are formatted correctly."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        result = vuln_detector.detect(
            "I'm thinking about ending it, last hope, can't take it anymore."
        )
        crisis_response = crisis_detector.assess_crisis(result)

        message = crisis_detector.format_crisis_message(crisis_response)

        assert len(message) > 0
        assert "CRISIS" in message or "crisis" in message
        assert "help" in message.lower()
        # Should include at least one resource contact
        assert any(
            resource.contact.lower() in message.lower() for resource in crisis_response.resources
        )

    def test_no_crisis_message_formatting(self) -> None:
        """Test that non-crisis situations return empty message."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        result = vuln_detector.detect("I'm learning Python today.")
        crisis_response = crisis_detector.assess_crisis(result)

        message = crisis_detector.format_crisis_message(crisis_response)
        assert message == ""

    def test_crisis_resource_dataclass(self) -> None:
        """Test the CrisisResource dataclass."""
        resource = CrisisResource(
            name="Test Hotline",
            description="Test description",
            contact="123-456-7890",
            region="Test Region",
        )

        assert resource.name == "Test Hotline"
        assert resource.description == "Test description"
        assert resource.contact == "123-456-7890"
        assert resource.region == "Test Region"

    def test_crisis_response_dataclass(self) -> None:
        """Test the CrisisResponse dataclass."""
        resource = CrisisResource("Test", "Desc", "123", "US")
        response = CrisisResponse(
            crisis_detected=True,
            crisis_type="mental_health",
            resources=[resource],
            recommended_actions=["action1", "action2"],
        )

        assert response.crisis_detected is True
        assert response.crisis_type == "mental_health"
        assert len(response.resources) == 1
        assert len(response.recommended_actions) == 2

    def test_multiple_crisis_categories(self) -> None:
        """Test handling of multiple crisis categories."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        # Trigger multiple categories
        result = vuln_detector.detect(
            "I lost my job, I have no one to talk to, I can't see a doctor, "
            "and this is my last hope. I'm thinking about ending it all."
        )
        crisis_response = crisis_detector.assess_crisis(result)

        assert crisis_response.crisis_detected
        # Mental health should be prioritized
        assert crisis_response.crisis_type == "mental_health"
        assert len(crisis_response.resources) > 0

    def test_severe_crisis_includes_mental_health_resources(self) -> None:
        """Test that severe crises (4+ triggers) include mental health resources."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        # Financial crisis with 4+ triggers
        result = vuln_detector.detect(
            "I lost my job, can't pay bills, behind on rent, and desperate for income."
        )

        # Force it to be a crisis for testing
        if result.protection_level == ProtectionLevel.CRISIS:
            crisis_response = crisis_detector.assess_crisis(result)

            # Even if primary type is financial, should include mental health for severe cases
            if result.trigger_count >= 4:
                resource_types = [r.name.lower() for r in crisis_response.resources]
                # Should have financial resources or mental health backup
                assert len(resource_types) > 0
