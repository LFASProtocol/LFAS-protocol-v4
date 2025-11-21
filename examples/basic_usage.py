"""
Basic usage example for LFAS Protocol v4 Python library.

Demonstrates:
- Vulnerability detection
- Protection level escalation
- Crisis response safeguards
"""

from lfas_protocol import CrisisDetectionSafeguard, VulnerabilityDetector


def main():
    """Demonstrate basic LFAS Protocol usage."""

    # Initialize components
    detector = VulnerabilityDetector()
    safeguard = CrisisDetectionSafeguard()

    # Example inputs at different severity levels
    examples = [
        {
            "name": "Standard Conversation",
            "input": "What's the weather like today?",
        },
        {
            "name": "Single Vulnerability Indicator",
            "input": "I'm feeling hopeless about my situation",
        },
        {
            "name": "Enhanced Protection Level",
            "input": "I'm broke and feeling hopeless",
        },
        {
            "name": "Crisis Protection Level",
            "input": "I can't take it anymore, I'm broke and all alone",
        },
    ]

    print("=" * 80)
    print("LFAS Protocol v4 - Basic Usage Examples")
    print("=" * 80)

    for example in examples:
        print(f"\n{'=' * 80}")
        print(f"Example: {example['name']}")
        print(f"{'=' * 80}")
        print(f"Input: \"{example['input']}\"")
        print()

        # LISTEN phase - detect vulnerability
        result = detector.detect(example["input"])

        # REFLECT phase - display detection results
        print("Detection Results:")
        print(f"  Triggers: {result.trigger_count}")
        print(f"  Protection Level: {result.protection_level.name}")
        print("  Indicators:")
        for indicator in result.indicators:
            print(f"    - {indicator.category.value}: {indicator.pattern}")

        # ACT phase - generate appropriate response
        if safeguard.should_activate(result):
            response = safeguard.generate_response(result)
            print(f"\n  Crisis Safeguard Activated: {response.should_activate}")
            if response.message:
                print("\n  Safeguard Response:")
                print("  " + "-" * 76)
                for line in response.message.split("\n"):
                    print(f"  {line}")
                print("  " + "-" * 76)
        else:
            print("\n  Crisis Safeguard Activated: False")
            print("  → Standard AI response can proceed")

    print(f"\n{'=' * 80}")
    print("Available Crisis Resources:")
    print("=" * 80)
    resources = safeguard.get_crisis_resources()
    for resource in resources:
        print(f"\n  {resource['name']}")
        print(f"  Contact: {resource['contact']}")
        print(f"  Description: {resource['description']}")
        print(f"  Availability: {resource['availability']}")


if __name__ == "__main__":
    main()
