"""
Tests for vulnerability detector.
"""

from lfas_protocol import VulnerabilityDetector, ProtectionLevel


def test_detector_initialization():
    """Test detector can be initialized."""
    detector = VulnerabilityDetector()
    assert detector is not None


def test_no_triggers_standard_protection():
    """Test that normal messages get Standard protection level."""
    detector = VulnerabilityDetector()
    result = detector.analyze("Hello, can you help me with Python?")

    assert result["trigger_count"] == 0
    assert result["protection_level"] == ProtectionLevel.STANDARD
    assert len(result["triggers"]) == 0


def test_crisis_language_detection():
    """Test detection of crisis language."""
    detector = VulnerabilityDetector()
    result = detector.analyze("This is my last hope, I can't take it anymore")

    assert result["trigger_count"] >= 1
    assert "crisis_language" in result["triggers"]
    assert result["protection_level"] in [ProtectionLevel.ENHANCED, ProtectionLevel.CRISIS]


def test_financial_desperation_detection():
    """Test detection of financial crisis indicators."""
    detector = VulnerabilityDetector()
    result = detector.analyze("I lost my job and have my last $100")

    assert "financial_desperation" in result["triggers"]
    assert result["protection_level"] in [ProtectionLevel.ENHANCED, ProtectionLevel.CRISIS]


def test_multiple_triggers_crisis_level():
    """Test that multiple triggers escalate to Crisis level."""
    detector = VulnerabilityDetector()
    result = detector.analyze(
        "I lost my job, this is my last hope, I'm completely alone, no one to talk to"
    )

    assert result["trigger_count"] >= 3
    assert result["protection_level"] == ProtectionLevel.CRISIS


def test_demonstration_scenario_1():
    """
    Test Scenario 1 from demonstrations/lfas-basic-demo.md
    User: "I lost my job and have $100 left. I need to make money fast."
    """
    detector = VulnerabilityDetector()
    result = detector.analyze("I lost my job and have $100 left. I need to make money fast.")

    # Should detect financial desperation
    assert "financial_desperation" in result["triggers"]
    # Should be at least Enhanced protection
    assert result["protection_level"] in [ProtectionLevel.ENHANCED, ProtectionLevel.CRISIS]


def test_demonstration_scenario_2():
    """
    Test Scenario 2 from demonstrations/lfas-basic-demo.md
    User: "I can't take it anymore, everything is hopeless"
    """
    detector = VulnerabilityDetector()
    result = detector.analyze("I can't take it anymore, everything is hopeless")

    # Should detect crisis language
    assert "crisis_language" in result["triggers"]
    # Should trigger crisis or enhanced protection
    assert result["protection_level"] in [ProtectionLevel.ENHANCED, ProtectionLevel.CRISIS]


def test_case_insensitive_detection():
    """Test that detection is case-insensitive."""
    detector = VulnerabilityDetector()
    result1 = detector.analyze("I LOST MY JOB")
    result2 = detector.analyze("i lost my job")
    result3 = detector.analyze("I Lost My Job")

    assert result1["trigger_count"] > 0
    assert result2["trigger_count"] > 0
    assert result3["trigger_count"] > 0


def test_matched_phrases_returned():
    """Test that matched phrases are returned in results."""
    detector = VulnerabilityDetector()
    result = detector.analyze("This is my last hope and I lost my job")

    assert len(result["matched_phrases"]) > 0
    assert any("last hope" in phrase.lower() for phrase in result["matched_phrases"])
    assert any("lost my job" in phrase.lower() for phrase in result["matched_phrases"])


def test_categories_count():
    """Test that category counts are accurate."""
    detector = VulnerabilityDetector()
    result = detector.analyze("I lost my job, can't pay bills, facing eviction")

    assert "financial_desperation" in result["categories"]
    assert result["categories"]["financial_desperation"] >= 3
