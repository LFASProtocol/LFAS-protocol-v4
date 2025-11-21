"""Crisis detection and response safeguards for LFAS Protocol v4."""

from typing import Dict, List

from .models import DetectionResult, ProtectionLevel, SafeguardResponse


class CrisisDetectionSafeguard:
    """
    VR-24 Crisis Detection & Response Safeguard.

    Implements the ACT phase of LFAS Protocol v4 by providing:
    - Immediate crisis resources (988 Lifeline, Crisis Text Line)
    - Empathetic, non-dismissive responses
    - Protection level-appropriate messaging
    """

    # Crisis resources (VR-24)
    CRISIS_RESOURCES = [
        {
            "name": "988 Suicide & Crisis Lifeline",
            "contact": "Call or text 988",
            "availability": "24/7",
            "description": "Free, confidential support for people in distress",
        },
        {
            "name": "Crisis Text Line",
            "contact": "Text HOME to 741741",
            "availability": "24/7",
            "description": "Text-based crisis support",
        },
        {
            "name": "International Association for Suicide Prevention",
            "contact": "https://www.iasp.info/resources/Crisis_Centres/",
            "availability": "24/7",
            "description": "Global crisis center directory",
        },
    ]

    def should_activate(self, detection_result: DetectionResult) -> bool:
        """
        Determine if crisis safeguard should activate.

        Args:
            detection_result: Result from vulnerability detection

        Returns:
            True if crisis level protection is needed
        """
        return detection_result.protection_level == ProtectionLevel.CRISIS

    def generate_response(self, detection_result: DetectionResult) -> SafeguardResponse:
        """
        Generate appropriate safeguard response based on protection level.

        Args:
            detection_result: Result from vulnerability detection

        Returns:
            SafeguardResponse with message and resources
        """
        level = detection_result.protection_level

        if level == ProtectionLevel.CRISIS:
            return self._generate_crisis_response(detection_result)
        elif level == ProtectionLevel.ENHANCED:
            return self._generate_enhanced_response(detection_result)
        else:
            return self._generate_standard_response(detection_result)

    def _generate_crisis_response(self, result: DetectionResult) -> SafeguardResponse:
        """Generate crisis-level response with immediate resources."""
        message = (
            "I'm concerned about what you're sharing. Your safety matters, "
            "and there are people ready to help right now.\n\n"
            "**Immediate Support Available:**\n"
        )

        for resource in self.CRISIS_RESOURCES:
            message += (
                f"\n• **{resource['name']}**\n"
                f"  {resource['contact']}\n"
                f"  {resource['description']} ({resource['availability']})\n"
            )

        message += (
            "\nThese services provide free, confidential support. "
            "You don't have to face this alone."
        )

        return SafeguardResponse(
            should_activate=True,
            message=message,
            resources=self.CRISIS_RESOURCES,
            protection_level=ProtectionLevel.CRISIS,
            metadata={"indicators": [str(i) for i in result.indicators]},
        )

    def _generate_enhanced_response(self, result: DetectionResult) -> SafeguardResponse:
        """Generate enhanced-level response with supportive messaging."""
        message = (
            "I notice you're going through a difficult time. While I can provide "
            "information, please remember:\n\n"
            "• Professional support can make a real difference\n"
            "• You don't have to handle everything alone\n"
            "• Help is available when you need it\n"
        )

        return SafeguardResponse(
            should_activate=True,
            message=message,
            resources=[],
            protection_level=ProtectionLevel.ENHANCED,
            metadata={"indicators": [str(i) for i in result.indicators]},
        )

    def _generate_standard_response(self, result: DetectionResult) -> SafeguardResponse:
        """Generate standard-level response."""
        return SafeguardResponse(
            should_activate=False,
            message="",
            resources=[],
            protection_level=ProtectionLevel.STANDARD,
            metadata={},
        )

    def get_crisis_resources(self) -> List[Dict[str, str]]:
        """
        Get list of crisis resources.

        Returns:
            List of crisis resource dictionaries
        """
        return self.CRISIS_RESOURCES.copy()
