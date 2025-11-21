"""
Tests for LFAS Protocol v4 - Data Models
"""

import pytest
from lfas.models import (
    ProtectionLevel, 
    DetectionResult, 
    CrisisType, 
    CrisisResult,
    CrisisResource
)


class TestProtectionLevel:
    """Tests for ProtectionLevel enum"""
    
    def test_protection_levels_exist(self):
        """Verify all protection levels are defined"""
        assert ProtectionLevel.STANDARD.value == 1
        assert ProtectionLevel.ENHANCED.value == 2
        assert ProtectionLevel.CRISIS.value == 3
    
    def test_protection_level_names(self):
        """Verify protection level names"""
        assert ProtectionLevel.STANDARD.name == "STANDARD"
        assert ProtectionLevel.ENHANCED.name == "ENHANCED"
        assert ProtectionLevel.CRISIS.name == "CRISIS"


class TestCrisisType:
    """Tests for CrisisType enum"""
    
    def test_crisis_types_exist(self):
        """Verify all crisis types are defined"""
        assert CrisisType.MENTAL_HEALTH.value == "mental_health"
        assert CrisisType.FINANCIAL.value == "financial"
        assert CrisisType.HEALTH.value == "health"
        assert CrisisType.ABUSE.value == "abuse"
        assert CrisisType.MIXED.value == "mixed"


class TestDetectionResult:
    """Tests for DetectionResult dataclass"""
    
    def test_create_detection_result(self):
        """Test creating a detection result"""
        result = DetectionResult(
            protection_level=ProtectionLevel.ENHANCED,
            triggers_count=2,
            detected_categories=["crisis_language", "isolation_indicators"],
            original_input="I feel alone and desperate"
        )
        
        assert result.protection_level == ProtectionLevel.ENHANCED
        assert result.triggers_count == 2
        assert len(result.detected_categories) == 2
        assert result.original_input == "I feel alone and desperate"
    
    def test_detection_result_with_history(self):
        """Test detection result with conversation history"""
        history = ["First message", "Second message"]
        result = DetectionResult(
            protection_level=ProtectionLevel.STANDARD,
            triggers_count=0,
            detected_categories=[],
            original_input="Hello",
            conversation_history=history
        )
        
        assert result.conversation_history == history
    
    def test_detection_result_repr(self):
        """Test string representation of detection result"""
        result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Test"
        )
        
        repr_str = repr(result)
        assert "CRISIS" in repr_str
        assert "triggers_count=3" in repr_str


class TestCrisisResource:
    """Tests for CrisisResource dataclass"""
    
    def test_create_crisis_resource(self):
        """Test creating a crisis resource"""
        resource = CrisisResource(
            name="988 Suicide & Crisis Lifeline",
            description="24/7 crisis support",
            contact="Call or text 988",
            availability="24/7",
            crisis_type="mental_health"
        )
        
        assert resource.name == "988 Suicide & Crisis Lifeline"
        assert resource.contact == "Call or text 988"
        assert resource.crisis_type == "mental_health"


class TestCrisisResult:
    """Tests for CrisisResult dataclass"""
    
    def test_create_crisis_result(self):
        """Test creating a crisis result"""
        detection_result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Test crisis"
        )
        
        resources = [
            CrisisResource(
                name="Test Resource",
                description="Test description",
                contact="123-456-7890",
                availability="24/7",
                crisis_type="mental_health"
            )
        ]
        
        crisis_result = CrisisResult(
            crisis_type=CrisisType.MENTAL_HEALTH,
            severity="high",
            detection_result=detection_result,
            resources=resources,
            recommended_actions=["Call for help"],
            message="Test message"
        )
        
        assert crisis_result.crisis_type == CrisisType.MENTAL_HEALTH
        assert crisis_result.severity == "high"
        assert len(crisis_result.resources) == 1
        assert len(crisis_result.recommended_actions) == 1
    
    def test_format_crisis_message_mental_health(self):
        """Test formatting crisis message for mental health crisis"""
        detection_result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Test"
        )
        
        resources = [
            CrisisResource(
                name="988 Lifeline",
                description="Crisis support",
                contact="988",
                availability="24/7",
                crisis_type="mental_health"
            )
        ]
        
        crisis_result = CrisisResult(
            crisis_type=CrisisType.MENTAL_HEALTH,
            severity="high",
            detection_result=detection_result,
            resources=resources,
            recommended_actions=["Call 988"],
            message="Crisis detected"
        )
        
        message = crisis_result.format_crisis_message()
        
        assert "difficult time" in message
        assert "988 Lifeline" in message
        assert "Call 988" in message
        assert "don't have to face this alone" in message.lower()
    
    def test_format_crisis_message_financial(self):
        """Test formatting crisis message for financial crisis"""
        detection_result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["financial_desperation"],
            original_input="Test"
        )
        
        resources = [
            CrisisResource(
                name="Financial Help",
                description="Financial counseling",
                contact="1-800-123-4567",
                availability="Business hours",
                crisis_type="financial"
            )
        ]
        
        crisis_result = CrisisResult(
            crisis_type=CrisisType.FINANCIAL,
            severity="high",
            detection_result=detection_result,
            resources=resources,
            recommended_actions=["Seek counseling"],
            message="Financial crisis"
        )
        
        message = crisis_result.format_crisis_message()
        
        assert "Financial" in message or "financial" in message
        assert "Financial Help" in message
    
    def test_crisis_result_repr(self):
        """Test string representation of crisis result"""
        detection_result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Test"
        )
        
        crisis_result = CrisisResult(
            crisis_type=CrisisType.MENTAL_HEALTH,
            severity="critical",
            detection_result=detection_result,
            resources=[],
            recommended_actions=[],
            message="Test"
        )
        
        repr_str = repr(crisis_result)
        assert "MENTAL_HEALTH" in repr_str
        assert "critical" in repr_str
