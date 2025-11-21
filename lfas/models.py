"""
LFAS Protocol v4 - Data Models
Defines core data structures for vulnerability and crisis detection
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict


class ProtectionLevel(Enum):
    """Protection levels based on vulnerability signals detected"""
    STANDARD = 1  # 0 triggers - basic safeguards
    ENHANCED = 2  # 1-2 triggers - vulnerability detected
    CRISIS = 3    # 3+ triggers - immediate danger


class CrisisType(Enum):
    """Types of crisis situations that can be detected"""
    MENTAL_HEALTH = "mental_health"
    FINANCIAL = "financial"
    HEALTH = "health"
    ABUSE = "abuse"
    MIXED = "mixed"  # Multiple crisis types detected


@dataclass
class DetectionResult:
    """Result from vulnerability detection analysis"""
    protection_level: ProtectionLevel
    triggers_count: int
    detected_categories: List[str]
    original_input: str
    conversation_history: Optional[List[str]] = None
    
    def __str__(self) -> str:
        return (
            f"DetectionResult(protection_level={self.protection_level.name}, "
            f"triggers={self.triggers_count}, "
            f"categories={self.detected_categories})"
        )


@dataclass
class CrisisResource:
    """Crisis support resource information"""
    name: str
    contact: str
    description: str
    available_247: bool = True


@dataclass
class CrisisResult:
    """Result from crisis assessment"""
    crisis_type: CrisisType
    protection_level: ProtectionLevel
    detected_indicators: List[str]
    primary_resources: List[CrisisResource]
    recommended_actions: List[str]
    user_message: str
    
    def format_crisis_message(self) -> str:
        """Format a user-facing crisis response message"""
        message_parts = [
            "⚠️ CRISIS SUPPORT ACTIVATED",
            "",
            self.user_message,
            "",
            "📞 IMMEDIATE RESOURCES:",
        ]
        
        for resource in self.primary_resources:
            message_parts.append(f"• {resource.name}: {resource.contact}")
            message_parts.append(f"  {resource.description}")
        
        message_parts.extend([
            "",
            "🔒 RECOMMENDED ACTIONS:",
        ])
        
        for action in self.recommended_actions:
            message_parts.append(f"• {action}")
        
        message_parts.extend([
            "",
            "Remember: You are not alone. Professional help is available 24/7.",
        ])
        
        return "\n".join(message_parts)
    
    def __str__(self) -> str:
        return (
            f"CrisisResult(type={self.crisis_type.value}, "
            f"level={self.protection_level.name}, "
            f"resources={len(self.primary_resources)})"
        )
