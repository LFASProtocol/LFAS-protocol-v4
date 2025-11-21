#!/usr/bin/env python3
"""
LFAS Protocol v4 - Conversation History Example

This example demonstrates how the system maintains conversation history
and detects escalating vulnerability across multiple messages.
"""

from lfas import VulnerabilityDetector, CrisisDetector


def simulate_conversation(messages):
    """Simulate a conversation and track protection level changes"""
    
    detector = VulnerabilityDetector()
    
    print("="*70)
    print("LFAS Protocol v4 - Conversation History Example")
    print("="*70)
    print()
    print("Simulating a multi-turn conversation to demonstrate")
    print("vulnerability detection and protection level escalation...")
    print()
    
    for i, message in enumerate(messages, 1):
        print(f"Turn {i}: User")
        print("-" * 70)
        print(f"Message: {message}")
        
        result = detector.detect(message)
        
        print(f"Protection Level: {result.protection_level.name} (Level {result.protection_level.value})")
        print(f"Triggers Detected: {result.triggers_count}")
        if result.detected_categories:
            print(f"Categories: {', '.join(result.detected_categories)}")
        
        # Check for crisis
        if result.protection_level.value >= 3:
            print()
            print("⚠️  CRISIS LEVEL REACHED - Immediate intervention required")
            
            crisis_detector = CrisisDetector()
            crisis = crisis_detector.assess_crisis(result)
            
            print(f"Crisis Type: {crisis.crisis_type.name}")
            print(f"Severity: {crisis.severity}")
            print()
            
            print("Recommended Actions:")
            for action in crisis.recommended_actions[:3]:  # Show first 3 actions
                print(f"  • {action}")
            
            # In a real system, you would now modify your response behavior
            print()
            print("System Response Adjustment:")
            print("  → VR-24 Crisis Detection activated")
            print("  → VR-25 Amplification Prevention active")
            print("  → Prioritizing safety resources over task completion")
            
            break  # Stop conversation after crisis detected
        
        print()
    
    print()
    print("="*70)
    print("Conversation History Summary")
    print("="*70)
    print(f"Total Messages: {len(detector.conversation_history)}")
    print(f"Final Protection Level: {result.protection_level.name}")
    print()
    
    if result.conversation_history:
        print("Message History:")
        for i, msg in enumerate(result.conversation_history, 1):
            print(f"  {i}. {msg[:60]}{'...' if len(msg) > 60 else ''}")


def main():
    """Run conversation scenarios"""
    
    # Scenario 1: Gradual escalation
    print("\n" + "="*70)
    print("SCENARIO 1: Gradual Escalation")
    print("="*70 + "\n")
    
    gradual_messages = [
        "Hi, I need some advice about my career",
        "I've been looking for jobs for 3 months with no luck",
        "I lost my job and I'm running out of savings",
        "This is my last hope, I can't take this anymore, nobody understands"
    ]
    
    simulate_conversation(gradual_messages)
    
    # Scenario 2: Immediate crisis
    print("\n\n" + "="*70)
    print("SCENARIO 2: Immediate Crisis Detection")
    print("="*70 + "\n")
    
    immediate_messages = [
        "I don't want to live anymore, this is my last hope, nobody cares"
    ]
    
    simulate_conversation(immediate_messages)


if __name__ == "__main__":
    main()
