"""
LFAS Protocol v4 - Vulnerability Detector
Analyzes user input for vulnerability signals and escalates protection levels
"""

from typing import List, Optional
from .models import DetectionResult, ProtectionLevel
from .specification_loader import SpecificationLoader


class VulnerabilityDetector:
    """
    Vulnerability detection system that dynamically loads indicators from XML spec
    Escalates protection levels based on detected signals:
    - 0 triggers → Standard Protection (Level 1)
    - 1-2 triggers → Enhanced Protection (Level 2)
    - 3+ triggers → Crisis Protection (Level 3)
    """
    
    def __init__(self, spec_path: Optional[str] = None):
        """
        Initialize vulnerability detector
        
        Args:
            spec_path: Path to XML specification file. If None, uses default.
        """
        self.loader = SpecificationLoader(spec_path)
        self.indicators = self.loader.load_vulnerability_indicators()
        self.escalation_rules = self.loader.load_protection_escalation_rules()
        self.conversation_history: List[str] = []
    
    def detect(
        self, 
        user_input: str, 
        conversation_history: Optional[List[str]] = None
    ) -> DetectionResult:
        """
        Analyze user input for vulnerability indicators
        
        Args:
            user_input: Current user message to analyze
            conversation_history: Optional list of previous messages for context
            
        Returns:
            DetectionResult with protection level and detected triggers
        """
        # Update conversation history
        if conversation_history is not None:
            self.conversation_history = conversation_history
        self.conversation_history.append(user_input)
        
        # Analyze current input
        input_lower = user_input.lower()
        detected_categories = set()
        total_triggers = 0
        
        # Check each category of indicators
        for category, indicators in self.indicators.items():
            for indicator in indicators:
                indicator_lower = indicator.lower()
                if indicator_lower in input_lower:
                    detected_categories.add(category)
                    total_triggers += 1
        
        # Determine protection level based on trigger count
        protection_level = self._determine_protection_level(total_triggers)
        
        return DetectionResult(
            protection_level=protection_level,
            triggers_count=total_triggers,
            detected_categories=list(detected_categories),
            original_input=user_input,
            conversation_history=self.conversation_history.copy()
        )
    
    def _determine_protection_level(self, trigger_count: int) -> ProtectionLevel:
        """
        Determine protection level based on number of triggers
        
        Args:
            trigger_count: Number of vulnerability indicators detected
            
        Returns:
            Appropriate ProtectionLevel
        """
        if trigger_count >= self.escalation_rules['crisis_min']:
            return ProtectionLevel.CRISIS
        elif trigger_count >= self.escalation_rules['enhanced_min']:
            return ProtectionLevel.ENHANCED
        else:
            return ProtectionLevel.STANDARD
    
    def reset_history(self):
        """Clear conversation history"""
        self.conversation_history = []
