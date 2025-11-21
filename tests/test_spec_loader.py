"""
Tests for the SpecificationLoader module.
"""


from lfas.spec_loader import SpecificationLoader


class TestSpecificationLoader:
    """Test suite for SpecificationLoader."""

    def test_loader_finds_default_spec(self) -> None:
        """Test that the loader can find the default specification file."""
        loader = SpecificationLoader()
        assert loader.spec_path.exists()
        assert loader.spec_path.name == "lfas-v4-specification.xml"

    def test_loader_loads_xml(self) -> None:
        """Test that the loader can parse the XML file."""
        loader = SpecificationLoader()
        loader.load()
        assert loader.tree is not None
        assert loader.root is not None
        assert loader.root.tag == "LFAS_Protocol_v4"

    def test_get_vulnerability_indicators(self) -> None:
        """Test extraction of vulnerability indicators."""
        loader = SpecificationLoader()
        indicators = loader.get_vulnerability_indicators()

        # Check that all expected categories are present
        assert "crisis_language" in indicators
        assert "financial_desperation" in indicators
        assert "health_crisis" in indicators
        assert "isolation_indicators" in indicators

        # Check that indicators were actually loaded
        assert len(indicators["crisis_language"]) > 0
        assert len(indicators["financial_desperation"]) > 0
        assert len(indicators["health_crisis"]) > 0
        assert len(indicators["isolation_indicators"]) > 0

    def test_crisis_language_indicators(self) -> None:
        """Test that crisis language indicators are loaded correctly."""
        loader = SpecificationLoader()
        indicators = loader.get_vulnerability_indicators()

        crisis_indicators = indicators["crisis_language"]

        # Check for known indicators from the spec
        assert any("last hope" in indicator.lower() for indicator in crisis_indicators)
        assert any("can't take it anymore" in indicator.lower() for indicator in crisis_indicators)
        assert any(
            "thinking about ending it" in indicator.lower() for indicator in crisis_indicators
        )

    def test_financial_desperation_indicators(self) -> None:
        """Test that financial desperation indicators are loaded correctly."""
        loader = SpecificationLoader()
        indicators = loader.get_vulnerability_indicators()

        financial_indicators = indicators["financial_desperation"]

        # Check for known indicators from the spec
        assert any("lost my job" in indicator.lower() for indicator in financial_indicators)
        assert any(
            "desperate for income" in indicator.lower() for indicator in financial_indicators
        )

    def test_get_verification_requirement(self) -> None:
        """Test extraction of verification requirements."""
        loader = SpecificationLoader()

        # Test VR-24 (Crisis Detection & Response)
        vr24 = loader.get_verification_requirement("VR-24")
        assert vr24 is not None
        assert vr24["code"] == "VR-24"
        assert vr24["name"] == "Crisis Detection & Response"
        assert "crisis" in vr24["description"].lower()

    def test_nonexistent_verification_requirement(self) -> None:
        """Test that requesting a nonexistent VR returns None."""
        loader = SpecificationLoader()
        vr99 = loader.get_verification_requirement("VR-99")
        assert vr99 is None

    def test_protection_escalation_rules(self) -> None:
        """Test extraction of protection escalation rules."""
        loader = SpecificationLoader()
        rules = loader.get_protection_escalation_rules()

        assert len(rules) > 0
        # Rules should reference protection levels
        rules_text = " ".join(rules.values()).lower()
        assert "level 1" in rules_text or "standard" in rules_text
        assert "level 3" in rules_text or "crisis" in rules_text
