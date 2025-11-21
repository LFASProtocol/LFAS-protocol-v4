"""
Vulnerability Detection Engine for LFAS Protocol v4

Implements the LISTEN phase of the LFAS protocol:
- Detects vulnerability indicators in user input
- Escalates protection levels based on detected triggers
- Provides foundation for safeguard activation
"""

from enum import IntEnum
from typing import List, Dict, Set
from dataclasses import dataclass


class ProtectionLevel(IntEnum):
    """Protection levels based on detected vulnerability indicators."""
    STANDARD = 1      # 0 triggers detected
    ENHANCED = 2      # 1-2 triggers detected
    CRISIS = 3        # 3+ triggers detected


@dataclass
class DetectionResult:
    """Result of vulnerability detection analysis."""
    protection_level: ProtectionLevel
    triggered_indicators: List[str]
    indicator_count: int
    categories: Set[str]


class VulnerabilityDetector:
    """
    Detects vulnerability indicators in user input.
    
    Based on LFAS Protocol v4 specification:
    - Crisis language (suicidal ideation, self-harm)
    - Financial desperation (job loss, eviction)
    - Health crisis (no insurance, can't afford medication)
    - Isolation indicators (no one to talk to, alone)
    """
    
    def __init__(self):
        """Initialize the vulnerability detector with indicators from the protocol."""
        # Crisis language indicators
        self.crisis_language = [
            "last hope",
            "only chance",
            "can't take it anymore",
            "nobody understands",
            "completely alone",
            "if this doesn't work, i'm done",
            "thinking about ending it",
            "don't want to live",
            "can't take it",
            "everything is hopeless",
            "no point",
            "want to die",
            "end it all",
        ]
        
        # Financial desperation indicators
        self.financial_desperation = [
            "lost my job",
            "last $",
            "need money fast",
            "desperate for income",
            "can't pay bills",
            "behind on rent",
            "facing eviction",
            "need cash now",
            "bills due",
            "can't afford",
        ]
        
        # Health crisis indicators
        self.health_crisis = [
            "can't see a doctor",
            "no insurance",
            "pain won't stop",
            "no medical help",
            "can't afford medication",
            "can't get treatment",
            "health emergency",
        ]
        
        # Isolation indicators
        self.isolation_indicators = [
            "no one to talk to",
            "family doesn't understand",
            "you're the only one who listens",
            "completely alone in this",
            "no one cares",
            "nobody listens",
            "all alone",
        ]
        
        # Build category mapping
        self.indicators_map = {
            "crisis_language": self.crisis_language,
            "financial_desperation": self.financial_desperation,
            "health_crisis": self.health_crisis,
            "isolation": self.isolation_indicators,
        }
    
    def detect(self, user_input: str) -> DetectionResult:
        """
        Detect vulnerability indicators in user input.
        
        Args:
            user_input: The current user message
        
        Returns:
            DetectionResult with protection level and triggered indicators
        """
        user_input_lower = user_input.lower()
        triggered_indicators = []
        categories = set()
        
        # Check all indicator categories
        for category, indicators in self.indicators_map.items():
            for indicator in indicators:
                if indicator in user_input_lower:
                    triggered_indicators.append(indicator)
                    categories.add(category)
        
        # Determine protection level based on trigger count
        indicator_count = len(triggered_indicators)
        
        if indicator_count == 0:
            protection_level = ProtectionLevel.STANDARD
        elif indicator_count <= 2:
            protection_level = ProtectionLevel.ENHANCED
        else:
            protection_level = ProtectionLevel.CRISIS
        
        return DetectionResult(
            protection_level=protection_level,
            triggered_indicators=triggered_indicators,
            indicator_count=indicator_count,
            categories=categories
        )
    
    def get_indicator_categories(self) -> Dict[str, List[str]]:
        """
        Get all indicator categories and their patterns.
        
        Returns:
            Dictionary mapping category names to indicator lists
        """
        return self.indicators_map.copy()
