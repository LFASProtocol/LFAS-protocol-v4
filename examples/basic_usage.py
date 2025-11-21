"""
Basic Usage Example for LFAS Protocol Python Library

Demonstrates the core functionality:
1. Detecting vulnerability indicators
2. Determining protection levels
3. Activating crisis safeguards
"""

from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard, ProtectionLevel


def example_basic_detection():
    """Example 1: Basic vulnerability detection."""
    print("=" * 60)
    print("Example 1: Basic Vulnerability Detection")
    print("=" * 60)
    
    detector = VulnerabilityDetector()
    
    # Test various inputs
    test_inputs = [
        "I'm feeling great today!",
        "I lost my job and need money fast",
        "I can't take it anymore, everything is hopeless",
    ]
    
    for user_input in test_inputs:
        result = detector.detect(user_input)
        
        print(f"\nUser Input: \"{user_input}\"")
        print(f"Protection Level: {result.protection_level.name}")
        print(f"Indicators Detected: {result.indicator_count}")
        if result.triggered_indicators:
            print(f"Triggered: {', '.join(result.triggered_indicators[:3])}")
        print(f"Categories: {', '.join(result.categories) if result.categories else 'None'}")


def example_crisis_response():
    """Example 2: Crisis detection and response generation."""
    print("\n" + "=" * 60)
    print("Example 2: Crisis Detection & Response")
    print("=" * 60)
    
    detector = VulnerabilityDetector()
    safeguard = CrisisDetectionSafeguard()
    
    crisis_input = "I can't take it anymore, everything is hopeless"
    
    # Step 1: Detect vulnerability
    result = detector.detect(crisis_input)
    
    print(f"\nUser Input: \"{crisis_input}\"")
    print(f"\nDetection Result:")
    print(f"  Protection Level: {result.protection_level.name}")
    print(f"  Indicators: {result.indicator_count}")
    print(f"  Categories: {', '.join(result.categories)}")
    
    # Step 2: Check if crisis safeguard should activate
    should_activate = safeguard.should_activate(result)
    print(f"\nCrisis Safeguard Activated: {should_activate}")
    
    # Step 3: Generate appropriate response
    if should_activate:
        response = safeguard.generate_response(result)
        print(f"\nGenerated Response:")
        print("-" * 60)
        print(response)
        print("-" * 60)


def example_financial_crisis():
    """Example 3: Financial crisis scenario (from demo)."""
    print("\n" + "=" * 60)
    print("Example 3: Financial Crisis Scenario")
    print("=" * 60)
    
    detector = VulnerabilityDetector()
    safeguard = CrisisDetectionSafeguard()
    
    user_input = "I lost my job and have $100 left. I need to make money fast."
    
    result = detector.detect(user_input)
    
    print(f"\nUser Input: \"{user_input}\"")
    print(f"\nDetection Result:")
    print(f"  Protection Level: {result.protection_level.name}")
    print(f"  Indicators: {result.indicator_count}")
    print(f"  Categories: {', '.join(result.categories)}")
    
    # Note: Financial crisis may not trigger VR-24 unless combined with crisis language
    # This demonstrates the different protection levels
    if safeguard.should_activate(result):
        print("\n[VR-24 Crisis Safeguard Activated]")
        response = safeguard.generate_response(result)
        print(response)
    else:
        print("\n[Enhanced Protection - VR-23 Financial Realism would apply]")
        print("Note: For Level 2 protection, other safeguards like VR-23")
        print("(Financial Realism Verification) should be applied.")


def example_get_all_indicators():
    """Example 4: Viewing all vulnerability indicators."""
    print("\n" + "=" * 60)
    print("Example 4: Available Vulnerability Indicators")
    print("=" * 60)
    
    detector = VulnerabilityDetector()
    categories = detector.get_indicator_categories()
    
    for category, indicators in categories.items():
        print(f"\n{category.upper().replace('_', ' ')}:")
        for indicator in indicators[:5]:  # Show first 5 of each
            print(f"  • {indicator}")
        if len(indicators) > 5:
            print(f"  ... and {len(indicators) - 5} more")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  LFAS Protocol v4 - Python Reference Library".center(58) + "║")
    print("║" + "  Protecting Vulnerable Users in AI Systems".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    example_basic_detection()
    example_crisis_response()
    example_financial_crisis()
    example_get_all_indicators()
    
    print("\n" + "=" * 60)
    print("For more information:")
    print("  Repository: https://github.com/LFASProtocol/LFAS-protocol-v4")
    print("  Email: lfasprotocol@outlook.com")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
