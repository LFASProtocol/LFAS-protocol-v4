"""
LFAS Protocol v4 - Crisis Detector
Crisis assessment and resource provision based on VR-24 safeguards
"""

from typing import List, Optional
from .models import (
    DetectionResult, CrisisResult, CrisisType, 
    CrisisResource, ProtectionLevel
)
from .spec_loader import SpecificationLoader


class CrisisDetector:
    """
    Assesses crisis situations and provides appropriate resources.
    Implements VR-24: Crisis Detection & Response
    """
    
    def __init__(self, spec_loader: Optional[SpecificationLoader] = None):
        """
        Initialize the crisis detector.
        
        Args:
            spec_loader: Optional SpecificationLoader instance. If None, creates one.
        """
        self.spec_loader = spec_loader or SpecificationLoader()
        self.crisis_resources = self.spec_loader.get_crisis_resources()
        self.vr_requirements = self.spec_loader.get_verification_requirements()
    
    def assess_crisis(self, detection_result: DetectionResult) -> CrisisResult:
        """
        Assess crisis type and severity, provide appropriate resources.
        
        Args:
            detection_result: Result from VulnerabilityDetector
            
        Returns:
            CrisisResult with crisis type, resources, and messaging
        """
        # Only assess if protection level indicates crisis
        if detection_result.protection_level.value < 3:
            raise ValueError(
                f"Crisis assessment requires protection level >= 3, "
                f"got {detection_result.protection_level.name}"
            )
        
        # Determine crisis type based on detected categories
        crisis_type = self._determine_crisis_type(detection_result.detected_categories)
        
        # Determine severity
        severity = self._determine_severity(detection_result.triggers_count)
        
        # Get appropriate resources
        resources = self._get_resources_for_crisis(crisis_type)
        
        # Generate recommended actions
        actions = self._generate_recommended_actions(crisis_type, detection_result)
        
        # Create message
        message = self._generate_crisis_message(crisis_type, resources)
        
        return CrisisResult(
            crisis_type=crisis_type,
            severity=severity,
            detection_result=detection_result,
            resources=resources,
            recommended_actions=actions,
            message=message
        )
    
    def _determine_crisis_type(self, detected_categories: List[str]) -> CrisisType:
        """
        Determine the type of crisis based on detected categories.
        Mental health is prioritized in multi-issue contexts per requirements.
        
        Args:
            detected_categories: List of category names detected
            
        Returns:
            CrisisType enum value
        """
        # Mental health prioritized in mixed crisis contexts
        if "crisis_language" in detected_categories:
            return CrisisType.MENTAL_HEALTH
        
        # Check for multiple crisis types
        crisis_count = 0
        primary_type = None
        
        category_mapping = {
            "crisis_language": CrisisType.MENTAL_HEALTH,
            "financial_desperation": CrisisType.FINANCIAL,
            "health_crisis": CrisisType.HEALTH,
            "isolation_indicators": CrisisType.MENTAL_HEALTH  # Isolation maps to mental health
        }
        
        for category in detected_categories:
            if category in category_mapping:
                crisis_count += 1
                if primary_type is None:
                    primary_type = category_mapping[category]
        
        # Multiple distinct crisis types = mixed
        if crisis_count > 1:
            # But mental health still takes priority if present
            if "crisis_language" in detected_categories:
                return CrisisType.MENTAL_HEALTH
            return CrisisType.MIXED
        
        # Single crisis type
        if primary_type:
            return primary_type
        
        # Default to mental health for safety
        return CrisisType.MENTAL_HEALTH
    
    def _determine_severity(self, triggers_count: int) -> str:
        """
        Determine crisis severity based on number of triggers.
        
        Args:
            triggers_count: Number of vulnerability triggers detected
            
        Returns:
            Severity level as string
        """
        if triggers_count >= 5:
            return "critical"
        elif triggers_count >= 3:
            return "high"
        else:
            return "moderate"
    
    def _get_resources_for_crisis(self, crisis_type: CrisisType) -> List[CrisisResource]:
        """
        Get appropriate crisis resources based on crisis type.
        
        Args:
            crisis_type: Type of crisis detected
            
        Returns:
            List of CrisisResource objects
        """
        resources = []
        
        if crisis_type == CrisisType.MENTAL_HEALTH:
            resource_dicts = self.crisis_resources.get("mental_health", [])
        elif crisis_type == CrisisType.FINANCIAL:
            resource_dicts = self.crisis_resources.get("financial", [])
        elif crisis_type == CrisisType.HEALTH:
            resource_dicts = self.crisis_resources.get("health", [])
        elif crisis_type == CrisisType.ABUSE:
            resource_dicts = self.crisis_resources.get("abuse", [])
        else:  # MIXED - prioritize mental health resources first
            resource_dicts = (
                self.crisis_resources.get("mental_health", []) +
                self.crisis_resources.get("financial", [])[:1]  # Add one financial resource
            )
        
        # Convert dictionaries to CrisisResource objects
        for res_dict in resource_dicts:
            resources.append(CrisisResource(
                name=res_dict["name"],
                description=res_dict["description"],
                contact=res_dict["contact"],
                availability=res_dict["availability"],
                crisis_type=res_dict["crisis_type"]
            ))
        
        return resources
    
    def _generate_recommended_actions(
        self, 
        crisis_type: CrisisType, 
        detection_result: DetectionResult
    ) -> List[str]:
        """
        Generate recommended immediate actions based on crisis type.
        
        Args:
            crisis_type: Type of crisis detected
            detection_result: Original detection result
            
        Returns:
            List of recommended action strings
        """
        actions = []
        
        if crisis_type == CrisisType.MENTAL_HEALTH:
            actions.extend([
                "Call or text 988 right now to speak with a trained crisis counselor",
                "If you're in immediate danger, call 911 or go to the nearest emergency room",
                "Reach out to a trusted friend or family member - you don't have to be alone",
                "Stay in a safe environment and remove access to means of self-harm"
            ])
        elif crisis_type == CrisisType.FINANCIAL:
            actions.extend([
                "Contact the National Foundation for Credit Counseling for free guidance",
                "Call 211 to find local emergency financial assistance programs",
                "Reach out to creditors to discuss hardship programs or payment plans",
                "Speak with a trusted person about your situation - isolation makes it harder"
            ])
        elif crisis_type == CrisisType.HEALTH:
            actions.extend([
                "If this is a medical emergency, call 911 immediately",
                "Visit the nearest emergency room or urgent care center",
                "Contact Health Resources & Services Administration to find free/low-cost care",
                "Don't delay medical care - financial concerns can be addressed after treatment"
            ])
        elif crisis_type == CrisisType.ABUSE:
            actions.extend([
                "Your safety comes first - reach out to the National Domestic Violence Hotline",
                "Create a safety plan if you're not ready to leave yet",
                "Document incidents when it's safe to do so",
                "Contact local law enforcement if you're in immediate danger"
            ])
        else:  # MIXED
            actions.extend([
                "Your safety and wellbeing are the priority right now",
                "Call 988 for immediate mental health support",
                "Reach out to a real person - friend, family member, or crisis professional",
                "Focus on one immediate need at a time with professional guidance"
            ])
        
        return actions
    
    def _generate_crisis_message(
        self, 
        crisis_type: CrisisType, 
        resources: List[CrisisResource]
    ) -> str:
        """
        Generate a crisis intervention message.
        
        Args:
            crisis_type: Type of crisis detected
            resources: List of applicable resources
            
        Returns:
            Formatted crisis message string
        """
        msg = f"Crisis detected: {crisis_type.value}. "
        msg += f"Immediate professional help is available. "
        msg += f"Found {len(resources)} crisis resources."
        return msg
