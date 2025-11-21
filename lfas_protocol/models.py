"""Data models and enums for the LFAS Protocol."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class ProtectionLevel(Enum):
    """Protection levels as defined in LFAS Protocol v4."""

    STANDARD = 1  # 0-1 triggers
    ENHANCED = 2  # 2 triggers
    CRISIS = 3  # 3+ triggers


class VulnerabilityCategory(Enum):
    """Categories of vulnerability indicators."""

    CRISIS_LANGUAGE = "crisis_language"
    FINANCIAL_DESPERATION = "financial_desperation"
    HEALTH_CRISIS = "health_crisis"
    ISOLATION = "isolation"


@dataclass
class VulnerabilityIndicator:
    """A detected vulnerability indicator."""

    category: VulnerabilityCategory
    pattern: str
    severity: str = "medium"

    def __str__(self) -> str:
        return f"{self.category.value}: {self.pattern}"


@dataclass
class DetectionResult:
    """Result of vulnerability detection."""

    text: str
    indicators: List[VulnerabilityIndicator] = field(default_factory=list)
    protection_level: ProtectionLevel = ProtectionLevel.STANDARD
    trigger_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Calculate trigger count and protection level from indicators."""
        self.trigger_count = len(self.indicators)

        # Protection level escalation logic
        if self.trigger_count >= 3:
            self.protection_level = ProtectionLevel.CRISIS
        elif self.trigger_count >= 2:
            self.protection_level = ProtectionLevel.ENHANCED
        else:
            self.protection_level = ProtectionLevel.STANDARD

    def add_indicator(self, indicator: VulnerabilityIndicator) -> None:
        """Add an indicator and recalculate protection level."""
        self.indicators.append(indicator)
        self.__post_init__()

    def __str__(self) -> str:
        return (
            f"DetectionResult(triggers={self.trigger_count}, "
            f"level={self.protection_level.name}, "
            f"indicators={len(self.indicators)})"
        )


@dataclass
class SafeguardResponse:
    """Response from a crisis safeguard."""

    should_activate: bool
    message: str
    resources: List[Dict[str, str]] = field(default_factory=list)
    protection_level: ProtectionLevel = ProtectionLevel.STANDARD
    metadata: Dict[str, Any] = field(default_factory=dict)
