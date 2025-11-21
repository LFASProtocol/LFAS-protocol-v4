"""
Integration tests for the complete LFAS system
"""

import pytest
from lfas import VulnerabilityDetector, CrisisDetector, ProtectionLevel, CrisisType


class TestIntegration:
    """Integration tests for the full detection pipeline"""
    
    def test_full_pipeline_crisis_example(self):
        """Test the full example from the problem statement"""
        detector = VulnerabilityDetector()
        result = detector.detect("I lost my job, this is my last hope, can't take it anymore")
        
        assert result.protection_level.value >= 3
        
        if result.protection_level.value >= 3:
            crisis = CrisisDetector().assess_crisis(result)
            message = crisis.format_crisis_message()
            
            assert len(message) > 0
            assert "988" in message or "crisis" in message.lower()
    
    def test_standard_conversation_flow(self):
        """Test a standard conversation without crisis"""
        detector = VulnerabilityDetector()
        
        result1 = detector.detect("Hi, I need help with my project")
        assert result1.protection_level == ProtectionLevel.STANDARD
        
        result2 = detector.detect("Can you help me plan a task?")
        assert result2.protection_level == ProtectionLevel.STANDARD
        
        # History should be maintained
        assert len(detector.conversation_history) == 2
    
    def test_escalation_scenario(self):
        """Test escalation from standard to enhanced to crisis"""
        detector = VulnerabilityDetector()
        
        # Start standard
        result1 = detector.detect("Hello")
        assert result1.protection_level == ProtectionLevel.STANDARD
        
        detector.reset_history()
        
        # Escalate to enhanced
        result2 = detector.detect("I lost my job recently")
        assert result2.protection_level == ProtectionLevel.ENHANCED
        
        detector.reset_history()
        
        # Escalate to crisis
        result3 = detector.detect("I lost my job, this is my last hope, nobody understands")
        assert result3.protection_level == ProtectionLevel.CRISIS
    
    def test_all_crisis_types_coverage(self):
        """Test that all crisis types can be detected"""
        crisis_detector = CrisisDetector()
        
        # Mental health crisis
        from lfas.models import DetectionResult
        
        mh_result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Test"
        )
        mh_crisis = crisis_detector.assess_crisis(mh_result)
        assert mh_crisis.crisis_type == CrisisType.MENTAL_HEALTH
        
        # Financial crisis
        fin_result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["financial_desperation"],
            original_input="Test"
        )
        fin_crisis = crisis_detector.assess_crisis(fin_result)
        assert fin_crisis.crisis_type == CrisisType.FINANCIAL
        
        # Health crisis
        health_result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["health_crisis"],
            original_input="Test"
        )
        health_crisis = crisis_detector.assess_crisis(health_result)
        assert health_crisis.crisis_type == CrisisType.HEALTH
    
    def test_message_formatting_all_types(self):
        """Test message formatting for all crisis types"""
        from lfas.models import DetectionResult, CrisisResult, CrisisResource
        
        crisis_types = [
            CrisisType.MENTAL_HEALTH,
            CrisisType.FINANCIAL,
            CrisisType.HEALTH,
            CrisisType.ABUSE,
            CrisisType.MIXED
        ]
        
        detection_result = DetectionResult(
            protection_level=ProtectionLevel.CRISIS,
            triggers_count=3,
            detected_categories=["crisis_language"],
            original_input="Test"
        )
        
        for crisis_type in crisis_types:
            crisis_result = CrisisResult(
                crisis_type=crisis_type,
                severity="high",
                detection_result=detection_result,
                resources=[],
                recommended_actions=["Test action"],
                message="Test"
            )
            
            message = crisis_result.format_crisis_message()
            assert len(message) > 100
            assert "difficult" in message.lower() or "serious" in message.lower()
    
    def test_conversation_history_context(self):
        """Test that conversation history is maintained for context"""
        detector = VulnerabilityDetector()
        
        inputs = [
            "I'm working on a project",
            "It's not going well",
            "I lost my job",
            "This is my last hope"
        ]
        
        results = []
        for inp in inputs:
            result = detector.detect(inp)
            results.append(result)
        
        # Last result should have all history
        assert len(results[-1].conversation_history) == 4
        assert results[-1].conversation_history[0] == inputs[0]
        assert results[-1].conversation_history[3] == inputs[3]
    
    def test_spec_loader_integration(self):
        """Test that spec loader properly integrates with detectors"""
        from lfas.spec_loader import SpecificationLoader
        
        loader = SpecificationLoader()
        detector = VulnerabilityDetector()
        crisis_detector = CrisisDetector(spec_loader=loader)
        
        # All should use the same specification
        assert detector.indicators == loader.get_detection_indicators()
        assert crisis_detector.crisis_resources == loader.get_crisis_resources()
