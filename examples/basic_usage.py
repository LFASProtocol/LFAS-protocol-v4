"""
Basic usage example for LFAS Protocol v4.

This demonstrates how to use the vulnerability detector
to analyze user messages and determine protection levels.
"""

from lfas_protocol import VulnerabilityDetector, ProtectionLevel


def main():
    # Initialize the detector
    detector = VulnerabilityDetector()

    # Example messages
    messages = [
        "Hello, can you help me learn Python?",
        "I lost my job and have $100 left. Need money fast.",
        "I can't take it anymore, everything is hopeless",
    ]

    print("LFAS Protocol v4 - Vulnerability Detection Demo")
    print("=" * 60)

    for i, message in enumerate(messages, 1):
        print(f"\nExample {i}:")
        print(f"User: {message}")
        print("-" * 60)

        # Analyze the message
        result = detector.analyze(message)

        # Display results
        print(f"Protection Level: {result['protection_level'].name}")
        print(f"Triggers Detected: {result['trigger_count']}")

        if result["triggers"]:
            print(f"Trigger Categories: {', '.join(result['triggers'])}")
            print(f"Matched Phrases: {', '.join(result['matched_phrases'])}")
        else:
            print("No vulnerability indicators detected")

        # Suggest appropriate response strategy
        if result["protection_level"] == ProtectionLevel.CRISIS:
            print("\n⚠️  CRISIS MODE: Apply VR-24 (Crisis Detection)")
            print("   Provide immediate support resources")
        elif result["protection_level"] == ProtectionLevel.ENHANCED:
            print("\n⚡ ENHANCED MODE: Apply relevant safeguards")
            print("   Use cautious, realistic language")
        else:
            print("\n✓ STANDARD MODE: Normal interaction")


if __name__ == "__main__":
    main()
