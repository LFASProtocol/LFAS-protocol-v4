"""
OpenAI integration example for LFAS Protocol v4.

Demonstrates how to integrate LFAS Protocol with OpenAI's API
to add vulnerability detection and crisis safeguards.

Note: This is a demonstration. You'll need to:
1. Install openai: pip install openai
2. Set OPENAI_API_KEY environment variable
"""

from lfas_protocol import CrisisDetectionSafeguard, ProtectionLevel, VulnerabilityDetector


def simulate_openai_chat(user_message: str, system_message: str = None) -> str:
    """
    Simulate OpenAI chat completion (replace with actual OpenAI API call).

    For a real implementation, use:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(...)
    """
    # This is a simulation - replace with actual OpenAI API call
    return f"[Simulated AI Response to: {user_message[:50]}...]"


def chat_with_lfas_protection(user_message: str) -> dict:
    """
    Process user message through LFAS Protocol before AI response.

    Implements the LFAS workflow:
    1. LISTEN - Detect vulnerability indicators
    2. REFLECT - Assess protection level
    3. WAIT - (Brief pause implemented via API call sequencing)
    4. ACT - Apply safeguards or proceed with AI response
    5. ACKNOWLEDGE - Return appropriate response

    Args:
        user_message: User's input message

    Returns:
        dict with response and metadata
    """
    # Initialize LFAS components
    detector = VulnerabilityDetector()
    safeguard = CrisisDetectionSafeguard()

    # LISTEN - Detect vulnerability
    detection_result = detector.detect(user_message)

    # REFLECT - Assess protection level
    protection_level = detection_result.protection_level

    # WAIT - Pause is implicit in our workflow

    # ACT - Apply appropriate safeguards
    if protection_level == ProtectionLevel.CRISIS:
        # Crisis level: Provide immediate resources, don't generate AI response
        safeguard_response = safeguard.generate_response(detection_result)
        return {
            "response": safeguard_response.message,
            "protection_level": "CRISIS",
            "safeguard_activated": True,
            "resources": safeguard_response.resources,
            "ai_response_generated": False,
        }

    elif protection_level == ProtectionLevel.ENHANCED:
        # Enhanced level: Generate AI response with safeguard prefix
        safeguard_response = safeguard.generate_response(detection_result)

        # Modify system message to be more supportive
        enhanced_system = (
            "You are a helpful, empathetic AI assistant. "
            "The user may be going through a difficult time. "
            "Be supportive, honest, and avoid false optimism."
        )

        ai_response = simulate_openai_chat(user_message, enhanced_system)

        combined_response = f"{safeguard_response.message}\n\n{ai_response}"

        return {
            "response": combined_response,
            "protection_level": "ENHANCED",
            "safeguard_activated": True,
            "resources": [],
            "ai_response_generated": True,
        }

    else:
        # Standard level: Normal AI response
        ai_response = simulate_openai_chat(user_message)

        return {
            "response": ai_response,
            "protection_level": "STANDARD",
            "safeguard_activated": False,
            "resources": [],
            "ai_response_generated": True,
        }


def main():
    """Demonstrate LFAS + OpenAI integration."""

    print("=" * 80)
    print("LFAS Protocol v4 + OpenAI Integration Example")
    print("=" * 80)

    # Example conversations
    test_messages = [
        "What's the capital of France?",
        "I'm feeling stressed about work",
        "I'm broke and feeling hopeless",
        "I can't take it anymore, I'm broke and lost everything, I'm all alone",
    ]

    for message in test_messages:
        print(f"\n{'=' * 80}")
        print(f"User: {message}")
        print("-" * 80)

        # Process through LFAS protection
        result = chat_with_lfas_protection(message)

        print(f"Protection Level: {result['protection_level']}")
        print(f"Safeguard Activated: {result['safeguard_activated']}")
        print(f"AI Response Generated: {result['ai_response_generated']}")

        if result["resources"]:
            print(f"\nCrisis Resources Provided: {len(result['resources'])}")
            for resource in result["resources"]:
                print(f"  - {resource['name']}: {resource['contact']}")

        print("\nResponse:")
        print("-" * 80)
        print(result["response"])

    print(f"\n{'=' * 80}")
    print("Integration Notes:")
    print("=" * 80)
    print(
        """
    To use with real OpenAI API:

    1. Install OpenAI SDK:
       pip install openai

    2. Set your API key:
       export OPENAI_API_KEY='your-api-key-here'

    3. Replace simulate_openai_chat() with actual API calls:

       from openai import OpenAI
       client = OpenAI()

       response = client.chat.completions.create(
           model="gpt-4",
           messages=[
               {"role": "system", "content": system_message},
               {"role": "user", "content": user_message}
           ]
       )

       return response.choices[0].message.content

    4. The LFAS protection workflow remains the same!
    """
    )


if __name__ == "__main__":
    main()
