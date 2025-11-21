"""
LFAS Protocol v4 - Crisis Detection and Response
"""

from typing import List
from .models import DetectionResult, CrisisResource, SafetyResponse, ProtectionLevel


class CrisisDetector:
    """Handles crisis detection and generates appropriate responses"""
    
    CRISIS_RESOURCES = [
        CrisisResource(
            name="National Suicide Prevention Lifeline",
            phone="988",
            description="24/7 crisis support for people in distress",
            available_247=True
        ),
        CrisisResource(
            name="Crisis Text Line",
            phone="Text HOME to 741741",
            description="Free, 24/7 crisis support via text",
            available_247=True
        ),
        CrisisResource(
            name="SAMHSA National Helpline",
            phone="1-800-662-4357",
            description="Substance abuse and mental health services",
            available_247=True
        ),
    ]
    
    def assess_crisis(self, detection: DetectionResult) -> SafetyResponse:
        """
        Assess crisis level and generate appropriate safety response
        
        Args:
            detection: The vulnerability detection result
            
        Returns:
            SafetyResponse with appropriate interventions
        """
        if detection.protection_level == ProtectionLevel.CRISIS:
            return self._generate_crisis_response(detection)
        elif detection.protection_level == ProtectionLevel.ENHANCED:
            return self._generate_enhanced_response(detection)
        else:
            return self._generate_standard_response(detection)
    
    def _generate_crisis_response(self, detection: DetectionResult) -> SafetyResponse:
        """Generate response for crisis-level situations"""
        response_parts = [
            "I'm concerned about what you've shared with me.",
            "",
            "It's important that you know:",
            "• Your safety matters, and you don't have to face this alone",
            "• Professional help is available 24/7",
            "• Reaching out for help is a sign of strength, not weakness",
            "",
            "IMMEDIATE HELP:",
        ]
        
        for resource in self.CRISIS_RESOURCES:
            response_parts.append(f"• {resource.name}: {resource.phone}")
        
        response_parts.extend([
            "",
            "Please reach out to one of these resources. They have trained professionals",
            "who can provide the immediate support you need right now.",
            "",
            "I cannot provide advice on critical matters. Please connect with a human who can help."
        ])
        
        return SafetyResponse(
            original_detection=detection,
            response_text="\n".join(response_parts),
            applied_safeguards=["VR-24: Crisis Detection & Response", "VR-25: Amplification Prevention"],
            resources_provided=self.CRISIS_RESOURCES,
            requires_human_escalation=True
        )
    
    def _generate_enhanced_response(self, detection: DetectionResult) -> SafetyResponse:
        """Generate response for enhanced protection situations"""
        response_parts = [
            "I notice you may be going through a difficult time.",
            "",
            "Before we continue, I want to share some resources that might help:",
        ]
        
        for resource in self.CRISIS_RESOURCES[:2]:  # Share first 2 resources
            response_parts.append(f"• {resource.name}: {resource.phone}")
        
        response_parts.extend([
            "",
            "Please remember:",
            "• I can provide general information, but I'm not a substitute for professional help",
            "• Any advice I give may not account for your specific situation",
            "• Consider consulting with qualified professionals for important decisions",
        ])
        
        return SafetyResponse(
            original_detection=detection,
            response_text="\n".join(response_parts),
            applied_safeguards=["VR-20: Unfounded Optimism Prevention", "VR-23: Financial Realism"],
            resources_provided=self.CRISIS_RESOURCES[:2],
            requires_human_escalation=False
        )
    
    def _generate_standard_response(self, detection: DetectionResult) -> SafetyResponse:
        """Generate response for standard protection situations"""
        response_parts = [
            "I'll help with that. Please keep in mind:",
            "• I provide general information that may not fit every situation",
            "• Always verify important information with qualified sources",
            "• For critical decisions, consult with relevant professionals"
        ]
        
        return SafetyResponse(
            original_detection=detection,
            response_text="\n".join(response_parts),
            applied_safeguards=["VR-20: Unfounded Optimism Prevention"],
            resources_provided=[],
            requires_human_escalation=False
        )
    
    def format_crisis_message(self, detection: DetectionResult = None) -> str:
        """
        Quick format of crisis message
        
        Args:
            detection: Optional detection result
            
        Returns:
            Formatted crisis message string
        """
        if detection:
            response = self.assess_crisis(detection)
            return response.response_text
        
        # Default crisis message
        parts = ["CRISIS RESOURCES:", ""]
        for resource in self.CRISIS_RESOURCES:
            parts.append(f"{resource.name}: {resource.phone}")
        return "\n".join(parts)
