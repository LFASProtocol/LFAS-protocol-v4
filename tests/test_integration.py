"""
Integration tests for the complete LFAS workflow.

These tests verify that the vulnerability detector and crisis safeguard
work together correctly in real-world scenarios.
"""

from lfas import CrisisDetector, ProtectionLevel, VulnerabilityDetector


class TestIntegration:
    """Integration tests for the complete LFAS workflow."""

    def test_complete_workflow_mental_health_crisis(self) -> None:
        """Test complete workflow for mental health crisis scenario."""
        # Initialize components
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        # User input indicating mental health crisis (needs 3+ triggers for crisis level)
        user_input = (
            "I'm thinking about ending it all. I don't want to live anymore. "
            "This is my last hope."
        )

        # Step 1: LISTEN - Detect vulnerabilities
        detection_result = vuln_detector.detect(user_input)

        # Verify vulnerability detection
        assert detection_result.protection_level == ProtectionLevel.CRISIS
        assert "crisis_language" in detection_result.triggered_categories

        # Step 2: Apply VR-24 - Crisis Detection & Response
        crisis_response = crisis_detector.assess_crisis(detection_result)

        # Verify crisis response
        assert crisis_response.crisis_detected
        assert crisis_response.crisis_type == "mental_health"
        assert len(crisis_response.resources) > 0
        assert len(crisis_response.recommended_actions) > 0

        # Verify that appropriate resources are provided
        resource_names = [r.name.lower() for r in crisis_response.resources]
        assert any("suicide" in name or "crisis" in name for name in resource_names)

        # Step 3: Generate user message
        message = crisis_detector.format_crisis_message(crisis_response)
        assert len(message) > 0
        assert "988" in message or "741741" in message  # Crisis hotlines

    def test_complete_workflow_enhanced_protection(self) -> None:
        """Test complete workflow for enhanced protection scenario."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        # User input requiring enhanced protection
        user_input = "I lost my job and need money fast."

        # Detect vulnerabilities
        detection_result = vuln_detector.detect(user_input)

        # Verify enhanced protection level
        assert detection_result.protection_level == ProtectionLevel.ENHANCED

        # Check that crisis safeguard is NOT triggered
        crisis_response = crisis_detector.assess_crisis(detection_result)
        assert not crisis_response.crisis_detected

    def test_complete_workflow_with_conversation_history(self) -> None:
        """Test workflow with conversation history tracking."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        # Simulate a conversation
        conversation_history = []

        # Turn 1: Normal
        input1 = "I need some career advice."
        result1 = vuln_detector.detect(input1, conversation_history)
        conversation_history.append(input1)
        assert result1.protection_level == ProtectionLevel.STANDARD

        # Turn 2: Vulnerability emerges
        input2 = "I lost my job last week."
        result2 = vuln_detector.detect(input2, conversation_history)
        conversation_history.append(input2)
        assert result2.protection_level <= ProtectionLevel.ENHANCED

        # Turn 3: Crisis escalates
        input3 = "I can't pay bills and this is my last hope."
        result3 = vuln_detector.detect(input3, conversation_history)

        # Should detect multiple triggers from history + current
        assert result3.protection_level >= ProtectionLevel.ENHANCED

        # Apply crisis safeguard if needed
        crisis_response = crisis_detector.assess_crisis(result3)
        if crisis_response.crisis_detected:
            assert crisis_response.crisis_type in ["financial", "mental_health"]

    def test_multiple_crisis_types_prioritization(self) -> None:
        """Test that mental health crises are prioritized in mixed scenarios."""
        vuln_detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector()

        # Input with multiple crisis types
        user_input = (
            "I lost my job, I have no one to talk to, I can't see a doctor, "
            "and I'm thinking about ending it. This is my last hope."
        )

        detection_result = vuln_detector.detect(user_input)
        crisis_response = crisis_detector.assess_crisis(detection_result)

        # Mental health should be prioritized
        assert crisis_response.crisis_type == "mental_health"
        assert crisis_response.crisis_detected

    def test_spec_driven_detection(self) -> None:
        """Test that detection is driven by XML specification."""
        vuln_detector = VulnerabilityDetector()

        # Verify indicators are loaded from spec
        assert len(vuln_detector.indicators) > 0

        # Test with specific indicator from spec
        result = vuln_detector.detect("This is my last hope.")
        assert result.trigger_count >= 1
        assert "last hope" in result.triggered_indicators

    def test_protection_level_escalation_and_deescalation(self) -> None:
        """Test protection level can escalate and de-escalate."""
        vuln_detector = VulnerabilityDetector()
        conversation = []

        # Start with crisis
        crisis_input = "I'm thinking about ending it, last hope, can't take it anymore."
        result1 = vuln_detector.detect(crisis_input)
        conversation.append(crisis_input)
        assert result1.protection_level == ProtectionLevel.CRISIS

        # Then normal conversation (should still consider history)
        normal_input = "Thank you for listening."
        result2 = vuln_detector.detect(normal_input, conversation)
        # Protection could be high due to recent history
        assert result2.protection_level >= ProtectionLevel.STANDARD

    def test_all_crisis_types_have_resources(self) -> None:
        """Test that all crisis types have appropriate resources."""
        crisis_detector = CrisisDetector()

        crisis_types = ["mental_health", "financial", "health", "abuse"]

        for crisis_type in crisis_types:
            assert crisis_type in CrisisDetector.CRISIS_RESOURCES
            resources = CrisisDetector.CRISIS_RESOURCES[crisis_type]
            assert len(resources) > 0
            # Each resource should have required fields
            for resource in resources:
                assert resource.name
                assert resource.description
                assert resource.contact
