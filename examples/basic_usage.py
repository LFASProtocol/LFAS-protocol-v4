#!/usr/bin/env python3
"""
Basic example of using LFAS Protocol v4 for vulnerability detection

This example demonstrates how to:
1. Detect vulnerability in user input
2. Determine protection level
3. Handle crisis situations
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lfas import VulnerabilityDetector, CrisisDetector


def main():
    """Run basic detection examples"""
    
    # Initialize detectors
    print("Initializing LFAS Protocol v4...")
    vuln_detector = VulnerabilityDetector()
    crisis_detector = CrisisDetector()
    
    # Example 1: Standard input (no vulnerability)
    print("\n" + "="*60)
    print("EXAMPLE 1: Standard Input")
    print("="*60)
    
    input1 = "Hello, can you help me learn Python?"
    result1 = vuln_detector.detect(input1)
    
    print(f"Input: {input1}")
    print(f"Result: {result1}")
    print(f"Is vulnerable: {result1.is_vulnerable()}")
    print(f"Is crisis: {result1.is_crisis()}")
    
    # Example 2: Single vulnerability trigger (Enhanced protection)
    print("\n" + "="*60)
    print("EXAMPLE 2: Enhanced Protection (Financial Concern)")
    print("="*60)
    
    input2 = "I just lost my job and I'm looking for ways to make money online"
    result2 = vuln_detector.detect(input2)
    
    print(f"Input: {input2}")
    print(f"Result: {result2}")
    print(f"Is vulnerable: {result2.is_vulnerable()}")
    print(f"Detected categories: {result2.detected_categories}")
    
    # Example 3: Multiple triggers (Crisis protection)
    print("\n" + "="*60)
    print("EXAMPLE 3: Crisis Protection (Multiple Triggers)")
    print("="*60)
    
    input3 = "I lost my job, this is my last hope, I can't take it anymore"
    result3 = vuln_detector.detect(input3)
    crisis_response = crisis_detector.assess_crisis(result3)
    
    print(f"Input: {input3}")
    print(f"Result: {result3}")
    print(f"Is crisis: {result3.is_crisis()}")
    print(f"\nCrisis Response:")
    print(crisis_response.format_crisis_message())
    
    # Example 4: Suicidal ideation (Immediate crisis)
    print("\n" + "="*60)
    print("EXAMPLE 4: Immediate Crisis (Suicidal Ideation)")
    print("="*60)
    
    input4 = "I want to end my life, nobody understands me, thinking about ending it"
    result4 = vuln_detector.detect(input4)
    crisis_response4 = crisis_detector.assess_crisis(result4)
    
    print(f"Input: {input4}")
    print(f"Result: {result4}")
    print(f"\nCrisis Response:")
    print(crisis_response4.format_crisis_message())
    
    # Demonstrate safe response formatting
    print("\n" + "="*60)
    print("EXAMPLE 5: Safe Response Formatting")
    print("="*60)
    
    original_ai_response = "I'm sorry to hear that. Here are some tips to feel better..."
    safe_response = crisis_detector.format_safe_response(
        crisis_response4, 
        original_ai_response
    )
    
    print("Original AI response would have been:")
    print(f"  '{original_ai_response}'")
    print("\nSafe LFAS response:")
    print(safe_response)
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
