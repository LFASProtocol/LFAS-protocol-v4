#!/usr/bin/env python3
"""
Advanced example: Integrating LFAS into a chatbot

This example shows how to integrate LFAS Protocol into an AI chatbot
to provide safe, vulnerability-aware responses.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lfas import VulnerabilityDetector, CrisisDetector, ProtectionLevel


class SafeChatbot:
    """Example chatbot with LFAS Protocol integration"""
    
    def __init__(self):
        self.vuln_detector = VulnerabilityDetector()
        self.crisis_detector = CrisisDetector()
        self.conversation_history = []
    
    def process_input(self, user_input: str) -> str:
        """
        Process user input through LFAS Protocol
        
        This implements the 5-stage LFAS loop:
        LISTEN → REFLECT → WAIT → ACT → ACKNOWLEDGE
        """
        
        # STAGE 1: LISTEN - Detect vulnerability
        detection = self.vuln_detector.detect(user_input)
        
        # STAGE 2: REFLECT - Assess risk level
        protection_level = detection.protection_level
        crisis_response = self.crisis_detector.assess_crisis(detection)
        
        # STAGE 3: WAIT - Safety pause (simulated)
        # In a real system, this might involve additional checks
        
        # STAGE 4: ACT - Generate safe response
        if crisis_response.is_crisis:
            # Crisis takes absolute priority
            response = self._generate_crisis_response(crisis_response)
        elif protection_level == ProtectionLevel.ENHANCED:
            # Apply enhanced safeguards
            response = self._generate_enhanced_response(user_input, detection)
        else:
            # Standard response
            response = self._generate_standard_response(user_input)
        
        # STAGE 5: ACKNOWLEDGE - Log and confirm
        self.conversation_history.append({
            'input': user_input,
            'detection': detection,
            'response': response
        })
        
        return response
    
    def _generate_crisis_response(self, crisis_response) -> str:
        """Generate response for crisis situations (VR-24, VR-25)"""
        # Crisis resources take priority over any AI advice
        return crisis_response.format_crisis_message()
    
    def _generate_enhanced_response(self, user_input: str, detection) -> str:
        """Generate response with enhanced safeguards (VR-20, VR-22, VR-23)"""
        response = "I understand you're going through a difficult time. "
        
        # VR-20: Unfounded Optimism Prevention
        response += "While I can share some general guidance, please note that "
        response += "individual situations vary and there are no guaranteed solutions. "
        
        # VR-23: Financial Realism (if financial trigger detected)
        if 'financial_desperation' in detection.detected_categories:
            response += "\n\nIMPORTANT FINANCIAL DISCLAIMER:\n"
            response += "• All business ventures involve risk\n"
            response += "• Many businesses fail in the first year\n"
            response += "• Consider speaking with a financial counselor (call 211 for local resources)\n"
            response += "• Avoid quick-fix schemes or high-interest loans\n"
        
        # VR-25: Encourage human connection
        response += "\n\nI recommend reaching out to someone you trust or a professional "
        response += "who can provide personalized support for your situation."
        
        return response
    
    def _generate_standard_response(self, user_input: str) -> str:
        """Generate standard response with basic safeguards"""
        return f"Thank you for your message. How can I help you today?"
    
    def get_conversation_summary(self) -> str:
        """Get summary of protection levels used in conversation"""
        if not self.conversation_history:
            return "No conversation history"
        
        summary = "Conversation Summary:\n"
        summary += "="*50 + "\n"
        
        for i, entry in enumerate(self.conversation_history, 1):
            summary += f"\nExchange {i}:\n"
            summary += f"  Protection Level: {entry['detection'].protection_level.name}\n"
            summary += f"  Triggers: {entry['detection'].triggers_count}\n"
            if entry['detection'].detected_categories:
                summary += f"  Categories: {', '.join(entry['detection'].detected_categories)}\n"
        
        return summary


def main():
    """Demonstrate chatbot integration"""
    
    print("LFAS-Protected Chatbot Demo")
    print("="*60)
    print("This chatbot uses LFAS Protocol to detect and respond to")
    print("vulnerability signals in user input.\n")
    
    chatbot = SafeChatbot()
    
    # Simulate a conversation
    test_inputs = [
        "Hello, how are you?",
        "I just lost my job",
        "I'm worried about money and don't know what to do",
        "This is my last hope, I can't take it anymore"
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n{'='*60}")
        print(f"Exchange {i}")
        print(f"{'='*60}")
        print(f"USER: {user_input}")
        print(f"\nCHATBOT: {chatbot.process_input(user_input)}")
    
    # Show conversation summary
    print(f"\n{'='*60}")
    print(chatbot.get_conversation_summary())
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
