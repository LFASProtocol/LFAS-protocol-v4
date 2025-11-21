"""
Tests for LFAS Protocol v4 - Specification Loader
"""

import pytest
from pathlib import Path
from lfas.spec_loader import SpecificationLoader


class TestSpecificationLoader:
    """Tests for SpecificationLoader"""
    
    def test_load_default_specification(self):
        """Test loading the default XML specification"""
        loader = SpecificationLoader()
        assert loader.spec_path.exists()
        assert loader._tree is not None
        assert loader._root is not None
    
    def test_load_custom_specification(self):
        """Test loading a custom specification path"""
        spec_path = Path(__file__).parent.parent / "protocol" / "lfas-v4-specification.xml"
        loader = SpecificationLoader(str(spec_path))
        assert loader.spec_path == spec_path
    
    def test_get_detection_indicators(self):
        """Test extracting detection indicators"""
        loader = SpecificationLoader()
        indicators = loader.get_detection_indicators()
        
        # Should have all four categories
        assert "crisis_language" in indicators
        assert "financial_desperation" in indicators
        assert "health_crisis" in indicators
        assert "isolation_indicators" in indicators
        
        # Each category should have indicators
        assert len(indicators["crisis_language"]) > 0
        assert len(indicators["financial_desperation"]) > 0
        assert len(indicators["health_crisis"]) > 0
        assert len(indicators["isolation_indicators"]) > 0
    
    def test_indicators_are_parsed(self):
        """Test that indicators are properly parsed from XML"""
        loader = SpecificationLoader()
        indicators = loader.get_detection_indicators()
        
        # Check for known indicators
        crisis_indicators = indicators.get("crisis_language", [])
        
        # The indicators should be split and stripped
        assert any("last hope" in ind.lower() for ind in crisis_indicators)
    
    def test_get_protection_rules(self):
        """Test extracting protection escalation rules"""
        loader = SpecificationLoader()
        rules = loader.get_protection_rules()
        
        # Should have rules defined
        assert len(rules) > 0
        
        # Check for specific rule patterns
        rule_text = " ".join(rules.values())
        assert "Standard Protection" in rule_text or "Level 1" in rule_text
    
    def test_get_crisis_resources(self):
        """Test extracting crisis resources"""
        loader = SpecificationLoader()
        resources = loader.get_crisis_resources()
        
        # Should have resources for all crisis types
        assert "mental_health" in resources
        assert "financial" in resources
        assert "health" in resources
        assert "abuse" in resources
        
        # Mental health should have 988 Lifeline
        mh_resources = resources["mental_health"]
        assert len(mh_resources) > 0
        assert any("988" in r["contact"] for r in mh_resources)
    
    def test_get_verification_requirements(self):
        """Test extracting verification requirements"""
        loader = SpecificationLoader()
        requirements = loader.get_verification_requirements()
        
        # Should have VR-20 through VR-25
        assert "VR-20" in requirements
        assert "VR-22" in requirements
        assert "VR-23" in requirements
        assert "VR-24" in requirements
        assert "VR-25" in requirements
        
        # VR-24 should be Crisis Detection & Response
        vr24 = requirements["VR-24"]
        assert "Crisis" in vr24["name"]
        assert vr24["description"]
    
    def test_reload_specification(self):
        """Test reloading the specification"""
        loader = SpecificationLoader()
        original_indicators = loader.get_detection_indicators()
        
        loader.reload()
        reloaded_indicators = loader.get_detection_indicators()
        
        # Should be the same after reload
        assert original_indicators.keys() == reloaded_indicators.keys()
    
    def test_invalid_spec_path_raises_error(self):
        """Test that invalid spec path raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            SpecificationLoader("/nonexistent/path/spec.xml")
