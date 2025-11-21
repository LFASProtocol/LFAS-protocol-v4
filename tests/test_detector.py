"""
Tests for the VulnerabilityDetector module.
"""


from lfas.detector import ProtectionLevel, VulnerabilityDetector


class TestVulnerabilityDetector:
    """Test suite for VulnerabilityDetector."""

    def test_detector_initializes(self) -> None:
        """Test that the detector initializes successfully."""
        detector = VulnerabilityDetector()
        assert detector is not None
        assert len(detector.indicators) > 0

    def test_detector_has_all_categories(self) -> None:
        """Test that all expected indicator categories are loaded."""
        detector = VulnerabilityDetector()
        categories = detector.get_indicator_categories()

        assert "crisis_language" in categories
        assert "financial_desperation" in categories
        assert "health_crisis" in categories
        assert "isolation_indicators" in categories

    def test_no_triggers_standard_level(self) -> None:
        """Test that clean input results in standard protection level."""
        detector = VulnerabilityDetector()
        result = detector.detect("I'm learning Python programming today.")

        assert result.protection_level == ProtectionLevel.STANDARD
        assert result.trigger_count == 0
        assert len(result.triggered_indicators) == 0
        assert len(result.triggered_categories) == 0

    def test_one_trigger_standard_level(self) -> None:
        """Test that one trigger still results in standard protection level."""
        detector = VulnerabilityDetector()
        result = detector.detect("I lost my job recently but I'm doing okay.")

        assert result.protection_level == ProtectionLevel.STANDARD
        assert result.trigger_count == 1
        assert len(result.triggered_indicators) == 1

    def test_two_triggers_enhanced_level(self) -> None:
        """Test that two triggers result in enhanced protection level."""
        detector = VulnerabilityDetector()
        # Use exactly 2 triggers
        result = detector.detect("I lost my job and need money fast.")

        assert result.protection_level == ProtectionLevel.ENHANCED
        assert result.trigger_count == 2
        assert "financial_desperation" in result.triggered_categories

    def test_three_triggers_crisis_level(self) -> None:
        """Test that three or more triggers result in crisis protection level."""
        detector = VulnerabilityDetector()
        result = detector.detect(
            "I lost my job, this is my last hope, I can't take it anymore. "
            "I'm completely alone in this."
        )

        assert result.protection_level == ProtectionLevel.CRISIS
        assert result.trigger_count >= 3
        assert len(result.triggered_categories) >= 2

    def test_crisis_language_detection(self) -> None:
        """Test detection of crisis language indicators."""
        detector = VulnerabilityDetector()
        result = detector.detect("This is my last hope, I can't take it anymore.")

        assert result.trigger_count >= 2
        assert "crisis_language" in result.triggered_categories

    def test_suicidal_ideation_detection(self) -> None:
        """Test detection of suicidal ideation."""
        detector = VulnerabilityDetector()
        # Use three separate triggers to ensure CRISIS level
        result = detector.detect(
            "I'm thinking about ending it all, I don't want to live anymore, this is my last hope."
        )

        assert result.protection_level == ProtectionLevel.CRISIS
        assert "crisis_language" in result.triggered_categories
        assert result.trigger_count >= 3

    def test_financial_crisis_detection(self) -> None:
        """Test detection of financial desperation."""
        detector = VulnerabilityDetector()
        result = detector.detect("I'm desperate for income, this is my last $100.")

        assert result.trigger_count >= 2
        assert "financial_desperation" in result.triggered_categories

    def test_health_crisis_detection(self) -> None:
        """Test detection of health crisis indicators."""
        detector = VulnerabilityDetector()
        result = detector.detect(
            "I can't see a doctor, I have no insurance and the pain won't stop."
        )

        assert result.trigger_count >= 2
        assert "health_crisis" in result.triggered_categories

    def test_isolation_detection(self) -> None:
        """Test detection of isolation indicators."""
        detector = VulnerabilityDetector()
        result = detector.detect("I have no one to talk to, you're the only one who listens.")

        assert result.trigger_count >= 2
        assert "isolation_indicators" in result.triggered_categories

    def test_case_insensitive_detection(self) -> None:
        """Test that detection is case-insensitive."""
        detector = VulnerabilityDetector()

        result1 = detector.detect("LAST HOPE")
        result2 = detector.detect("last hope")
        result3 = detector.detect("Last Hope")

        assert result1.trigger_count > 0
        assert result2.trigger_count > 0
        assert result3.trigger_count > 0

    def test_conversation_history_context(self) -> None:
        """Test that conversation history is considered for context."""
        detector = VulnerabilityDetector()

        history = [
            "I lost my job last week.",
            "I can't pay my bills anymore.",
        ]
        result = detector.detect("This is my last hope.", conversation_history=history)

        # Should detect triggers from both current input and history
        # "lost my job", "can't pay bills", "last hope" = 3 triggers
        assert result.trigger_count >= 2  # At least 2 for enhanced protection
        assert result.protection_level >= ProtectionLevel.ENHANCED

    def test_detection_result_repr(self) -> None:
        """Test the string representation of DetectionResult."""
        detector = VulnerabilityDetector()
        result = detector.detect("I'm thinking about ending it.")

        repr_str = repr(result)
        assert "DetectionResult" in repr_str
        assert "triggers=" in repr_str
        assert "categories=" in repr_str

    def test_get_indicators_for_category(self) -> None:
        """Test retrieval of indicators for a specific category."""
        detector = VulnerabilityDetector()

        crisis_indicators = detector.get_indicators_for_category("crisis_language")
        assert len(crisis_indicators) > 0
        assert any("last hope" in indicator.lower() for indicator in crisis_indicators)

    def test_get_indicators_for_nonexistent_category(self) -> None:
        """Test that requesting indicators for a nonexistent category returns empty list."""
        detector = VulnerabilityDetector()

        indicators = detector.get_indicators_for_category("nonexistent_category")
        assert indicators == []

    def test_multiple_categories_triggered(self) -> None:
        """Test scenario where multiple vulnerability categories are triggered."""
        detector = VulnerabilityDetector()
        result = detector.detect(
            "I lost my job, I have no one to talk to, and I can't see a doctor. "
            "This is my last hope."
        )

        assert result.protection_level == ProtectionLevel.CRISIS
        assert len(result.triggered_categories) >= 3
        assert "crisis_language" in result.triggered_categories
        assert "financial_desperation" in result.triggered_categories
        assert "isolation_indicators" in result.triggered_categories

    def test_protection_level_enum_values(self) -> None:
        """Test that ProtectionLevel enum has correct values."""
        assert ProtectionLevel.STANDARD == 1
        assert ProtectionLevel.ENHANCED == 2
        assert ProtectionLevel.CRISIS == 3

        # Test that they can be compared
        assert ProtectionLevel.CRISIS > ProtectionLevel.ENHANCED
        assert ProtectionLevel.ENHANCED > ProtectionLevel.STANDARD
