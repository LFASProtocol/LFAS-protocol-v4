"""
Crisis detection and response system for LFAS Protocol v4
"""

from typing import List, Optional
from .models import DetectionResult, CrisisResponse, ProtectionLevel


class CrisisDetector:
    """Detect and respond to crisis situations (VR-24)"""
    
    # Crisis hotlines and resources
    CRISIS_RESOURCES = {
        "suicidal_ideation": [
            "National Suicide Prevention Lifeline: 988 (US)",
            "Crisis Text Line: Text HOME to 741741",
            "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/",
        ],
        "financial_crisis": [
            "National Foundation for Credit Counseling: 1-800-388-2227",
            "211 (Community Resources): Dial 211",
            "Local social services and emergency assistance programs",
        ],
        "health_emergency": [
            "Emergency Services: 911 (US) or local emergency number",
            "Poison Control: 1-800-222-1222",
            "Telemedicine services if available in your area",
        ],
        "domestic_violence": [
            "National Domestic Violence Hotline: 1-800-799-7233",
            "Text START to 88788",
            "Local women's shelters and support services",
        ],
        "general_crisis": [
            "Crisis Text Line: Text HOME to 741741",
            "SAMHSA National Helpline: 1-800-662-4357",
            "Local community mental health services",
        ]
    }
    
    def __init__(self):
        self.crisis_keywords = {
            "suicidal_ideation": [
                "suicide", "kill myself", "end my life", "want to die",
                "better off dead", "ending it", "no reason to live",
                "suicidal", "take my own life"
            ],
            "financial_crisis": [
                "can't pay rent", "about to be evicted", "losing my home",
                "utilities shut off", "can't feed", "no money for food",
                "completely broke", "financial emergency"
            ],
            "health_emergency": [
                "severe pain", "can't breathe", "chest pain", "overdose",
                "medical emergency", "serious injury", "urgent medical"
            ],
            "domestic_violence": [
                "being abused", "domestic violence", "partner hurts me",
                "afraid for my safety", "violent relationship"
            ]
        }
    
    def assess_crisis(self, detection_result: DetectionResult) -> CrisisResponse:
        """
        Assess if situation is a crisis and provide appropriate resources
        
        Args:
            detection_result: Result from VulnerabilityDetector
            
        Returns:
            CrisisResponse with appropriate resources and actions
        """
        if not detection_result.is_crisis():
            return CrisisResponse(
                is_crisis=False,
                crisis_type=None,
                resources=[],
                recommended_actions=[]
            )
        
        # Identify specific crisis type
        crisis_type = self._identify_crisis_type(detection_result.original_input)
        
        # Get appropriate resources
        resources = self._get_crisis_resources(crisis_type)
        
        # Get recommended actions
        actions = self._get_recommended_actions(crisis_type)
        
        return CrisisResponse(
            is_crisis=True,
            crisis_type=crisis_type,
            resources=resources,
            recommended_actions=actions
        )
    
    def _identify_crisis_type(self, user_input: str) -> str:
        """Identify the specific type of crisis from user input"""
        input_lower = user_input.lower()
        
        # Check for specific crisis types (order matters - suicide is highest priority)
        for crisis_type, keywords in self.crisis_keywords.items():
            for keyword in keywords:
                if keyword in input_lower:
                    return crisis_type
        
        return "general_crisis"
    
    def _get_crisis_resources(self, crisis_type: str) -> List[str]:
        """Get appropriate crisis resources based on type"""
        return self.CRISIS_RESOURCES.get(crisis_type, self.CRISIS_RESOURCES["general_crisis"])
    
    def _get_recommended_actions(self, crisis_type: str) -> List[str]:
        """Get recommended actions based on crisis type"""
        if crisis_type == "suicidal_ideation":
            return [
                "Call or text a crisis helpline immediately",
                "Reach out to a trusted friend or family member",
                "If in immediate danger, call emergency services (911)",
                "Remove access to means of self-harm if possible",
                "Consider going to the nearest emergency room"
            ]
        elif crisis_type == "financial_crisis":
            return [
                "Contact local social services (dial 211)",
                "Reach out to community organizations for emergency assistance",
                "Talk to your landlord or utility company about payment plans",
                "Avoid quick-fix financial schemes or high-interest loans",
                "Seek professional financial counseling"
            ]
        elif crisis_type == "health_emergency":
            return [
                "Call emergency services (911) if life-threatening",
                "Go to the nearest emergency room if needed",
                "Contact a medical professional immediately",
                "Do not rely solely on AI for medical advice",
                "Have someone stay with you if possible"
            ]
        elif crisis_type == "domestic_violence":
            return [
                "Call the National Domestic Violence Hotline",
                "Create a safety plan with a professional",
                "Reach out to local domestic violence resources",
                "Trust your instincts about your safety",
                "Consider staying with someone you trust if safe to do so"
            ]
        else:
            return [
                "Reach out to a crisis helpline",
                "Talk to someone you trust about what you're experiencing",
                "Seek professional help from a counselor or therapist",
                "Remember: This situation is temporary and help is available",
                "Take care of your immediate safety and basic needs"
            ]
    
    def format_safe_response(self, crisis_response: CrisisResponse, 
                            original_ai_response: str = "") -> str:
        """
        Format a safe response that prioritizes crisis resources over AI advice
        
        Args:
            crisis_response: The crisis assessment result
            original_ai_response: The AI's original response (will be deprioritized)
            
        Returns:
            A formatted safe response prioritizing crisis resources
        """
        if not crisis_response.is_crisis:
            return original_ai_response
        
        # Crisis takes absolute priority - original response is suppressed
        safe_response = crisis_response.format_crisis_message()
        
        safe_response += "\n" + "="*50 + "\n"
        safe_response += "⚠️ IMPORTANT: I'm an AI and cannot provide emergency support.\n"
        safe_response += "Please use the resources above to connect with real people who can help.\n"
        
        return safe_response
