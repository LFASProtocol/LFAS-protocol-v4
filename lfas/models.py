"""
LFAS Protocol v4 - Data Models
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict


class ProtectionLevel(Enum):
    """Protection levels based on detected vulnerability triggers"""
    STANDARD = 1  # 0 triggers: Basic protection
    ENHANCED = 2  # 1-2 triggers: Enhanced protection
    CRISIS = 3    # 3+ triggers: Crisis protection


class CrisisType(Enum):
    """Types of crisis situations that can be detected"""
    MENTAL_HEALTH = "mental_health"
    FINANCIAL = "financial"
    HEALTH = "health"
    ABUSE = "abuse"
    MIXED = "mixed"  # Multiple crisis types detected


@dataclass
class DetectionResult:
    """Result of vulnerability detection analysis"""
    protection_level: ProtectionLevel
    triggers_count: int
    detected_categories: List[str]
    original_input: str
    conversation_history: Optional[List[str]] = None
    
    def __repr__(self):
        return (f"DetectionResult(protection_level={self.protection_level.name}, "
                f"triggers_count={self.triggers_count}, "
                f"categories={self.detected_categories})")


@dataclass
class CrisisResource:
    """Crisis support resource information"""
    name: str
    description: str
    contact: str
    availability: str
    crisis_type: str


@dataclass
class CrisisResult:
    """Result of crisis assessment including resources and messaging"""
    crisis_type: CrisisType
    severity: str
    detection_result: DetectionResult
    resources: List[CrisisResource]
    recommended_actions: List[str]
    message: str
    
    def format_crisis_message(self) -> str:
        """Format a user-facing crisis intervention message"""
        msg_parts = []
        
        # Acknowledgment
        msg_parts.append("I can see you're going through an extremely difficult time.")
        msg_parts.append("")
        
        # Crisis-specific message
        if self.crisis_type == CrisisType.MENTAL_HEALTH:
            msg_parts.append("What you're feeling is serious, and you deserve immediate support.")
            msg_parts.append("")
            msg_parts.append("**Please reach out to a crisis professional right now:**")
        elif self.crisis_type == CrisisType.FINANCIAL:
            msg_parts.append("Financial crises can feel overwhelming, but help is available.")
            msg_parts.append("")
            msg_parts.append("**Here are immediate resources:**")
        elif self.crisis_type == CrisisType.HEALTH:
            msg_parts.append("This sounds like a health emergency that needs professional attention.")
            msg_parts.append("")
            msg_parts.append("**Please seek immediate medical help:**")
        elif self.crisis_type == CrisisType.ABUSE:
            msg_parts.append("Your safety is the priority. Help is available right now.")
            msg_parts.append("")
            msg_parts.append("**Crisis support for your situation:**")
        else:  # MIXED
            msg_parts.append("You're dealing with multiple serious challenges simultaneously.")
            msg_parts.append("")
            msg_parts.append("**Priority crisis resources:**")
        
        # Resources
        msg_parts.append("")
        for resource in self.resources:
            msg_parts.append(f"• **{resource.name}**")
            msg_parts.append(f"  {resource.description}")
            msg_parts.append(f"  Contact: {resource.contact}")
            msg_parts.append(f"  Available: {resource.availability}")
            msg_parts.append("")
        
        # Recommended actions
        if self.recommended_actions:
            msg_parts.append("**What you can do right now:**")
            for action in self.recommended_actions:
                msg_parts.append(f"• {action}")
            msg_parts.append("")
        
        # Closing
        msg_parts.append("You don't have to face this alone. Real people are ready to help you right now.")
        
        return "\n".join(msg_parts)
    
    def __repr__(self):
        return (f"CrisisResult(crisis_type={self.crisis_type.name}, "
                f"severity={self.severity}, "
                f"resources_count={len(self.resources)})")
