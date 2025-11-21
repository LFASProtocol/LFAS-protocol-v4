#!/usr/bin/env python3
"""
Basic example demonstrating LFAS vulnerability detection.

This script shows how to use the VulnerabilityDetector to analyze
user input and determine appropriate protection levels.
"""

from lfas import ProtectionLevel, VulnerabilityDetector


def main() -> None:
    """Run basic vulnerability detection examples."""
    print("=" * 70)
    print("LFAS Protocol v4 - Basic Vulnerability Detection Examples")
    print("=" * 70)
    print()

    # Initialize the detector
    detector = VulnerabilityDetector()
    print("✓ Vulnerability detector initialized")
    print(f"✓ Loaded {sum(len(v) for v in detector.indicators.values())} indicators")
    print()

    # Example scenarios
    scenarios = [
        {
            "name": "Standard Interaction",
            "input": "I'm learning Python programming today.",
            "expected": ProtectionLevel.STANDARD,
        },
        {
            "name": "Single Vulnerability Indicator",
            "input": "I lost my job recently but I'm doing okay.",
            "expected": ProtectionLevel.STANDARD,
        },
        {
            "name": "Enhanced Protection Needed",
            "input": "I lost my job and need money fast.",
            "expected": ProtectionLevel.ENHANCED,
        },
        {
            "name": "Crisis Detection - Financial",
            "input": "I lost my job, can't pay bills, and this is my last hope.",
            "expected": ProtectionLevel.CRISIS,
        },
        {
            "name": "Crisis Detection - Mental Health",
            "input": "I'm thinking about ending it all. I don't want to live anymore. "
            "This is my last hope.",
            "expected": ProtectionLevel.CRISIS,
        },
        {
            "name": "Multiple Category Detection",
            "input": "I lost my job, I have no one to talk to, and I can't see a doctor. "
            "This is my last hope.",
            "expected": ProtectionLevel.CRISIS,
        },
    ]

    # Run through each scenario
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'─' * 70}")
        print(f"Scenario {i}: {scenario['name']}")
        print(f"{'─' * 70}")
        print(f"Input: {scenario['input'][:60]}{'...' if len(scenario['input']) > 60 else ''}")
        print()

        # Detect vulnerabilities
        result = detector.detect(scenario["input"])

        # Display results
        level_name = result.protection_level.name
        level_value = result.protection_level.value
        print(f"Protection Level: {level_name} (Level {level_value})")
        print(f"Trigger Count: {result.trigger_count}")

        if result.triggered_categories:
            print(f"Categories Detected: {', '.join(sorted(result.triggered_categories))}")

        if result.triggered_indicators:
            print("Specific Indicators:")
            for indicator in sorted(set(result.triggered_indicators)):
                print(f"  • {indicator}")

        # Show recommended action
        print()
        if result.protection_level == ProtectionLevel.CRISIS:
            print("🚨 RECOMMENDED ACTION: CRISIS PROTOCOL")
            print("   → Provide immediate crisis resources")
            print("   → Encourage professional help")
            print("   → Avoid productivity/business advice")
        elif result.protection_level == ProtectionLevel.ENHANCED:
            print("⚠️  RECOMMENDED ACTION: ENHANCED SAFEGUARDS")
            print("   → Apply reality checking")
            print("   → Provide disclaimers")
            print("   → Encourage human consultation")
        else:
            print("✓  RECOMMENDED ACTION: STANDARD SAFEGUARDS")
            print("   → Apply basic honesty safeguards")
            print("   → Provide balanced information")

    print(f"\n{'=' * 70}")
    print("All scenarios processed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
