"""
OpenAI Integration Example for LFAS Protocol

This example demonstrates how to wrap OpenAI's API with LFAS safety checks.
Note: This is a demonstration. For production use, you would need an OpenAI API key.
"""

from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard, ProtectionLevel


class SafeAIChat:
    """
    A safe AI chat wrapper that applies LFAS Protocol safeguards.
    
    This wrapper can be adapted for any AI API (OpenAI, Anthropic, Google, etc.)
    """
    
    def __init__(self):
        """Initialize the safe AI chat wrapper."""
        self.detector = VulnerabilityDetector()
        self.crisis_safeguard = CrisisDetectionSafeguard()
        self.conversation_history = []
    
    def generate_safe_response(self, user_message):
        """
        Generate a safe response with LFAS Protocol safeguards.
        
        Args:
            user_message: The user's input message
            
        Returns:
            tuple: (response_text, protection_level, is_crisis)
        """
        # LISTEN: Detect vulnerabilities
        detection_result = self.detector.detect(user_message)
        
        print(f"[LFAS] Protection Level: {detection_result.protection_level.name}")
        if detection_result.indicator_count > 0:
            print(f"[LFAS] Detected {detection_result.indicator_count} vulnerability indicators")
            print(f"[LFAS] Categories: {', '.join(detection_result.categories)}")
        
        # REFLECT & ACT: Check if crisis safeguard should activate
        if self.crisis_safeguard.should_activate(detection_result):
            print("[LFAS] ⚠️ Crisis safeguard activated - bypassing normal AI response")
            response = self.crisis_safeguard.generate_response(detection_result)
            return response, detection_result.protection_level, True
        
        # For non-crisis situations, you would call your AI API here
        # This is where you'd integrate with OpenAI, Claude, etc.
        response = self._generate_ai_response(
            user_message, 
            detection_result.protection_level
        )
        
        return response, detection_result.protection_level, False
    
    def _generate_ai_response(self, user_message, protection_level):
        """
        Generate AI response with appropriate safety level.
        
        In a real implementation, this would call OpenAI, Claude, etc.
        For this demo, we return a simulated response.
        """
        # Simulated AI response (replace with actual API call)
        if protection_level == ProtectionLevel.ENHANCED:
            return (
                f"I understand you're facing a challenging situation. "
                f"Let me provide some realistic guidance while acknowledging "
                f"the complexities involved..."
            )
        else:
            return (
                f"I'm here to help. Let me address your question..."
            )


def demo_safe_ai_chat():
    """Demonstrate the SafeAIChat wrapper."""
    print("=" * 70)
    print("LFAS Protocol - OpenAI Integration Demo")
    print("=" * 70)
    
    chat = SafeAIChat()
    
    # Test scenarios
    test_messages = [
        {
            "input": "What's the weather like today?",
            "description": "Standard query - no vulnerability"
        },
        {
            "input": "I lost my job and need to make money fast",
            "description": "Financial crisis - enhanced protection"
        },
        {
            "input": "I can't take it anymore, everything is hopeless",
            "description": "Mental health crisis - crisis protection"
        }
    ]
    
    for i, test in enumerate(test_messages, 1):
        print(f"\n{'=' * 70}")
        print(f"Test {i}: {test['description']}")
        print(f"{'=' * 70}")
        print(f"User: {test['input']}")
        print()
        
        response, level, is_crisis = chat.generate_safe_response(test['input'])
        
        print(f"\n{'─' * 70}")
        print("AI Response:")
        print(f"{'─' * 70}")
        print(response)
        print()
        
        if is_crisis:
            print("⚠️  Crisis response provided - normal AI processing bypassed")
        else:
            print(f"✓ Safe response generated at {level.name} protection level")


# Example: Real OpenAI Integration (requires openai package and API key)
def example_real_openai_integration():
    """
    Example of real OpenAI integration with LFAS.
    
    Uncomment and modify if you have OpenAI API access.
    """
    # from openai import OpenAI
    # import os
    # 
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # detector = VulnerabilityDetector()
    # safeguard = CrisisDetectionSafeguard()
    # 
    # def safe_chat_completion(user_message):
    #     # LISTEN: Detect vulnerability
    #     result = detector.detect(user_message)
    #     
    #     # ACT: Handle crisis situations
    #     if safeguard.should_activate(result):
    #         return safeguard.generate_response(result)
    #     
    #     # Modify system prompt based on protection level
    #     system_prompt = "You are a helpful AI assistant."
    #     if result.protection_level == ProtectionLevel.ENHANCED:
    #         system_prompt += (
    #             " The user may be in a vulnerable situation. "
    #             "Provide realistic, grounded advice without false optimism. "
    #             "Include appropriate disclaimers for financial or health topics."
    #         )
    #     
    #     # Generate response with OpenAI
    #     response = client.chat.completions.create(
    #         model="gpt-4",
    #         messages=[
    #             {"role": "system", "content": system_prompt},
    #             {"role": "user", "content": user_message}
    #         ]
    #     )
    #     
    #     return response.choices[0].message.content
    # 
    # # Use the safe chat completion
    # response = safe_chat_completion("I need help with my project")
    # print(response)
    
    print("\n" + "=" * 70)
    print("Real OpenAI Integration Example")
    print("=" * 70)
    print("\nTo use this with a real OpenAI API:")
    print("1. Install: pip install openai")
    print("2. Set your API key: export OPENAI_API_KEY='your-key'")
    print("3. Uncomment the code above and run")
    print("\nThe pattern:")
    print("  1. Detect vulnerability with LFAS")
    print("  2. Activate crisis response if needed")
    print("  3. Modify system prompt based on protection level")
    print("  4. Generate response with OpenAI")
    print("  5. Apply any additional safeguards to the response")


if __name__ == "__main__":
    demo_safe_ai_chat()
    example_real_openai_integration()
    
    print("\n" + "=" * 70)
    print("Integration complete! Adapt this pattern for your AI platform.")
    print("=" * 70)
