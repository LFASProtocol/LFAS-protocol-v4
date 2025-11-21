"""
Crisis Safeguard - VR-24 Implementation

This module implements VR-24 (Crisis Detection & Response) from the LFAS Protocol v4.
It provides crisis response actions and resource provision for users in crisis situations.
"""

from dataclasses import dataclass
from typing import List

from .detector import DetectionResult, ProtectionLevel


@dataclass
class CrisisResource:
    """Represents a crisis resource with contact information."""

    name: str
    description: str
    contact: str
    region: str = "US"


class CrisisResponse:
    """Encapsulates a crisis response with resources and actions."""

    def __init__(
        self,
        crisis_detected: bool,
        crisis_type: str,
        resources: List[CrisisResource],
        recommended_actions: List[str],
    ):
        """
        Initialize a crisis response.

        Args:
            crisis_detected: Whether a crisis was detected
            crisis_type: Type of crisis (mental_health, financial, health, abuse)
            resources: List of crisis resources to provide
            recommended_actions: List of recommended actions for the AI system
        """
        self.crisis_detected = crisis_detected
        self.crisis_type = crisis_type
        self.resources = resources
        self.recommended_actions = recommended_actions


class CrisisDetector:
    """
    Implements VR-24: Crisis Detection & Response.

    This class determines when a crisis situation exists and provides
    appropriate crisis resources and response guidance.
    """

    # Crisis resources database
    CRISIS_RESOURCES = {
        "mental_health": [
            CrisisResource(
                name="National Suicide Prevention Lifeline",
                description="24/7 support for people in distress",
                contact="988 or 1-800-273-8255",
                region="US",
            ),
            CrisisResource(
                name="Crisis Text Line",
                description="Text-based crisis support",
                contact="Text HOME to 741741",
                region="US",
            ),
            CrisisResource(
                name="International Association for Suicide Prevention",
                description="Global crisis helpline directory",
                contact="https://findahelpline.com",
                region="International",
            ),
        ],
        "financial": [
            CrisisResource(
                name="National Foundation for Credit Counseling",
                description="Free financial counseling",
                contact="1-800-388-2227 or https://nfcc.org",
                region="US",
            ),
            CrisisResource(
                name="211 Helpline",
                description="Local community resources",
                contact="Dial 211",
                region="US",
            ),
        ],
        "health": [
            CrisisResource(
                name="Emergency Services",
                description="Immediate medical emergency",
                contact="911",
                region="US",
            ),
            CrisisResource(
                name="SAMHSA National Helpline",
                description="Substance abuse and mental health",
                contact="1-800-662-4357",
                region="US",
            ),
        ],
        "abuse": [
            CrisisResource(
                name="National Domestic Violence Hotline",
                description="24/7 support for domestic violence",
                contact="1-800-799-7233 or text START to 88788",
                region="US",
            ),
            CrisisResource(
                name="Childhelp National Child Abuse Hotline",
                description="Support for child abuse cases",
                contact="1-800-422-4453",
                region="US",
            ),
        ],
    }

    def __init__(self) -> None:
        """Initialize the crisis detector."""
        pass

    def assess_crisis(self, detection_result: DetectionResult) -> CrisisResponse:
        """
        Assess whether a crisis exists and generate appropriate response.

        Args:
            detection_result: Result from VulnerabilityDetector

        Returns:
            CrisisResponse with resources and recommended actions
        """
        # Crisis is triggered at Protection Level 3
        if detection_result.protection_level < ProtectionLevel.CRISIS:
            return CrisisResponse(
                crisis_detected=False,
                crisis_type="none",
                resources=[],
                recommended_actions=[],
            )

        # Determine crisis type based on triggered categories
        crisis_type = self._determine_crisis_type(detection_result)

        # Get relevant resources
        resources = self._get_resources(crisis_type, detection_result)

        # Generate recommended actions
        actions = self._generate_recommended_actions(crisis_type, detection_result)

        return CrisisResponse(
            crisis_detected=True,
            crisis_type=crisis_type,
            resources=resources,
            recommended_actions=actions,
        )

    def _determine_crisis_type(self, detection_result: DetectionResult) -> str:
        """
        Determine the primary crisis type based on detected categories.

        Args:
            detection_result: Result from VulnerabilityDetector

        Returns:
            Crisis type string
        """
        categories = detection_result.triggered_categories

        # Priority order: mental health > health > financial > abuse
        if "crisis_language" in categories:
            # Check if any mental health indicators are present
            mental_health_keywords = [
                "ending it",
                "don't want to live",
                "thinking about ending",
            ]
            if any(
                keyword in indicator.lower()
                for indicator in detection_result.triggered_indicators
                for keyword in mental_health_keywords
            ):
                return "mental_health"

        if "health_crisis" in categories:
            return "health"

        if "financial_desperation" in categories:
            return "financial"

        # Default to mental health for crisis language
        if "crisis_language" in categories:
            return "mental_health"

        return "general"

    def _get_resources(
        self, crisis_type: str, detection_result: DetectionResult
    ) -> List[CrisisResource]:
        """
        Get appropriate crisis resources for the detected crisis type.

        Args:
            crisis_type: Type of crisis
            detection_result: Detection result for context

        Returns:
            List of relevant crisis resources
        """
        resources = []

        # Add specific resources for the crisis type
        if crisis_type in self.CRISIS_RESOURCES:
            resources.extend(self.CRISIS_RESOURCES[crisis_type])

        # For severe cases, always include mental health resources
        if crisis_type != "mental_health" and detection_result.trigger_count >= 4:
            resources.extend(self.CRISIS_RESOURCES["mental_health"][:1])

        return resources

    def _generate_recommended_actions(
        self, crisis_type: str, detection_result: DetectionResult
    ) -> List[str]:
        """
        Generate recommended actions for the AI system.

        Args:
            crisis_type: Type of crisis
            detection_result: Detection result for context

        Returns:
            List of recommended actions
        """
        actions = [
            "Pause normal processing immediately",
            "Acknowledge the crisis state explicitly",
            "Provide immediate crisis resources",
            "Encourage seeking professional help",
            "Avoid any business or productivity advice",
        ]

        # Add specific actions based on crisis type
        if crisis_type == "mental_health":
            actions.extend(
                [
                    "Express empathy without minimizing feelings",
                    "Do not attempt to provide therapy or counseling",
                    "Strongly encourage contacting crisis support immediately",
                ]
            )
        elif crisis_type == "financial":
            actions.extend(
                [
                    "Avoid suggesting risky financial strategies",
                    "Recommend professional financial counseling",
                    "Connect to local community resources",
                ]
            )
        elif crisis_type == "health":
            actions.extend(
                [
                    "For emergencies, recommend calling 911 immediately",
                    "Do not provide medical diagnosis or treatment advice",
                    "Encourage seeking professional medical care",
                ]
            )

        return actions

    def format_crisis_message(self, crisis_response: CrisisResponse) -> str:
        """
        Format a crisis response into a user-friendly message.

        Args:
            crisis_response: The crisis response to format

        Returns:
            Formatted message string
        """
        if not crisis_response.crisis_detected:
            return ""

        lines = [
            "🚨 CRISIS SUPPORT RESOURCES",
            "",
            "It sounds like you're going through a very difficult time. ",
            "Please know that help is available:",
            "",
        ]

        # Add resources
        for resource in crisis_response.resources:
            lines.append(f"• {resource.name}")
            lines.append(f"  {resource.description}")
            lines.append(f"  Contact: {resource.contact}")
            if resource.region != "US":
                lines.append(f"  ({resource.region})")
            lines.append("")

        # Add encouraging message
        lines.extend(
            [
                "You don't have to face this alone. Professional support can help.",
                "Please reach out to one of these resources - they are there for you.",
            ]
        )

        return "\n".join(lines)
