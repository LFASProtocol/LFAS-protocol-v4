import xml.etree.ElementTree as ET
from typing import List, Dict
from .models import DetectionResult, ProtectionLevel

class VulnerabilityDetector:
    def __init__(self, spec_path: str = "protocol/lfas-v4-specification.xml"):
        self.spec_path = spec_path
        self.indicators = self._load_indicators()
    
    def _load_indicators(self) -> Dict[str, List[str]]:
        """Load vulnerability indicators from XML specification"""
        tree = ET.parse(self.spec_path)
        root = tree.getroot()
        
        indicators = {}
        detection_engine = root.find(".//vulnerability_detection_engine")
        
        for category in detection_engine.findall(".//detection_indicators/*"):
            cat_name = category.tag
            category_indicators = []
            for ind in category.findall("indicator"):
                # Check for None text content
                if ind.text:
                    # Split comma-separated phrases and strip whitespace
                    phrases = [phrase.strip().lower() for phrase in ind.text.split(',')]
                    category_indicators.extend(phrases)
            indicators[cat_name] = category_indicators
        
        return indicators
    
    def detect(self, user_input: str) -> DetectionResult:
        """Analyze user input for vulnerability indicators"""
        input_lower = user_input.lower()
        detected_categories = set()
        total_triggers = 0
        
        for category, indicators in self.indicators.items():
            for indicator in indicators:
                if indicator in input_lower:
                    detected_categories.add(category)
                    total_triggers += 1
        
        # Determine protection level
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
            original_input=user_input
        )
