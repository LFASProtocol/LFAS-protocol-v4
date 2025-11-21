"""
LFAS Protocol v4 - Crisis Type Detection Example
Demonstrates different crisis types and mental health prioritization
"""

from lfas import CrisisDetector, VulnerabilityDetector


def detect_and_respond(message: str, title: str):
    """Helper function to detect and respond to a message"""
    print(f"\n{title}")
    print("=" * 70)
    print(f"Input: {message}")
    print()

    detector = VulnerabilityDetector()
    result = detector.detect(message)

    print(f"Protection Level: {result.protection_level.name}")
    print(f"Triggers: {result.triggers_count}")

    if result.protection_level.value >= 3:
        crisis_detector = CrisisDetector()
        crisis_result = crisis_detector.assess_crisis(result)

        print(f"Crisis Type: {crisis_result.crisis_type.value.upper()}")
        print()
        print("Primary Resources:")
        for resource in crisis_result.primary_resources:
            print(f"  • {resource.name}: {resource.contact}")
        print()
        print("Top Recommended Actions:")
        for action in crisis_result.recommended_actions[:3]:
            print(f"  • {action}")
    else:
        print("(Not at crisis level)")

    print()


def main():
    print("=" * 70)
    print("LFAS Protocol v4 - Crisis Type Detection Example")
    print("=" * 70)

    # Example 1: Mental Health Crisis
    detect_and_respond(
        "thinking about suicide, only chance, last hope, can't take it anymore",
        "Example 1: Mental Health Crisis",
    )

    # Example 2: Financial Crisis
    detect_and_respond(
        "lost my job, need money fast, can't pay bills", "Example 2: Financial Crisis"
    )

    # Example 3: Health Crisis
    detect_and_respond(
        "can't see a doctor, pain won't stop, no medical help", "Example 3: Health Crisis"
    )

    # Example 4: Mixed Crisis (Mental Health Prioritized)
    print("Example 4: Mixed Crisis - Mental Health Priority")
    print("=" * 70)
    print("When multiple crisis types are detected, mental health is prioritized")
    print()

    message = "lost my job, thinking about suicide, can't afford medication, only chance, last hope"
    print(f"Input: {message}")
    print()

    detector = VulnerabilityDetector()
    result = detector.detect(message)
    crisis_detector = CrisisDetector()
    crisis_result = crisis_detector.assess_crisis(result)

    print(f"Protection Level: {result.protection_level.name}")
    print(f"Triggers: {result.triggers_count}")
    print(f"Primary Crisis Type: {crisis_result.crisis_type.value.upper()}")
    print()
    print("Note: Even though financial and health issues were mentioned,")
    print("MENTAL HEALTH is prioritized as the primary crisis type.")
    print()
    print("Primary Resources (Mental Health focused):")
    for resource in crisis_result.primary_resources[:2]:
        print(f"  • {resource.name}: {resource.contact}")

    print()
    print("=" * 70)
    print("Crisis type detection ensures appropriate resources are provided.")
    print("Mental health is always prioritized in mixed-crisis situations.")
    print("=" * 70)


if __name__ == "__main__":
    main()
