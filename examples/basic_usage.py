#!/usr/bin/env python3
"""
LFAS Protocol v4 - Basic Usage Example

This example demonstrates the basic workflow of detecting vulnerability
and responding to crisis situations.
"""

from lfas import VulnerabilityDetector, CrisisDetector


def main():
    """Basic vulnerability and crisis detection example"""
    
    print("="*70)
    print("LFAS Protocol v4 - Basic Usage Example")
    print("="*70)
    print()
    
    # Initialize the detector
    detector = VulnerabilityDetector()
    print("✓ VulnerabilityDetector initialized")
    print()
    
    # Example 1: Standard conversation (no triggers)
    print("Example 1: Standard Conversation")
    print("-" * 70)
    
    result = detector.detect("Hello, can you help me with my project?")
    print(f"Input: 'Hello, can you help me with my project?'")
    print(f"Protection Level: {result.protection_level.name} (Level {result.protection_level.value})")
    print(f"Triggers Detected: {result.triggers_count}")
    print()
    
    # Example 2: Enhanced protection (1-2 triggers)
    print("Example 2: Enhanced Protection")
    print("-" * 70)
    
    detector.reset_history()
    result = detector.detect("I lost my job recently and need to find new income")
    print(f"Input: 'I lost my job recently and need to find new income'")
    print(f"Protection Level: {result.protection_level.name} (Level {result.protection_level.value})")
    print(f"Triggers Detected: {result.triggers_count}")
    print(f"Categories: {', '.join(result.detected_categories)}")
    print()
    
    # Example 3: Crisis situation (3+ triggers)
    print("Example 3: Crisis Detection & Response")
    print("-" * 70)
    
    detector.reset_history()
    crisis_input = "I lost my job, this is my last hope, can't take it anymore"
    result = detector.detect(crisis_input)
    
    print(f"Input: '{crisis_input}'")
    print(f"Protection Level: {result.protection_level.name} (Level {result.protection_level.value})")
    print(f"Triggers Detected: {result.triggers_count}")
    print(f"Categories: {', '.join(result.detected_categories)}")
    print()
    
    # When crisis level is reached, assess and provide resources
    if result.protection_level.value >= 3:
        print("⚠️  CRISIS DETECTED - Activating VR-24 Crisis Response")
        print()
        
        crisis_detector = CrisisDetector()
        crisis = crisis_detector.assess_crisis(result)
        
        print(f"Crisis Type: {crisis.crisis_type.name}")
        print(f"Severity: {crisis.severity}")
        print(f"Resources Available: {len(crisis.resources)}")
        print()
        
        print("CRISIS INTERVENTION MESSAGE:")
        print("="*70)
        print(crisis.format_crisis_message())
        print("="*70)


if __name__ == "__main__":
    main()
