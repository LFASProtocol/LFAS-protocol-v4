"""
LFAS Protocol v4 - Data Models
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class ProtectionLevel(Enum):
    """Protection levels for user interactions"""
    STANDARD = 1  # Basic protection
    ENHANCED = 2  # Vulnerability detected
    CRISIS = 3    # Crisis situation detected
    
    def __str__(self):
        return self.name


@dataclass
class DetectionResult:
    """Result of vulnerability detection analysis"""
    protection_level: ProtectionLevel
    triggers_count: int
    detected_categories: List[str]
    original_input: str
    confidence_score: Optional[float] = None
    
    def is_crisis(self) -> bool:
        """Check if this is a crisis-level detection"""
        return self.protection_level == ProtectionLevel.CRISIS
    
    def is_vulnerable(self) -> bool:
        """Check if any vulnerability was detected"""
        return self.protection_level.value >= ProtectionLevel.ENHANCED.value
    
    def __str__(self):
        return f"DetectionResult(level={self.protection_level}, triggers={self.triggers_count}, categories={self.detected_categories})"


@dataclass
class CrisisResource:
    """Crisis intervention resource information"""
    name: str
    phone: str
    description: str
    available_247: bool = False
    
    
@dataclass
class SafetyResponse:
    """Response with safety considerations applied"""
    original_detection: DetectionResult
    response_text: str
    applied_safeguards: List[str]
    resources_provided: List[CrisisResource]
    requires_human_escalation: bool = False
