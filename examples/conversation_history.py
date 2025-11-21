"""
LFAS Protocol v4 - Conversation History Example
Demonstrates how conversation history is tracked and used for context
"""

from lfas import CrisisDetector, VulnerabilityDetector


def main():
    print("=" * 70)
    print("LFAS Protocol v4 - Conversation History Example")
    print("=" * 70)
    print()

    detector = VulnerabilityDetector()
    crisis_detector = CrisisDetector()

    # Simulate a conversation where vulnerability escalates
    conversation = [
        "Hi, I need some advice about career options",
        "I've been struggling to find work lately",
        "Actually, I lost my job three months ago",
        "I'm running out of money and this is my last hope",
        "I can't take it anymore, I don't know what to do",
    ]

    print("Simulating a conversation where vulnerability escalates:")
    print("-" * 70)
    print()

    for i, message in enumerate(conversation, 1):
        result = detector.detect(message)

        print(f"Turn {i}:")
        print(f"  User: {message}")
        print(f"  Protection Level: {result.protection_level.name}")
        print(f"  Triggers: {result.triggers_count}")

        if result.detected_categories:
            print(f"  Categories: {', '.join(result.detected_categories)}")

        # Check if crisis level reached
        if result.protection_level.value >= 3:
            print()
            print("  ⚠️  CRISIS LEVEL REACHED - Activating Support")
            crisis_result = crisis_detector.assess_crisis(result)
            print(f"  Crisis Type: {crisis_result.crisis_type.value}")
            print(f"  Resources Available: {len(crisis_result.primary_resources)}")

        print()

    # Show conversation history
    print("-" * 70)
    print("Complete Conversation History:")
    print("-" * 70)
    for i, msg in enumerate(detector.conversation_history, 1):
        print(f"{i}. {msg}")

    print()
    print("=" * 70)
    print(f"Total messages tracked: {len(detector.conversation_history)}")
    print("Conversation history helps maintain context for better detection.")
    print("=" * 70)


if __name__ == "__main__":
    main()
