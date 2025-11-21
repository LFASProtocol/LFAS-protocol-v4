"""
Safeguards for LFAS Protocol v4

Implements the ACT phase of the LFAS protocol:
- VR-24: Crisis Detection & Response
- Provides crisis resources and appropriate responses
"""

from typing import List, Optional
from dataclasses import dataclass

from .detector import ProtectionLevel, DetectionResult


@dataclass
class CrisisResource:
    """Crisis support resource information."""
    name: str
    phone: str
    description: str
    available: str


class CrisisDetectionSafeguard:
    """
    VR-24: Crisis Detection & Response
    
    Identifies and responds appropriately to crisis situations:
    - Suicidal ideation or self-harm statements
    - Immediate financial crisis
    - Health emergency statements
    - Domestic violence or abuse disclosures
    """
    
    # Crisis resources (US-based, can be extended for other regions)
    CRISIS_RESOURCES = [
        CrisisResource(
            name="988 Suicide & Crisis Lifeline",
            phone="988",
            description="24/7 crisis support for mental health emergencies",
            available="24/7"
        ),
        CrisisResource(
            name="Crisis Text Line",
            phone="Text HOME to 741741",
            description="24/7 crisis support via text message",
            available="24/7"
        ),
        CrisisResource(
            name="National Domestic Violence Hotline",
            phone="1-800-799-7233",
            description="Support for domestic violence situations",
            available="24/7"
        ),
    ]
    
    def should_activate(self, detection_result: DetectionResult) -> bool:
        """
        Determine if crisis safeguard should activate.
        
        Args:
            detection_result: Result from vulnerability detection
            
        Returns:
            True if crisis safeguard should activate
        """
        # Activate for Crisis protection level
        if detection_result.protection_level == ProtectionLevel.CRISIS:
            return True
        
        # Also activate for Enhanced level with crisis language
        if (detection_result.protection_level == ProtectionLevel.ENHANCED and
            "crisis_language" in detection_result.categories):
            return True
        
        return False
    
    def generate_response(self, detection_result: DetectionResult, 
                         original_response: Optional[str] = None) -> str:
        """
        Generate crisis-appropriate response.
        
        Args:
            detection_result: Result from vulnerability detection
            original_response: Optional original AI response to modify
            
        Returns:
            Crisis-appropriate response text
        """
        response_parts = []
        
        # Acknowledge the crisis
        response_parts.append(
            "I hear the pain in your words. This sounds incredibly difficult."
        )
        
        # Pause normal processing
        if "crisis_language" in detection_result.categories:
            response_parts.append(
                "\nBefore discussing anything else, I want to acknowledge this seems "
                "like a crisis moment. Your safety and wellbeing are what matter most right now."
            )
        
        # Provide crisis resources
        response_parts.append("\n\n**Immediate Support Resources:**")
        
        for resource in self.CRISIS_RESOURCES:
            response_parts.append(
                f"\n• **{resource.name}**: {resource.phone}\n  "
                f"{resource.description} ({resource.available})"
            )
        
        # Encourage human connection
        response_parts.append(
            "\n\nPlease consider reaching out to one of these resources or to someone "
            "you trust. You don't have to go through this alone."
        )
        
        # Add professional help recommendation
        if "health_crisis" in detection_result.categories:
            response_parts.append(
                "\n\nFor medical concerns, please contact a healthcare provider or "
                "visit an urgent care facility or emergency room if needed."
            )
        
        return "".join(response_parts)
    
    def get_crisis_resources(self) -> List[CrisisResource]:
        """
        Get list of crisis resources.
        
        Returns:
            List of available crisis resources
        """
        return self.CRISIS_RESOURCES.copy()
