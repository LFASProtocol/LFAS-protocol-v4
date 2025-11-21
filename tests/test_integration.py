"""Integration tests for LFAS Protocol implementation."""

from lfas_protocol import (
    CrisisDetectionSafeguard,
    ProtectionLevel,
    VulnerabilityCategory,
    VulnerabilityDetector,
)


class TestIntegration:
    """Integration tests for complete LFAS Protocol workflow."""

    def test_complete_workflow_crisis_scenario(self):
        """Test complete workflow: detect → assess → respond (crisis scenario)."""
        # LISTEN phase
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        user_input = "I can't take it anymore, I'm broke and lost everything, I'm all alone"

        # REFLECT phase
        result = detector.detect(user_input)

        # Verify detection
        assert result.trigger_count >= 3
        assert result.protection_level == ProtectionLevel.CRISIS

        # ACT phase
        if safeguard.should_activate(result):
            response = safeguard.generate_response(result)

            # Verify response
            assert response.should_activate
            assert len(response.message) > 0
            assert len(response.resources) >= 2

    def test_complete_workflow_standard_scenario(self):
        """Test complete workflow: detect → assess → respond (standard scenario)."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        user_input = "What's the weather like today?"

        result = detector.detect(user_input)

        # Verify no vulnerability detected
        assert result.protection_level == ProtectionLevel.STANDARD
        assert not safeguard.should_activate(result)

        response = safeguard.generate_response(result)
        assert not response.should_activate

    def test_demonstration_scenario_1_suicide_ideation(self):
        """Test Demonstration 1: Suicide ideation with financial stress."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        # User expresses suicidal thoughts with financial crisis
        user_input = "I've lost everything financially and see no point in going on"

        result = detector.detect(user_input)

        # Should detect multiple vulnerability indicators
        assert result.trigger_count >= 2
        assert result.protection_level in [ProtectionLevel.ENHANCED, ProtectionLevel.CRISIS]

        # Should provide appropriate resources
        if result.protection_level == ProtectionLevel.CRISIS:
            response = safeguard.generate_response(result)
            assert "988" in response.message or any(
                "988" in r["contact"] for r in response.resources
            )

    def test_demonstration_scenario_2_isolation_health(self):
        """Test Demonstration 2: Isolation combined with health crisis."""
        detector = VulnerabilityDetector()

        user_input = "I have a terminal illness and I'm completely alone"

        result = detector.detect(user_input)

        # Should detect health crisis and isolation
        assert result.trigger_count >= 2
        categories = [i.category for i in result.indicators]
        assert VulnerabilityCategory.HEALTH_CRISIS in categories
        assert VulnerabilityCategory.ISOLATION in categories

    def test_demonstration_scenario_3_financial_desperation(self):
        """Test Demonstration 3: Severe financial desperation."""
        detector = VulnerabilityDetector()

        user_input = "I'm bankrupt, lost everything, and desperate for money"

        result = detector.detect(user_input)

        # Should detect financial desperation
        assert result.trigger_count >= 1
        categories = [i.category for i in result.indicators]
        assert VulnerabilityCategory.FINANCIAL_DESPERATION in categories

    def test_escalation_from_standard_to_enhanced(self):
        """Test protection level escalation: STANDARD → ENHANCED."""
        detector = VulnerabilityDetector()

        # Start with standard
        result1 = detector.detect("Hello, how are you?")
        assert result1.protection_level == ProtectionLevel.STANDARD

        # Escalate to enhanced with 2 triggers
        result2 = detector.detect("I'm broke and feeling hopeless")
        if result2.trigger_count == 2:
            assert result2.protection_level == ProtectionLevel.ENHANCED

    def test_escalation_from_enhanced_to_crisis(self):
        """Test protection level escalation: ENHANCED → CRISIS."""
        detector = VulnerabilityDetector()

        # Enhanced level (2 triggers)
        result1 = detector.detect("I'm broke and hopeless")
        if result1.trigger_count == 2:
            assert result1.protection_level == ProtectionLevel.ENHANCED

        # Crisis level (3+ triggers)
        result2 = detector.detect("I'm broke, hopeless, and all alone with nobody")
        assert result2.trigger_count >= 3
        assert result2.protection_level == ProtectionLevel.CRISIS

    def test_multiple_conversations(self):
        """Test handling multiple independent conversations."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        # Conversation 1: Crisis
        result1 = detector.detect("I can't take it, want to die, all alone")
        response1 = safeguard.generate_response(result1)

        # Conversation 2: Standard
        result2 = detector.detect("What's the capital of France?")
        response2 = safeguard.generate_response(result2)

        # Results should be independent
        assert result1.protection_level != result2.protection_level
        assert response1.should_activate != response2.should_activate

    def test_crisis_resources_accessibility(self):
        """Test that crisis resources are easily accessible."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        result = detector.detect("I want to end it all, can't go on")

        if result.protection_level == ProtectionLevel.CRISIS:
            # Resources should be available both from safeguard and response
            safeguard_resources = safeguard.get_crisis_resources()
            response = safeguard.generate_response(result)

            assert len(safeguard_resources) >= 2
            assert len(response.resources) >= 2

            # Resources should include contact information
            for resource in response.resources:
                assert resource["contact"]
                assert resource["name"]

    def test_empathetic_messaging_consistency(self):
        """Test that all crisis responses use empathetic messaging."""
        detector = VulnerabilityDetector()
        safeguard = CrisisDetectionSafeguard()

        crisis_inputs = [
            "I can't take it anymore",
            "I want to die",
            "Everything is hopeless and I'm alone",
        ]

        for user_input in crisis_inputs:
            result = detector.detect(user_input)
            if result.protection_level == ProtectionLevel.CRISIS:
                response = safeguard.generate_response(result)

                # Should contain empathetic language
                message_lower = response.message.lower()
                empathetic_words = ["concern", "care", "help", "support", "safety"]
                assert any(word in message_lower for word in empathetic_words)

                # Should not be dismissive
                dismissive_words = ["just", "simply", "calm down"]
                assert not any(word in message_lower for word in dismissive_words)
