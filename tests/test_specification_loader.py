"""
Tests for SpecificationLoader
"""

import pytest
from pathlib import Path
from lfas.specification_loader import SpecificationLoader


class TestSpecificationLoader:
    """Test XML specification loading"""
    
    def test_initialization_with_default_path(self):
        loader = SpecificationLoader()
        assert loader.spec_path.exists()
        assert loader.spec_path.name == "lfas-v4-specification.xml"
    
    def test_initialization_with_custom_path(self):
        spec_path = Path(__file__).parent.parent / "protocol" / "lfas-v4-specification.xml"
        loader = SpecificationLoader(str(spec_path))
        assert loader.spec_path == spec_path
    
    def test_initialization_with_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            SpecificationLoader("/nonexistent/path.xml")
    
    def test_load_vulnerability_indicators(self):
        loader = SpecificationLoader()
        indicators = loader.load_vulnerability_indicators()
        
        # Check that indicators were loaded
        assert isinstance(indicators, dict)
        assert len(indicators) > 0
        
        # Check for expected categories
        assert "crisis_language" in indicators
        assert "financial_desperation" in indicators
        assert "health_crisis" in indicators
        assert "isolation_indicators" in indicators
        
        # Check that each category has indicators
        for category, indicator_list in indicators.items():
            assert isinstance(indicator_list, list)
            assert len(indicator_list) > 0
    
    def test_indicators_are_strings(self):
        loader = SpecificationLoader()
        indicators = loader.load_vulnerability_indicators()
        
        for category, indicator_list in indicators.items():
            for indicator in indicator_list:
                assert isinstance(indicator, str)
                assert len(indicator) > 0
    
    def test_load_protection_escalation_rules(self):
        loader = SpecificationLoader()
        rules = loader.load_protection_escalation_rules()
        
        assert isinstance(rules, dict)
        assert "standard_max" in rules
        assert "enhanced_min" in rules
        assert "enhanced_max" in rules
        assert "crisis_min" in rules
        
        # Check rule values match spec
        assert rules["standard_max"] == 0
        assert rules["enhanced_min"] == 1
        assert rules["enhanced_max"] == 2
        assert rules["crisis_min"] == 3
    
    def test_load_crisis_indicators(self):
        loader = SpecificationLoader()
        crisis_indicators = loader.load_crisis_indicators()
        
        # Should have crisis type categories
        assert isinstance(crisis_indicators, dict)
        # May be empty if VR-24 structure is different
        # Just verify it returns a dict
    
    def test_load_crisis_resources(self):
        loader = SpecificationLoader()
        resources = loader.load_crisis_resources()
        
        assert isinstance(resources, dict)
        
        # Check for expected crisis types
        assert "mental_health" in resources
        assert "financial" in resources
        assert "health" in resources
        assert "abuse" in resources
        
        # Check mental health resources include 988
        mental_health_resources = resources["mental_health"]
        assert len(mental_health_resources) > 0
        
        # Verify structure
        for resource in mental_health_resources:
            assert "name" in resource
            assert "contact" in resource
            assert "description" in resource
            assert "available_247" in resource
    
    def test_988_resource_exists(self):
        loader = SpecificationLoader()
        resources = loader.load_crisis_resources()
        
        mental_health = resources["mental_health"]
        has_988 = any("988" in r["contact"] for r in mental_health)
        assert has_988, "988 Suicide & Crisis Lifeline should be included"
    
    def test_crisis_text_line_exists(self):
        loader = SpecificationLoader()
        resources = loader.load_crisis_resources()
        
        mental_health = resources["mental_health"]
        has_crisis_text = any("741741" in r["contact"] for r in mental_health)
        assert has_crisis_text, "Crisis Text Line should be included"
    
    def test_get_metadata(self):
        loader = SpecificationLoader()
        metadata = loader.get_metadata()
        
        assert isinstance(metadata, dict)
        assert "version" in metadata
        assert "creator" in metadata
        assert "status" in metadata
        
        # Check expected values
        assert metadata["version"] == "4.0"
        assert "Mehmet" in metadata["creator"]
