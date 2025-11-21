"""
LFAS Protocol v4 - Basic Usage Example
Demonstrates basic vulnerability detection and crisis response
"""

from lfas import VulnerabilityDetector, CrisisDetector

def main():
    print("=" * 70)
    print("LFAS Protocol v4 - Basic Usage Example")
    print("=" * 70)
    print()
    
    # Initialize the detector
    detector = VulnerabilityDetector()
    
    # Example 1: Standard Protection Level
    print("Example 1: Standard User Input")
    print("-" * 70)
    input1 = "Hello, I'm interested in learning Python programming"
    result1 = detector.detect(input1)
    print(f"Input: {input1}")
    print(f"Protection Level: {result1.protection_level.name}")
    print(f"Triggers Detected: {result1.triggers_count}")
    print()
    
    # Example 2: Enhanced Protection Level
    print("Example 2: Enhanced Protection (Vulnerability Detected)")
    print("-" * 70)
    detector.reset_history()
    input2 = "I lost my job last week and I'm worried about bills"
    result2 = detector.detect(input2)
    print(f"Input: {input2}")
    print(f"Protection Level: {result2.protection_level.name}")
    print(f"Triggers Detected: {result2.triggers_count}")
    print(f"Categories: {', '.join(result2.detected_categories)}")
    print()
    
    # Example 3: Crisis Protection Level
    print("Example 3: Crisis Protection (Immediate Support Needed)")
    print("-" * 70)
    detector.reset_history()
    input3 = "I lost my job, this is my last hope, can't take it anymore"
    result3 = detector.detect(input3)
    print(f"Input: {input3}")
    print(f"Protection Level: {result3.protection_level.name}")
    print(f"Triggers Detected: {result3.triggers_count}")
    print(f"Categories: {', '.join(result3.detected_categories)}")
    print()
    
    # When crisis level is detected, activate crisis support
    if result3.protection_level.value >= 3:
        print("🚨 ACTIVATING CRISIS SUPPORT 🚨")
        print()
        crisis_detector = CrisisDetector()
        crisis_result = crisis_detector.assess_crisis(result3)
        
        print(f"Crisis Type: {crisis_result.crisis_type.value}")
        print()
        print(crisis_result.format_crisis_message())
    
    print()
    print("=" * 70)
    print("Example completed. All protection levels demonstrated.")
    print("=" * 70)


if __name__ == "__main__":
    main()
