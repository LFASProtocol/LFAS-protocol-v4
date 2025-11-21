"""
LFAS Protocol v4 - Simple Chatbot Example

This example demonstrates a basic chatbot with LFAS protection
using the platform-agnostic core middleware.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import LFASMiddleware


def simple_ai_responder(user_input: str) -> str:
    """
    A simple AI responder (placeholder for actual AI).
    In a real application, this would call your AI platform.
    """
    # This is just a mock - replace with actual AI calls
    responses = {
        "hello": "Hello! How can I help you today?",
        "default": "I understand. Let me think about that..."
    }
    
    user_lower = user_input.lower()
    for keyword, response in responses.items():
        if keyword in user_lower:
            return response
    
    return responses["default"]


def main():
    """Run the simple chatbot."""
    print("=" * 60)
    print("LFAS-Protected Chatbot")
    print("=" * 60)
    print("Type 'quit' to exit\n")
    
    # Initialize LFAS middleware
    lfas = LFASMiddleware()
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nGoodbye! Stay safe.")
            break
        
        # Process through LFAS
        result = lfas.process_request(user_input, simple_ai_responder)
        
        # Display response
        print(f"\nAssistant: {result['response']}\n")
        
        # Display LFAS metadata
        metadata = result['metadata']
        print(f"[LFAS Status]")
        print(f"  Protection Level: {metadata['protection_level']}")
        print(f"  Triggers: {metadata['trigger_count']}")
        
        if metadata['detected_categories']:
            print(f"  Detected: {', '.join(metadata['detected_categories'])}")
        
        print()


if __name__ == "__main__":
    # Test scenarios
    print("\n" + "=" * 60)
    print("Test Scenario 1: Normal Conversation")
    print("=" * 60)
    
    lfas = LFASMiddleware()
    
    test_input = "Hello, how are you?"
    result = lfas.process_request(test_input, simple_ai_responder)
    print(f"Input: {test_input}")
    print(f"Response: {result['response']}")
    print(f"Protection Level: {result['metadata']['protection_level']}\n")
    
    print("=" * 60)
    print("Test Scenario 2: Financial Desperation")
    print("=" * 60)
    
    test_input = "I lost my job and have my last $100. I need money fast."
    result = lfas.process_request(test_input, simple_ai_responder)
    print(f"Input: {test_input}")
    print(f"Response: {result['response']}")
    print(f"Protection Level: {result['metadata']['protection_level']}")
    print(f"Detected Categories: {result['metadata']['detected_categories']}\n")
    
    print("=" * 60)
    print("Test Scenario 3: Crisis Situation")
    print("=" * 60)
    
    test_input = "I can't take it anymore. Nobody understands. This is my last hope."
    result = lfas.process_request(test_input, simple_ai_responder)
    print(f"Input: {test_input}")
    print(f"Response: {result['response']}")
    print(f"Protection Level: {result['metadata']['protection_level']}")
    print(f"Detected Categories: {result['metadata']['detected_categories']}\n")
    
    print("=" * 60)
    print("\nTo run the interactive chatbot, comment out the test scenarios")
    print("and uncomment the main() function call below.")
    print("=" * 60)
    
    # Uncomment to run interactive chatbot:
    # main()
