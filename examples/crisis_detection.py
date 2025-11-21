#!/usr/bin/env python3
"""
Crisis Detection Example - VR-24 Implementation

This script demonstrates the LFAS Crisis Detection & Response (VR-24)
safeguard, showing how to detect crisis situations and provide
appropriate resources.
"""

from lfas import CrisisDetector, VulnerabilityDetector


def main() -> None:
    """Run crisis detection examples."""
    print("=" * 70)
    print("LFAS Protocol v4 - Crisis Detection & Response (VR-24)")
    print("=" * 70)
    print()

    # Initialize detectors
    vuln_detector = VulnerabilityDetector()
    crisis_detector = CrisisDetector()
    print("✓ Detectors initialized")
    print()

    # Example scenarios
    scenarios = [
        {
            "name": "Mental Health Crisis",
            "input": (
                "I'm thinking about ending it all. I don't want to live "
                "anymore. This is my last hope."
            ),
        },
        {
            "name": "Financial Crisis",
            "input": (
                "I lost my job, can't pay my bills, and I'm facing eviction. "
                "This is my last hope."
            ),
        },
        {
            "name": "Health Crisis",
            "input": (
                "I can't see a doctor, I have no insurance, and the pain "
                "won't stop. I don't know what to do."
            ),
        },
        {
            "name": "Multiple Crisis Types",
            "input": (
                "I lost my job, I have no one to talk to, I can't see a doctor, "
                "and I'm thinking about ending it. This is my last hope."
            ),
        },
        {
            "name": "No Crisis - Enhanced Protection",
            "input": "I lost my job and need money fast.",
        },
        {
            "name": "No Crisis - Standard",
            "input": "I'm looking for career advice.",
        },
    ]

    # Run through each scenario
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'═' * 70}")
        print(f"Scenario {i}: {scenario['name']}")
        print(f"{'═' * 70}")
        print(f"Input: {scenario['input'][:60]}{'...' if len(scenario['input']) > 60 else ''}")
        print()

        # Detect vulnerabilities
        vuln_result = vuln_detector.detect(scenario["input"])

        # Assess crisis
        crisis_response = crisis_detector.assess_crisis(vuln_result)

        # Display vulnerability detection results
        print(f"Protection Level: {vuln_result.protection_level.name}")
        print(f"Trigger Count: {vuln_result.trigger_count}")

        if vuln_result.triggered_categories:
            categories = ", ".join(sorted(vuln_result.triggered_categories))
            print(f"Categories: {categories}")

        print()

        # Display crisis assessment
        if crisis_response.crisis_detected:
            print(f"🚨 CRISIS DETECTED: {crisis_response.crisis_type}")
            print()

            # Show resources
            if crisis_response.resources:
                print("Crisis Resources:")
                for resource in crisis_response.resources:
                    print(f"\n  • {resource.name}")
                    print(f"    {resource.description}")
                    print(f"    Contact: {resource.contact}")
                    if resource.region != "US":
                        print(f"    Region: {resource.region}")

            print()

            # Show recommended actions (first 5)
            print("Recommended Actions:")
            for action in crisis_response.recommended_actions[:5]:
                print(f"  ✓ {action}")

            if len(crisis_response.recommended_actions) > 5:
                remaining = len(crisis_response.recommended_actions) - 5
                print(f"  ... and {remaining} more")

            # Show formatted message
            print()
            print("─" * 70)
            print("User-Facing Message:")
            print("─" * 70)
            message = crisis_detector.format_crisis_message(crisis_response)
            # Indent the message
            for line in message.split("\n"):
                print(f"  {line}")
        else:
            print("✓ No crisis detected")
            print("  Apply standard or enhanced protection as appropriate")

    print()
    print("=" * 70)
    print("Crisis detection examples complete!")
    print("=" * 70)
    print()
    print("Key Takeaways:")
    print("  • VR-24 activates at Protection Level 3 (Crisis)")
    print("  • Different crisis types receive appropriate resources")
    print("  • Mental health crises are prioritized in mixed scenarios")
    print("  • Recommended actions guide the AI system's response")
    print("  • User-facing messages provide immediate help resources")


if __name__ == "__main__":
    main()
