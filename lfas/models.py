"""
Data models for LFAS Protocol v4
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class ProtectionLevel(Enum):
    """Protection levels for user interactions"""
    STANDARD = 1  # 0 triggers detected
    ENHANCED = 2  # 1-2 triggers detected
    CRISIS = 3    # 3+ triggers detected


@dataclass
class DetectionResult:
    """Result of vulnerability detection analysis"""
    protection_level: ProtectionLevel
    triggers_count: int
    detected_categories: List[str]
    original_input: str
    
    def is_crisis(self) -> bool:
        """Check if result indicates a crisis situation"""
        return self.protection_level == ProtectionLevel.CRISIS
    
    def is_vulnerable(self) -> bool:
        """Check if result indicates any vulnerability"""
        return self.protection_level.value >= 2
    
    def __str__(self) -> str:
        return (
            f"Protection Level: {self.protection_level.name} "
            f"(Triggers: {self.triggers_count}, "
            f"Categories: {', '.join(self.detected_categories) if self.detected_categories else 'None'})"
        )


@dataclass
class CrisisResponse:
    """Response structure for crisis situations"""
    is_crisis: bool
    crisis_type: Optional[str]
    resources: List[str]
    recommended_actions: List[str]
    
    def format_crisis_message(self) -> str:
        """Format a crisis response message for the user"""
        if not self.is_crisis:
            return ""
        
        message = "⚠️ CRISIS SUPPORT NEEDED\n\n"
        
        if self.crisis_type:
            message += f"Detected: {self.crisis_type}\n\n"
        
        if self.resources:
            message += "IMMEDIATE RESOURCES:\n"
            for resource in self.resources:
                message += f"• {resource}\n"
            message += "\n"
        
        if self.recommended_actions:
            message += "RECOMMENDED ACTIONS:\n"
            for action in self.recommended_actions:
                message += f"• {action}\n"
        
        return message


@dataclass
class SafeguardViolation:
    """Record of a safeguard violation"""
    safeguard_id: str  # e.g., "VR-20", "VR-24"
    safeguard_name: str
    violation_type: str
    original_text: str
    suggested_replacement: Optional[str] = None
