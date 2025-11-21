"""Vulnerability detection module for LFAS Protocol v4."""

import re
from typing import Dict, List, Set

from .models import DetectionResult, VulnerabilityCategory, VulnerabilityIndicator


class VulnerabilityDetector:
    """
    Detects vulnerability indicators in user input.

    Implements the LISTEN phase of LFAS Protocol v4 by monitoring for:
    - Crisis language (VR-24)
    - Financial desperation
    - Health crisis indicators
    - Isolation signals
    """

    def __init__(self):
        """Initialize the detector with pattern databases."""
        self._patterns: Dict[VulnerabilityCategory, List[str]] = {
            VulnerabilityCategory.CRISIS_LANGUAGE: [
                r"\b(suicid|kill myself|end it all|no reason to live)\b",
                r"\b(can\'?t take it|cannot take it|unbearable)\b",
                r"\b(hopeless|worthless|no point)\b",
                r"\b(want to die|better off dead)\b",
                r"\b(no way out|can\'?t go on)\b",
            ],
            VulnerabilityCategory.FINANCIAL_DESPERATION: [
                r"\b(bankruptcy|broke|destitute)\b",
                r"\b(lost everything|losing everything)\b",
                r"\b(can\'?t pay|cannot afford)\b",
                r"\b(financial ruin|money problems)\b",
                r"\b(desperate for money|need money now)\b",
            ],
            VulnerabilityCategory.HEALTH_CRISIS: [
                r"\b(terminal|dying|fatal illness)\b",
                r"\b(chronic pain|unbearable pain)\b",
                r"\b(medical emergency|health crisis)\b",
                r"\b(can\'?t function|cannot function)\b",
                r"\b(deteriorating health)\b",
            ],
            VulnerabilityCategory.ISOLATION: [
                r"\b(no one cares|nobody cares)\b",
                r"\b(all alone|completely alone)\b",
                r"\b(no friends|no family)\b",
                r"\b(abandoned|isolated|lonely)\b",
                r"\b(no one to talk to|nobody listens)\b",
            ],
        }

    def detect(self, text: str) -> DetectionResult:
        """
        Detect vulnerability indicators in the given text.

        Args:
            text: User input text to analyze

        Returns:
            DetectionResult with detected indicators and protection level
        """
        if not text or not isinstance(text, str):
            return DetectionResult(text="")

        result = DetectionResult(text=text)
        text_lower = text.lower()

        # Track matched patterns to avoid duplicates
        matched_patterns: Set[str] = set()

        # Check each category
        for category, patterns in self._patterns.items():
            for pattern in patterns:
                if pattern in matched_patterns:
                    continue

                if re.search(pattern, text_lower, re.IGNORECASE):
                    indicator = VulnerabilityIndicator(
                        category=category, pattern=pattern.replace(r"\b", "").replace("\\", "")
                    )
                    result.add_indicator(indicator)
                    matched_patterns.add(pattern)
                    # Only count one match per category
                    break

        return result

    def add_pattern(self, category: VulnerabilityCategory, pattern: str) -> None:
        """
        Add a custom detection pattern.

        Args:
            category: Vulnerability category
            pattern: Regular expression pattern to match
        """
        if category in self._patterns:
            self._patterns[category].append(pattern)
        else:
            self._patterns[category] = [pattern]

    def get_patterns(
        self, category: VulnerabilityCategory = None
    ) -> Dict[VulnerabilityCategory, List[str]]:
        """
        Get current detection patterns.

        Args:
            category: Optional specific category to retrieve

        Returns:
            Dictionary of patterns by category
        """
        if category:
            return {category: self._patterns.get(category, [])}
        return self._patterns.copy()
