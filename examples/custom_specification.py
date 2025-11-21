#!/usr/bin/env python3
"""
LFAS Protocol v4 - Custom Specification Example

This example demonstrates how to use a custom XML specification
and reload it dynamically for updated detection patterns.
"""

from pathlib import Path
from lfas import VulnerabilityDetector, CrisisDetector, SpecificationLoader


def main():
    """Demonstrate custom specification loading and dynamic updates"""
    
    print("="*70)
    print("LFAS Protocol v4 - Custom Specification Example")
    print("="*70)
    print()
    
    # Load the default specification
    print("1. Loading Default Specification")
    print("-" * 70)
    
    loader = SpecificationLoader()
    print(f"✓ Specification loaded from: {loader.spec_path}")
    print()
    
    # Show loaded indicators
    indicators = loader.get_detection_indicators()
    print(f"Detection Categories: {len(indicators)}")
    for category, patterns in indicators.items():
        print(f"  • {category}: {len(patterns)} indicators")
    print()
    
    # Show verification requirements
    print("2. Verification Requirements (VR-20 to VR-25)")
    print("-" * 70)
    
    requirements = loader.get_verification_requirements()
    for vr_code, vr_data in requirements.items():
        print(f"{vr_code}: {vr_data['name']}")
        print(f"  {vr_data['description']}")
    print()
    
    # Show crisis resources
    print("3. Crisis Resources")
    print("-" * 70)
    
    resources = loader.get_crisis_resources()
    for crisis_type, crisis_resources in resources.items():
        print(f"{crisis_type.replace('_', ' ').title()}:")
        for resource in crisis_resources:
            print(f"  • {resource['name']}")
            print(f"    Contact: {resource['contact']}")
    print()
    
    # Use the specification with detectors
    print("4. Using Specification with Detectors")
    print("-" * 70)
    
    detector = VulnerabilityDetector()
    crisis_detector = CrisisDetector(spec_loader=loader)
    
    print("✓ VulnerabilityDetector initialized with specification")
    print("✓ CrisisDetector initialized with specification")
    print()
    
    # Test detection
    test_inputs = [
        "Hello, how are you?",
        "I lost my job recently",
        "Lost my job, can't pay rent, this is my last hope"
    ]
    
    print("Testing Detection Pipeline:")
    print()
    
    for test_input in test_inputs:
        result = detector.detect(test_input, maintain_history=False)
        
        print(f"Input: '{test_input}'")
        print(f"  Protection Level: {result.protection_level.name}")
        print(f"  Triggers: {result.triggers_count}")
        
        if result.protection_level.value >= 3:
            crisis = crisis_detector.assess_crisis(result)
            print(f"  ⚠️  Crisis Type: {crisis.crisis_type.name}")
            print(f"  Resources: {len(crisis.resources)} available")
        
        print()
    
    # Demonstrate dynamic reload
    print("5. Dynamic Specification Reload")
    print("-" * 70)
    print("The specification can be reloaded dynamically to pick up changes:")
    print()
    print("  loader.reload()")
    print("  detector.reload_specification()")
    print()
    print("This allows updating detection patterns without restarting the system.")
    print()
    
    # Show protection levels
    print("6. Protection Level Escalation Rules")
    print("-" * 70)
    
    rules = loader.get_protection_rules()
    for rule in rules.values():
        print(f"  • {rule}")
    print()
    
    # Summary
    print("="*70)
    print("Summary")
    print("="*70)
    print()
    print("The LFAS Protocol dynamically loads detection patterns from XML,")
    print("enabling:")
    print()
    print("  ✓ Customizable vulnerability indicators")
    print("  ✓ Dynamic updates without code changes")
    print("  ✓ Extensible crisis resource configuration")
    print("  ✓ Verification requirement specifications (VR-20 to VR-25)")
    print("  ✓ Protection level escalation rules")
    print()
    print("This architecture enables organizations to adapt the system")
    print("to their specific needs while maintaining the core LFAS framework.")
    print()


if __name__ == "__main__":
    main()
