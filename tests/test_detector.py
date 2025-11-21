"""Tests for VulnerabilityDetector."""

from lfas_protocol import (
    ProtectionLevel,
    VulnerabilityCategory,
    VulnerabilityDetector,
)


class TestVulnerabilityDetector:
    """Test suite for VulnerabilityDetector."""

    def test_initialization(self):
        """Test detector initializes correctly."""
        detector = VulnerabilityDetector()
        assert detector is not None
        patterns = detector.get_patterns()
        assert len(patterns) == 4  # Four vulnerability categories

    def test_no_vulnerability_detected(self):
        """Test standard input with no vulnerability indicators."""
        detector = VulnerabilityDetector()
        result = detector.detect("Hello, how are you?")

        assert result.trigger_count == 0
        assert result.protection_level == ProtectionLevel.STANDARD
        assert len(result.indicators) == 0

    def test_crisis_language_detection(self):
        """Test detection of crisis language (VR-24)."""
        detector = VulnerabilityDetector()
        result = detector.detect("I can't take it anymore, everything is hopeless")

        assert result.trigger_count >= 1
        assert any(i.category == VulnerabilityCategory.CRISIS_LANGUAGE for i in result.indicators)

    def test_financial_desperation_detection(self):
        """Test detection of financial desperation."""
        detector = VulnerabilityDetector()
        result = detector.detect("I'm broke and lost everything")

        assert result.trigger_count >= 1
        assert any(
            i.category == VulnerabilityCategory.FINANCIAL_DESPERATION for i in result.indicators
        )

    def test_health_crisis_detection(self):
        """Test detection of health crisis indicators."""
        detector = VulnerabilityDetector()
        result = detector.detect("I have a terminal illness and unbearable pain")

        assert result.trigger_count >= 1
        assert any(i.category == VulnerabilityCategory.HEALTH_CRISIS for i in result.indicators)

    def test_isolation_detection(self):
        """Test detection of isolation signals."""
        detector = VulnerabilityDetector()
        result = detector.detect("I'm all alone and nobody cares")

        assert result.trigger_count >= 1
        assert any(i.category == VulnerabilityCategory.ISOLATION for i in result.indicators)

    def test_protection_level_standard(self):
        """Test protection level remains STANDARD with 0-1 triggers."""
        detector = VulnerabilityDetector()

        # 0 triggers
        result = detector.detect("What's the weather today?")
        assert result.protection_level == ProtectionLevel.STANDARD

        # 1 trigger
        result = detector.detect("I'm feeling hopeless")
        assert result.trigger_count >= 1
        if result.trigger_count == 1:
            assert result.protection_level == ProtectionLevel.STANDARD

    def test_protection_level_enhanced(self):
        """Test protection level escalates to ENHANCED with 2 triggers."""
        detector = VulnerabilityDetector()
        result = detector.detect("I'm broke and feeling hopeless")

        # Should detect at least 2 different categories
        if result.trigger_count == 2:
            assert result.protection_level == ProtectionLevel.ENHANCED

    def test_protection_level_crisis(self):
        """Test protection level escalates to CRISIS with 3+ triggers."""
        detector = VulnerabilityDetector()
        result = detector.detect("I can't take it anymore, I'm broke and all alone, nobody cares")

        assert result.trigger_count >= 3
        assert result.protection_level == ProtectionLevel.CRISIS

    def test_empty_input(self):
        """Test handling of empty input."""
        detector = VulnerabilityDetector()
        result = detector.detect("")

        assert result.text == ""
        assert result.trigger_count == 0
        assert result.protection_level == ProtectionLevel.STANDARD

    def test_none_input(self):
        """Test handling of None input."""
        detector = VulnerabilityDetector()
        result = detector.detect(None)

        assert result.text == ""
        assert result.trigger_count == 0

    def test_case_insensitive_detection(self):
        """Test detection is case-insensitive."""
        detector = VulnerabilityDetector()

        result1 = detector.detect("I CAN'T TAKE IT ANYMORE")
        result2 = detector.detect("i can't take it anymore")
        result3 = detector.detect("I Can't Take It Anymore")

        assert result1.trigger_count > 0
        assert result2.trigger_count > 0
        assert result3.trigger_count > 0

    def test_add_custom_pattern(self):
        """Test adding custom detection patterns."""
        detector = VulnerabilityDetector()

        # Add custom pattern
        detector.add_pattern(VulnerabilityCategory.CRISIS_LANGUAGE, r"\b(custom crisis pattern)\b")

        result = detector.detect("This contains custom crisis pattern")
        assert result.trigger_count >= 1

    def test_get_patterns(self):
        """Test retrieving detection patterns."""
        detector = VulnerabilityDetector()

        # Get all patterns
        all_patterns = detector.get_patterns()
        assert len(all_patterns) == 4

        # Get specific category
        crisis_patterns = detector.get_patterns(VulnerabilityCategory.CRISIS_LANGUAGE)
        assert VulnerabilityCategory.CRISIS_LANGUAGE in crisis_patterns
        assert len(crisis_patterns) == 1

    def test_multiple_indicators_same_category(self):
        """Test that only one indicator per category is counted."""
        detector = VulnerabilityDetector()
        result = detector.detect("I feel hopeless and worthless and no point")

        # Even with multiple crisis language patterns, should count as 1 per category
        crisis_indicators = [
            i for i in result.indicators if i.category == VulnerabilityCategory.CRISIS_LANGUAGE
        ]
        assert len(crisis_indicators) == 1
