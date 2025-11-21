"""
LFAS Protocol v4 - OpenAI Integration Example
Demonstrates how to use LFAS-protected OpenAI API
"""

import os
from lfas_openai import LFASOpenAI, create_lfas_client


def example_basic_usage():
    """Basic usage example"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)
    
    # Create LFAS-protected client
    api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key, model="gpt-4")
    
    # Standard conversation (no triggers)
    messages = [
        {"role": "user", "content": "What's the weather like today?"}
    ]
    
    response = lfas.chat_completion(messages)
    
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
    
    api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key, model="gpt-4")
    
    # Message with financial desperation triggers
    messages = [
        {
            "role": "user", 
            "content": "I lost my job and I'm desperate for income. Can you help me make money fast?"
        }
    ]
    
    response = lfas.chat_completion(messages)
    
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
    
    api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key, model="gpt-4")
    
    # Message with crisis triggers
    messages = [
        {
            "role": "user",
            "content": "I can't take it anymore. Nobody understands me and I'm completely alone. This is my last hope."
        }
    ]
    
    response = lfas.chat_completion(messages)
    
    print(f"User: {messages[0]['content']}")
    print(f"\nAssistant: {response['content']}")
    print(f"\n--- LFAS Metadata ---")
    print(f"Protection Level: {response['metadata']['protection_level']}")
    print(f"Triggers Detected: {response['metadata']['triggers_detected']}")
    print(f"Safeguards Applied: {', '.join(response['metadata']['safeguards_applied'])}")
    print()


def example_conversation_history():
    """Example showing conversation tracking"""
    print("=" * 60)
    print("EXAMPLE 4: Multi-Turn Conversation")
    print("=" * 60)
    
    api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key, model="gpt-4")
    
    # First message with vulnerability
    messages1 = [
        {"role": "user", "content": "I need money fast, can't pay bills"}
    ]
    response1 = lfas.chat_completion(messages1)
    print(f"Turn 1 - Protection Level: {response1['metadata']['protection_level']}")
    
    # Second message without vulnerability
    messages2 = [
        {"role": "user", "content": "I need money fast, can't pay bills"},
        {"role": "assistant", "content": response1['content']},
        {"role": "user", "content": "Thanks for the advice"}
    ]
    response2 = lfas.chat_completion(messages2)
    print(f"Turn 2 - Protection Level: {response2['metadata']['protection_level']}")
    
    # View conversation history
    history = lfas.get_conversation_history()
    print(f"\nTotal exchanges: {len(history)}")
    print()


def example_comparison():
    """Show difference between raw and LFAS-protected responses"""
    print("=" * 60)
    print("EXAMPLE 5: Raw vs LFAS-Protected Response")
    print("=" * 60)
    
    api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
    lfas = create_lfas_client(api_key=api_key, model="gpt-4")
    
    messages = [
        {
            "role": "user",
            "content": "I want to start a business that will make me rich quickly"
        }
    ]
    
    response = lfas.chat_completion(messages)
    
    print("User:", messages[0]['content'])
    print("\n--- Raw Response (before LFAS) ---")
    print(response['raw_response'])
    print("\n--- LFAS-Protected Response ---")
    print(response['content'])
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "LFAS Protocol v4 - OpenAI Examples" + " " * 13 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Note: Set OPENAI_API_KEY environment variable to run these examples
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY environment variable to run examples")
        print("   export OPENAI_API_KEY='your-key-here'")
        print()
    
    print("These examples demonstrate LFAS Protocol integration with OpenAI.")
    print("Uncomment the examples you want to run.\n")
    
    # Uncomment to run examples:
    # example_basic_usage()
    # example_financial_vulnerability()
    # example_crisis_detection()
    # example_conversation_history()
    # example_comparison()
