"""
LFAS Protocol v4 - Crisis Detector
Assesses crisis situations and provides appropriate resources and responses
"""

from typing import List, Optional

from .models import CrisisResource, CrisisResult, CrisisType, DetectionResult
from .specification_loader import SpecificationLoader


class CrisisDetector:
    """
    Crisis detection and response system
    Triggers when protection_level >= 3
    Determines crisis type and surfaces real-world support resources
    """

    def __init__(self, spec_path: Optional[str] = None):
        """
        Initialize crisis detector

        Args:
            spec_path: Path to XML specification file
        """
        self.loader = SpecificationLoader(spec_path)
        self.crisis_indicators = self.loader.load_crisis_indicators()
        self.crisis_resources = self.loader.load_crisis_resources()

        # Keywords for enhanced crisis type detection
        self.crisis_keywords = {
            "mental_health": [
                "suicide",
                "suicidal",
                "kill myself",
                "end it all",
                "self-harm",
                "want to die",
                "better off dead",
                "no reason to live",
                "thinking about ending",
                "can't go on",
                "don't want to live",
            ],
            "financial": [
                "lost my job",
                "unemployed",
                "bankrupt",
                "bankruptcy",
                "eviction",
                "foreclosure",
                "can't pay",
                "no money",
                "desperate for money",
                "financial crisis",
                "losing everything",
            ],
            "health": [
                "health emergency",
                "can't see doctor",
                "no insurance",
                "medical emergency",
                "pain won't stop",
                "can't afford medication",
                "seriously ill",
                "health crisis",
            ],
            "abuse": [
                "domestic violence",
                "being abused",
                "partner hurts me",
                "afraid for my safety",
                "violent relationship",
                "sexual assault",
                "physical abuse",
            ],
        }

    def assess_crisis(self, detection_result: DetectionResult) -> CrisisResult:
        """
        Assess crisis type and generate appropriate response

        Args:
            detection_result: Result from VulnerabilityDetector

        Returns:
            CrisisResult with crisis type, resources, and messaging
        """
        if detection_result.protection_level.value < 3:
            # Not a crisis-level situation
            return self._create_non_crisis_result(detection_result)

        # Determine crisis type(s)
        crisis_types = self._detect_crisis_types(detection_result.original_input)

        # Mental health takes priority in mixed-crisis contexts
        if len(crisis_types) > 1 and "mental_health" in crisis_types:
            primary_crisis = "mental_health"
        elif len(crisis_types) > 1:
            primary_crisis = "mixed"
        elif crisis_types:
            primary_crisis = crisis_types[0]
        else:
            # Default to mental health if unclear
            primary_crisis = "mental_health"

        # Get appropriate resources
        resources = self._get_crisis_resources(primary_crisis, crisis_types)

        # Generate recommended actions
        actions = self._get_recommended_actions(primary_crisis)

        # Create user message
        user_message = self._create_crisis_message(primary_crisis, crisis_types)

        # Collect detected indicators
        indicators = self._extract_detected_indicators(
            detection_result.original_input, crisis_types
        )

        return CrisisResult(
            crisis_type=CrisisType[primary_crisis.upper()],
            protection_level=detection_result.protection_level,
            detected_indicators=indicators,
            primary_resources=resources,
            recommended_actions=actions,
            user_message=user_message,
        )

    def _detect_crisis_types(self, user_input: str) -> List[str]:
        """Detect which crisis types are present in the input"""
        input_lower = user_input.lower()
        detected = []

        for crisis_type, keywords in self.crisis_keywords.items():
            for keyword in keywords:
                if keyword in input_lower:
                    if crisis_type not in detected:
                        detected.append(crisis_type)
                    break

        return detected

    def _get_crisis_resources(
        self, primary_crisis: str, all_crisis_types: List[str]
    ) -> List[CrisisResource]:
        """Get appropriate crisis resources"""
        resources = []

        # Always include primary crisis resources
        if primary_crisis in self.crisis_resources:
            for res_dict in self.crisis_resources[primary_crisis]:
                resources.append(CrisisResource(**res_dict))

        # For mixed crisis, include mental health if not primary
        if primary_crisis == "mixed" and "mental_health" in all_crisis_types:
            for res_dict in self.crisis_resources["mental_health"][:1]:  # Just 988
                if not any(r.name == res_dict["name"] for r in resources):
                    resources.append(CrisisResource(**res_dict))

        # If no resources found, default to mental health
        if not resources and "mental_health" in self.crisis_resources:
            for res_dict in self.crisis_resources["mental_health"]:
                resources.append(CrisisResource(**res_dict))

        return resources

    def _get_recommended_actions(self, primary_crisis: str) -> List[str]:
        """Get recommended actions based on crisis type"""
        base_actions = [
            "Reach out to one of the crisis resources listed above",
            "Consider contacting a trusted friend or family member",
            "If in immediate danger, call emergency services (911)",
        ]

        crisis_specific_actions = {
            "mental_health": [
                "Talk to someone trained in crisis support - call 988",
                "Do not make any permanent decisions right now",
                "Remove immediate means of self-harm if possible",
            ],
            "financial": [
                "Contact a financial counselor for professional guidance",
                "Explore community assistance programs in your area",
                "Avoid making rushed financial decisions",
            ],
            "health": [
                "Seek immediate medical attention if experiencing emergency symptoms",
                "Contact local community health centers for affordable care",
                "Look into health care assistance programs",
            ],
            "abuse": [
                "Reach out to the domestic violence hotline for confidential support",
                "Create a safety plan if you haven't already",
                "Contact local law enforcement if in immediate danger",
            ],
            "mixed": [
                "Prioritize your immediate safety and well-being",
                "Reach out to crisis support services",
                "Consider which issue needs most urgent attention",
            ],
        }

        specific = crisis_specific_actions.get(primary_crisis, [])
        return specific + base_actions

    def _create_crisis_message(self, primary_crisis: str, all_crisis_types: List[str]) -> str:
        """Create appropriate crisis message"""
        messages = {
            "mental_health": (
                "I can see you're going through an extremely difficult time. "
                "Your safety and well-being are the top priority right now. "
                "Please know that you don't have to face this alone - "
                "professional crisis support is available 24/7."
            ),
            "financial": (
                "I understand you're facing serious financial difficulties. "
                "This is an incredibly stressful situation, but there are resources "
                "and professionals who can help you navigate this crisis."
            ),
            "health": (
                "I can see you're dealing with a health crisis. "
                "Your health and safety are the priority. "
                "Please reach out to medical professionals or emergency services "
                "who can provide proper care."
            ),
            "abuse": (
                "I'm concerned about your safety based on what you've shared. "
                "No one deserves to be in an abusive situation. "
                "Confidential support is available 24/7 from trained professionals "
                "who can help you stay safe."
            ),
            "mixed": (
                "I can see you're facing multiple serious challenges right now. "
                "This is an overwhelming situation, but you don't have to handle "
                "it alone. Professional support is available to help you through this."
            ),
        }

        return messages.get(primary_crisis, messages["mental_health"])

    def _extract_detected_indicators(self, user_input: str, crisis_types: List[str]) -> List[str]:
        """Extract the specific indicators that triggered crisis detection"""
        input_lower = user_input.lower()
        indicators = []

        for crisis_type in crisis_types:
            if crisis_type in self.crisis_keywords:
                for keyword in self.crisis_keywords[crisis_type]:
                    if keyword in input_lower:
                        indicators.append(f"{crisis_type}: '{keyword}'")

        return indicators

    def _create_non_crisis_result(self, detection_result: DetectionResult) -> CrisisResult:
        """Create a result for non-crisis situations"""
        return CrisisResult(
            crisis_type=CrisisType.MENTAL_HEALTH,
            protection_level=detection_result.protection_level,
            detected_indicators=[],
            primary_resources=[],
            recommended_actions=[],
            user_message=(
                "No crisis detected. "
                "Protection level does not require crisis intervention."
            ),
        )
