"""
LFAS Protocol v4 - Anthropic Integration Example
Demonstrates how to use LFAS-protected Anthropic Claude API
"""

import os
from lfas_anthropic import LFASAnthropic, create_lfas_client


def example_basic_usage():
    """Basic usage example"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)
    
    # Create LFAS-protected client
    api_key = os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key)
    
    # Standard conversation (no triggers)
    messages = [
        {"role": "user", "content": "What's the capital of France?"}
    ]
    
    response = lfas.create_message(messages)
    
    print(f"User: {messages[0]['content']}")
    print(f"Assistant: {response['content']}")
    print(f"Protection Level: {response['metadata']['protection_level']}")
    print(f"Triggers: {response['metadata']['triggers_detected']}")
    print()


def example_financial_vulnerability():
    """Example with financial desperation triggers"""
    print("=" * 60)
    print("EXAMPLE 2: Financial Vulnerability Detection")
    print("=" * 60)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key)
    
    # Message with financial desperation triggers
    messages = [
        {
            "role": "user", 
            "content": "I'm facing eviction and need money fast. What can I do to get rich quickly?"
        }
    ]
    
    response = lfas.create_message(messages)
    
    print(f"User: {messages[0]['content']}")
    print(f"\nAssistant: {response['content']}")
    print(f"\n--- LFAS Metadata ---")
    print(f"Protection Level: {response['metadata']['protection_level']}")
    print(f"Triggers Detected: {response['metadata']['triggers_detected']}")
    print(f"Trigger Details: {response['metadata']['trigger_details']}")
    print(f"Safeguards Applied: {', '.join(response['metadata']['safeguards_applied'])}")
    print()


def example_crisis_detection():
    """Example with crisis language triggers"""
    print("=" * 60)
    print("EXAMPLE 3: Crisis Detection & Response")
    print("=" * 60)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key)
    
    # Message with crisis triggers
    messages = [
        {
            "role": "user",
            "content": "This is my last hope. I can't take it anymore and nobody understands."
        }
    ]
    
    response = lfas.create_message(messages)
    
    print(f"User: {messages[0]['content']}")
    print(f"\nAssistant: {response['content']}")
    print(f"\n--- LFAS Metadata ---")
    print(f"Protection Level: {response['metadata']['protection_level']}")
    print(f"Triggers Detected: {response['metadata']['triggers_detected']}")
    print(f"Safeguards Applied: {', '.join(response['metadata']['safeguards_applied'])}")
    print()


def example_multi_turn_conversation():
    """Example showing multi-turn conversation"""
    print("=" * 60)
    print("EXAMPLE 4: Multi-Turn Conversation")
    print("=" * 60)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key)
    
    # First turn with vulnerability
    messages = [
        {"role": "user", "content": "I lost my job and I'm desperate"}
    ]
    response1 = lfas.create_message(messages)
    print(f"Turn 1 - Protection Level: {response1['metadata']['protection_level']}")
    
    # Second turn
    messages.append({"role": "assistant", "content": response1['content']})
    messages.append({"role": "user", "content": "What should I do?"})
    response2 = lfas.create_message(messages)
    print(f"Turn 2 - Protection Level: {response2['metadata']['protection_level']}")
    
    # Third turn without triggers
    messages.append({"role": "assistant", "content": response2['content']})
    messages.append({"role": "user", "content": "Thanks for the advice"})
    response3 = lfas.create_message(messages)
    print(f"Turn 3 - Protection Level: {response3['metadata']['protection_level']}")
    
    # View full history
    history = lfas.get_conversation_history()
    print(f"\nTotal exchanges tracked by LFAS: {len(history)}")
    print()


def example_health_crisis():
    """Example with health crisis triggers"""
    print("=" * 60)
    print("EXAMPLE 5: Health Crisis Detection")
    print("=" * 60)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key)
    
    messages = [
        {
            "role": "user",
            "content": "I have severe pain but I can't afford medication and have no insurance. What should I do?"
        }
    ]
    
    response = lfas.create_message(messages)
    
    print(f"User: {messages[0]['content']}")
    print(f"\nAssistant: {response['content']}")
    print(f"\n--- LFAS Metadata ---")
    print(f"Protection Level: {response['metadata']['protection_level']}")
    print(f"Triggers: {response['metadata']['trigger_details']}")
    print()


def example_comparison():
    """Show difference between raw and LFAS-protected responses"""
    print("=" * 60)
    print("EXAMPLE 6: Raw vs LFAS-Protected Response")
    print("=" * 60)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key)
    
    messages = [
        {
            "role": "user",
            "content": "Tell me how to get rich with cryptocurrency"
        }
    ]
    
    response = lfas.create_message(messages)
    
    print("User:", messages[0]['content'])
    print("\n--- Raw Response (before LFAS) ---")
    print(response['raw_response'][:300] + "...")
    print("\n--- LFAS-Protected Response ---")
    print(response['content'][:300] + "...")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 8 + "LFAS Protocol v4 - Anthropic Examples" + " " * 11 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Note: Set ANTHROPIC_API_KEY environment variable to run these examples
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  Set ANTHROPIC_API_KEY environment variable to run examples")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        print()
    
    print("These examples demonstrate LFAS Protocol integration with Anthropic Claude.")
    print("Uncomment the examples you want to run.\n")
    
    # Uncomment to run examples:
    # example_basic_usage()
    # example_financial_vulnerability()
    # example_crisis_detection()
    # example_multi_turn_conversation()
    # example_health_crisis()
    # example_comparison()
