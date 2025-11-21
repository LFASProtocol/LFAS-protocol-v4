from typing import List, Dict, Optional
from .models import DetectionResult, ProtectionLevel
from .spec_loader import SpecificationLoader


class VulnerabilityDetector:
    """
    Detects vulnerability indicators in user input and determines protection levels.
    Uses dynamic XML specification for indicator patterns.
    """
    
    def __init__(self, spec_path: Optional[str] = None):
        """
        Initialize the vulnerability detector.
        
        Args:
            spec_path: Optional path to XML specification. If None, uses default.
        """
        self.spec_loader = SpecificationLoader(spec_path)
        raw_indicators = self.spec_loader.get_detection_indicators()
        # Pre-process indicators to lowercase for efficient matching
        self.indicators = {
            category: [ind.lower() for ind in indicators]
            for category, indicators in raw_indicators.items()
        }
        self.conversation_history: List[str] = []
    
    def detect(self, user_input: str, maintain_history: bool = True) -> DetectionResult:
        """
        Analyze user input for vulnerability indicators.
        
        Args:
            user_input: User's text input to analyze
            maintain_history: Whether to add this input to conversation history
            
        Returns:
            DetectionResult with protection level and detected categories
        """
        if maintain_history:
            self.conversation_history.append(user_input)
        
        input_lower = user_input.lower()
        detected_categories = set()
        total_triggers = 0
        
        # Check each category and its indicators
        for category, indicators in self.indicators.items():
            for indicator in indicators:
                if indicator in input_lower:
                    detected_categories.add(category)
                    total_triggers += 1
        
        # Determine protection level based on trigger count
        # Per specification: 0→L1, 1-2→L2, 3+→L3
        if total_triggers >= 3:
            protection_level = ProtectionLevel.CRISIS
        elif total_triggers >= 1:
            protection_level = ProtectionLevel.ENHANCED
        else:
            protection_level = ProtectionLevel.STANDARD
        
        return DetectionResult(
            protection_level=protection_level,
            triggers_count=total_triggers,
            detected_categories=list(detected_categories),
            original_input=user_input,
            conversation_history=self.conversation_history.copy() if maintain_history else None
        )
    
    def reset_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
    
    def reload_specification(self):
        """Reload the XML specification (useful for dynamic updates)"""
        self.spec_loader.reload()
        raw_indicators = self.spec_loader.get_detection_indicators()
        # Re-process indicators to lowercase
        self.indicators = {
            category: [ind.lower() for ind in indicators]
            for category, indicators in raw_indicators.items()
        }
