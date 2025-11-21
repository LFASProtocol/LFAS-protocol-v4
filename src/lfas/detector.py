"""
Vulnerability Detector - Core LISTEN Phase Implementation

This module implements the LISTEN phase of the LFAS Protocol v4, detecting
vulnerability indicators in user input and determining appropriate protection levels.
"""

from enum import IntEnum
from typing import Dict, List, Optional, Set

from .spec_loader import SpecificationLoader


class ProtectionLevel(IntEnum):
    """Protection levels for LFAS Protocol v4."""

    STANDARD = 1  # 0-1 triggers detected
    ENHANCED = 2  # 2 triggers detected
    CRISIS = 3  # 3+ triggers detected


class DetectionResult:
    """Results from vulnerability detection."""

    def __init__(
        self,
        protection_level: ProtectionLevel,
        triggered_indicators: List[str],
        triggered_categories: Set[str],
        trigger_count: int,
    ):
        """
        Initialize detection result.

        Args:
            protection_level: The determined protection level
            triggered_indicators: List of specific indicator phrases that matched
            triggered_categories: Set of categories that had matches
            trigger_count: Total number of triggers detected
        """
        self.protection_level = protection_level
        self.triggered_indicators = triggered_indicators
        self.triggered_categories = triggered_categories
        self.trigger_count = trigger_count

    def __repr__(self) -> str:
        return (
            f"DetectionResult(level={self.protection_level.name}, "
            f"triggers={self.trigger_count}, "
            f"categories={self.triggered_categories})"
        )


class VulnerabilityDetector:
    """
    Detects vulnerability indicators in user input.

    This class implements the LISTEN phase of the LFAS Protocol v4 by scanning
    user input for vulnerability indicators and determining the appropriate
    protection level.
    """

    def __init__(self, spec_path: Optional[str] = None):
        """
        Initialize the vulnerability detector.

        Args:
            spec_path: Optional path to LFAS v4 specification XML file.
                      If None, uses the default repository location.
        """
        self.spec_loader = SpecificationLoader(spec_path)
        self.indicators: Dict[str, List[str]] = {}
        self._load_indicators()

    def _load_indicators(self) -> None:
        """Load vulnerability indicators from the specification."""
        self.indicators = self.spec_loader.get_vulnerability_indicators()

    def detect(
        self, user_input: str, conversation_history: Optional[List[str]] = None
    ) -> DetectionResult:
        """
        Detect vulnerability indicators in user input.

        Args:
            user_input: The current user input to analyze
            conversation_history: Optional list of previous messages for context

        Returns:
            DetectionResult containing protection level and detected indicators
        """
        # Combine current input with recent history for context
        text_to_analyze = user_input.lower()
        if conversation_history:
            # Include recent history (last 3 messages) for context
            recent_history = " ".join(conversation_history[-3:]).lower()
            text_to_analyze = f"{recent_history} {text_to_analyze}"

        # Track triggered indicators
        triggered_indicators: List[str] = []
        triggered_categories: Set[str] = set()

        # Scan for indicators in each category
        for category, phrases in self.indicators.items():
            for phrase in phrases:
                if phrase.lower() in text_to_analyze:
                    triggered_indicators.append(phrase)
                    triggered_categories.add(category)

        # Determine protection level based on trigger count
        trigger_count = len(triggered_indicators)
        protection_level = self._determine_protection_level(trigger_count)

        return DetectionResult(
            protection_level=protection_level,
            triggered_indicators=triggered_indicators,
            triggered_categories=triggered_categories,
            trigger_count=trigger_count,
        )

    def _determine_protection_level(self, trigger_count: int) -> ProtectionLevel:
        """
        Determine protection level based on number of triggers.

        Args:
            trigger_count: Number of vulnerability indicators detected

        Returns:
            Appropriate ProtectionLevel
        """
        if trigger_count >= 3:
            return ProtectionLevel.CRISIS
        elif trigger_count >= 2:
            return ProtectionLevel.ENHANCED
        else:
            # 0-1 triggers = Standard
            return ProtectionLevel.STANDARD

    def get_indicator_categories(self) -> List[str]:
        """
        Get list of vulnerability indicator categories.

        Returns:
            List of category names
        """
        return list(self.indicators.keys())

    def get_indicators_for_category(self, category: str) -> List[str]:
        """
        Get all indicators for a specific category.

        Args:
            category: The category name (e.g., 'crisis_language')

        Returns:
            List of indicator phrases for that category
        """
        return self.indicators.get(category, [])
