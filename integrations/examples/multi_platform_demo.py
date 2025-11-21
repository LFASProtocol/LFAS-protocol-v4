"""
LFAS Protocol v4 - Multi-Platform Demo

This example demonstrates LFAS integration across different AI platforms.
Note: You'll need API keys for the platforms you want to test.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def demo_openai():
    """Demonstrate OpenAI integration with LFAS."""
    print("\n" + "=" * 60)
    print("OpenAI + LFAS Demo")
    print("=" * 60)
    
    try:
        # Import check only - the actual usage example is shown below
        import sys
        import os
        # Verify the module exists
        openai_path = os.path.join(os.path.dirname(__file__), '..', 'openai')
        if os.path.exists(openai_path):
            print("✅ OpenAI integration loaded successfully")
        
        print("\nExample usage:")
        print("""
from integrations.openai import LFASOpenAIClient

client = LFASOpenAIClient(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "I lost my job and need money fast"}
    ]
)

print(response.choices[0].message.content)
print(f"Protection Level: {response.protection_level}")
        """)
    except ImportError as e:
        print(f"❌ OpenAI integration not available: {e}")
        print("   Install with: pip install openai")


def demo_anthropic():
    """Demonstrate Anthropic integration with LFAS."""
    print("\n" + "=" * 60)
    print("Anthropic (Claude) + LFAS Demo")
    print("=" * 60)
    
    try:
        # Import check only - the actual usage example is shown below
        import sys
        import os
        anthropic_path = os.path.join(os.path.dirname(__file__), '..', 'anthropic')
        if os.path.exists(anthropic_path):
            print("✅ Anthropic integration loaded successfully")
        
        print("\nExample usage:")
        print("""
from integrations.anthropic import LFASAnthropicClient

client = LFASAnthropicClient(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "I can't take it anymore"}
    ]
)

print(response.content[0].text)
print(f"Protection Level: {response.protection_level}")
        """)
    except ImportError as e:
        print(f"❌ Anthropic integration not available: {e}")
        print("   Install with: pip install anthropic")


def demo_google():
    """Demonstrate Google Gemini integration with LFAS."""
    print("\n" + "=" * 60)
    print("Google Gemini + LFAS Demo")
    print("=" * 60)
    
    try:
        # Import check only - the actual usage example is shown below
        import sys
        import os
        google_path = os.path.join(os.path.dirname(__file__), '..', 'google')
        if os.path.exists(google_path):
            print("✅ Google Gemini integration loaded successfully")
        
        print("\nExample usage:")
        print("""
from integrations.google import LFASGeminiClient

client = LFASGeminiClient(
    model_name="gemini-pro",
    api_key="your-api-key"
)

response = client.generate_content(
    "I'm completely alone and nobody understands"
)

print(response.text)
print(f"Protection Level: {response.protection_level}")
        """)
    except ImportError as e:
        print(f"❌ Google Gemini integration not available: {e}")
        print("   Install with: pip install google-generativeai")


def demo_core_middleware():
    """Demonstrate core middleware (platform-agnostic)."""
    print("\n" + "=" * 60)
    print("Core Middleware Demo (Platform-Agnostic)")
    print("=" * 60)
    
    from core import LFASMiddleware
    
    print("✅ Core middleware loaded successfully")
    
    # Initialize middleware
    lfas = LFASMiddleware()
    
    # Mock AI response generator
    def mock_ai(user_input):
        return "This is a generic AI response to your query."
    
    # Test scenarios
    scenarios = [
        ("Hello, how are you?", "Standard conversation"),
        ("I lost my job and need money fast", "Financial desperation"),
        ("I can't take it anymore, this is my last hope", "Crisis situation"),
    ]
    
    print("\nTesting different scenarios:\n")
    
    for user_input, description in scenarios:
        print(f"Scenario: {description}")
        print(f"Input: {user_input}")
        
        result = lfas.process_request(user_input, mock_ai)
        
        print(f"Protection Level: {result['metadata']['protection_level']}")
        print(f"Trigger Count: {result['metadata']['trigger_count']}")
        
        if result['metadata']['detected_categories']:
            print(f"Detected: {', '.join(result['metadata']['detected_categories'])}")
        
        print(f"Response Preview: {result['response'][:100]}...")
        print()


def main():
    """Run all demos."""
    print("=" * 60)
    print("LFAS Protocol v4 - Multi-Platform Integration Demo")
    print("=" * 60)
    print("\nThis demo shows LFAS integrations for multiple AI platforms.")
    print("Each integration provides drop-in middleware with LFAS protection.\n")
    
    # Demo core middleware (always available)
    demo_core_middleware()
    
    # Demo platform-specific integrations
    demo_openai()
    demo_anthropic()
    demo_google()
    
    print("\n" + "=" * 60)
    print("Demo Complete")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Install the SDK for your AI platform (pip install openai/anthropic/google-generativeai)")
    print("2. Set up your API keys")
    print("3. Use the integration examples above in your application")
    print("4. Check out examples/simple_chatbot.py for a working chatbot")
    print("\nFor more information, see integrations/README.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
