"""
Tests for LFAS data models
"""

import pytest
from lfas.models import (
    ProtectionLevel, CrisisType, DetectionResult, 
    CrisisResult, CrisisResource
)


class TestProtectionLevel:
    """Test ProtectionLevel enum"""
    
    def test_levels_have_correct_values(self):
        assert ProtectionLevel.STANDARD.value == 1
        assert ProtectionLevel.ENHANCED.value == 2
        assert ProtectionLevel.CRISIS.value == 3
    
    def test_levels_have_correct_names(self):
        assert ProtectionLevel.STANDARD.name == "STANDARD"
        assert ProtectionLevel.ENHANCED.name == "ENHANCED"
        assert ProtectionLevel.CRISIS.name == "CRISIS"


class TestCrisisType:
    """Test CrisisType enum"""
    
    def test_crisis_types_exist(self):
        assert CrisisType.MENTAL_HEALTH.value == "mental_health"
        assert CrisisType.FINANCIAL.value == "financial"
        assert CrisisType.HEALTH.value == "health"
        assert CrisisType.ABUSE.value == "abuse"
        assert CrisisType.MIXED.value == "mixed"


class TestDetectionResult:
    """Test DetectionResult dataclass"""
    
    def test_creation_without_history(self):
        result = DetectionResult(
            protection_level=ProtectionLevel.ENHANCED,
            triggers_count=2,
            detected_categories=["crisis_language"],
            original_input="test input"
        )
        
        assert result.protection_level == ProtectionLevel.ENHANCED
        assert result.triggers_count == 2
        assert result.detected_categories == ["crisis_language"]
        assert result.original_input == "test input"
        assert result.conversation_history is None
    
    def test_creation_with_history(self):
        history = ["previous message", "another message"]
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language", "financial_desperation"],
            original_input="test input",
            conversation_history=history
        )
        
        assert result.conversation_history == history
    
    def test_string_representation(self):
        result = DetectionResult(
            protection_level=ProtectionLevel.STANDARD,
            triggers_count=0,
            detected_categories=[],
            original_input="test"
        )
        
        str_repr = str(result)
        assert "STANDARD" in str_repr
        assert "triggers=0" in str_repr


class TestCrisisResource:
    """Test CrisisResource dataclass"""
    
    def test_creation_with_defaults(self):
        resource = CrisisResource(
            name="Test Hotline",
            contact="1-800-TEST",
            description="Test description"
        )
        
        assert resource.name == "Test Hotline"
        assert resource.contact == "1-800-TEST"
        assert resource.description == "Test description"
        assert resource.available_247 is True
    
    def test_creation_without_247(self):
        resource = CrisisResource(
            name="Business Hours Line",
            contact="1-800-HOURS",
            description="9-5 only",
            available_247=False
        )
        
        assert resource.available_247 is False


class TestCrisisResult:
    """Test CrisisResult dataclass"""
    
    def test_creation(self):
        resources = [
            CrisisResource(
                name="988 Lifeline",
                contact="988",
                description="Crisis support"
            )
        ]
        
        result = CrisisResult(
            crisis_type=CrisisType.MENTAL_HEALTH,
            protection_level=ProtectionLevel.CRISIS,
            detected_indicators=["suicidal ideation"],
            primary_resources=resources,
            recommended_actions=["Call 988"],
            user_message="Test message"
        )
        
        assert result.crisis_type == CrisisType.MENTAL_HEALTH
        assert result.protection_level == ProtectionLevel.CRISIS
        assert len(result.primary_resources) == 1
        assert len(result.recommended_actions) == 1
    
    def test_format_crisis_message(self):
        resources = [
            CrisisResource(
                name="Test Resource",
                contact="123",
                description="Test"
            )
        ]
        
        result = CrisisResult(
            crisis_type=CrisisType.MENTAL_HEALTH,
            protection_level=ProtectionLevel.CRISIS,
            detected_indicators=[],
            primary_resources=resources,
            recommended_actions=["Action 1", "Action 2"],
            user_message="You need help"
        )
        
        message = result.format_crisis_message()
        
        assert "CRISIS SUPPORT ACTIVATED" in message
        assert "You need help" in message
        assert "Test Resource: 123" in message
        assert "Action 1" in message
        assert "Action 2" in message
        assert "not alone" in message
    
    def test_string_representation(self):
        result = CrisisResult(
            crisis_type=CrisisType.FINANCIAL,
            protection_level=ProtectionLevel.CRISIS,
            detected_indicators=[],
            primary_resources=[],
            recommended_actions=[],
            user_message=""
        )
        
        str_repr = str(result)
        assert "financial" in str_repr
        assert "CRISIS" in str_repr
