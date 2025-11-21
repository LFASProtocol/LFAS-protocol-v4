"""
Vulnerability detection module - implements the LISTEN phase.
"""

from enum import Enum
from typing import Dict, List, Set


class ProtectionLevel(Enum):
    """Protection levels as defined in LFAS Protocol v4."""

    STANDARD = 1
    ENHANCED = 2
    CRISIS = 3


class VulnerabilityDetector:
    """
    Detects vulnerability indicators in user input.

    This implements the LISTEN phase of the LFAS Protocol,
    scanning for crisis signals, financial desperation,
    health crises, and isolation indicators.
    """

    def __init__(self, spec_path: str = None):
        """
        Initialize the detector.

        Args:
            spec_path: Path to LFAS XML specification file.
                      If None, uses built-in indicators.

        Note:
            In this minimal implementation, spec_path is reserved for future use.
            Currently uses built-in indicators extracted from the XML spec.
            See parser.py for full XML parsing implementation.
        """
        # Future: Parse from XML spec using SpecificationParser
        # For minimal implementation, use built-in indicators
        self.indicators = self._get_default_indicators()

    def _get_default_indicators(self) -> Dict[str, List[str]]:
        """
        Get default vulnerability indicators.
        These are extracted from protocol/lfas-v4-specification.xml
        """
        return {
            "crisis_language": [
                "last hope",
                "only chance",
                "can't take it anymore",
                "nobody understands",
                "completely alone",
                "if this doesn't work",
                "i'm done",
                "thinking about ending it",
                "don't want to live",
            ],
            "financial_desperation": [
                "lost my job",
                "last $",
                "need money fast",
                "desperate for income",
                "can't pay bills",
                "behind on rent",
                "facing eviction",
            ],
            "health_crisis": [
                "can't see a doctor",
                "no insurance",
                "pain won't stop",
                "no medical help",
                "can't afford medication",
            ],
            "isolation_indicators": [
                "no one to talk to",
                "family doesn't understand",
                "you're the only one who listens",
                "completely alone in this",
            ],
        }

    def analyze(self, message: str) -> Dict:
        """
        Analyze user message for vulnerability indicators.

        Args:
            message: Current user message

        Returns:
            Dictionary with detection results:
            {
                'triggers': ['crisis_language', 'financial_desperation'],
                'trigger_count': 2,
                'protection_level': ProtectionLevel.ENHANCED,
                'matched_phrases': ['last hope', 'lost my job'],
                'categories': {'crisis_language': 1, 'financial_desperation': 1}
            }
        """
        message_lower = message.lower()
        triggers: Set[str] = set()
        matched_phrases: List[str] = []
        categories: Dict[str, int] = {}

        # Scan for indicators
        for category, phrases in self.indicators.items():
            category_matches = 0
            for phrase in phrases:
                if phrase.lower() in message_lower:
                    triggers.add(category)
                    matched_phrases.append(phrase)
                    category_matches += 1

            if category_matches > 0:
                categories[category] = category_matches

        # Calculate protection level based on trigger count
        trigger_count = len(triggers)
        protection_level = self._calculate_protection_level(trigger_count)

        return {
            "triggers": list(triggers),
            "trigger_count": trigger_count,
            "protection_level": protection_level,
            "matched_phrases": matched_phrases,
            "categories": categories,
        }

    def _calculate_protection_level(self, trigger_count: int) -> ProtectionLevel:
        """
        Calculate protection level based on number of vulnerability categories detected.

        As per LFAS v4 specification:
        - 0 categories triggered: Standard (Level 1)
        - 1-2 categories triggered: Enhanced (Level 2)
        - 3+ categories triggered: Crisis (Level 3)
        
        Note: trigger_count refers to the number of unique category types detected,
        not the total number of individual phrase matches.
        """
        if trigger_count == 0:
            return ProtectionLevel.STANDARD
        elif trigger_count <= 2:
            return ProtectionLevel.ENHANCED
        else:
            return ProtectionLevel.CRISIS
