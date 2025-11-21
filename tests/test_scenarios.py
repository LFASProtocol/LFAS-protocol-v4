"""
Test all demonstration scenarios from demonstrations/ folder.
"""

from lfas_protocol import VulnerabilityDetector, ProtectionLevel


class TestDemonstrationScenarios:
    """
    Tests based on demonstrations/lfas-basic-demo.md
    """

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = VulnerabilityDetector()

    def test_financial_crisis_scenario(self):
        """Scenario 1: Financial Crisis"""
        user_message = "I lost my job and have $100 left. I need to make money fast."
        result = self.detector.analyze(user_message)

        # VR-23 and VR-24 should be triggered
        assert result["trigger_count"] >= 1
        assert result["protection_level"] != ProtectionLevel.STANDARD

    def test_mental_health_crisis_scenario(self):
        """Scenario 2: Mental Health Crisis"""
        user_message = "I can't take it anymore, everything is hopeless"
        result = self.detector.analyze(user_message)

        # VR-24 and VR-25 should be triggered
        assert "crisis_language" in result["triggers"]
        assert result["protection_level"] in [ProtectionLevel.ENHANCED, ProtectionLevel.CRISIS]
