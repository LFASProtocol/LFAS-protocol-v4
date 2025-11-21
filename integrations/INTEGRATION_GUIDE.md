# LFAS Protocol v4 - Building Custom Integrations

This guide shows you how to build your own LFAS integration for any AI platform.

## Overview

All LFAS integrations follow the same pattern:

1. **Use the core middleware** - Platform-agnostic LFAS logic
2. **Wrap your AI platform** - Create a thin wrapper around the platform's API
3. **Apply LFAS safeguards** - Integrate the 5-phase protocol

## Quick Start: Minimal Integration

Here's the simplest possible LFAS integration:

```python
from integrations.core import LFASMiddleware

# Initialize LFAS
lfas = LFASMiddleware()

# Your AI function
def my_ai_platform(user_input):
    # Call your AI platform here
    return "AI response"

# Process through LFAS
result = lfas.process_request(user_input, my_ai_platform)

# Use the safe response
safe_response = result['response']
protection_level = result['metadata']['protection_level']
```

That's it! You now have LFAS protection.

## Building a Full Integration

For a production integration, follow these steps:

### Step 1: Create the Middleware Class

```python
from integrations.core import LFASMiddleware, ProtectionLevel

class MyPlatformLFASMiddleware:
    def __init__(self, platform_client=None):
        self.lfas = LFASMiddleware()
        self.client = platform_client
    
    def create_system_prompt(self, protection_level: ProtectionLevel) -> str:
        """Create LFAS-enhanced system prompt."""
        base = "You follow the LFAS Protocol v4 for user safety.\n"
        
        if protection_level >= ProtectionLevel.ENHANCED:
            base += "Enhanced protection active.\n"
        
        if protection_level >= ProtectionLevel.CRISIS:
            base += "CRISIS MODE: Focus on user safety.\n"
        
        return base
    
    def process_message(self, user_input: str, **kwargs):
        """Process a message with LFAS protection."""
        
        def generate_response(input_text):
            # Get current protection level
            level = self.lfas.protection_manager.get_current_level()
            
            # Create LFAS system prompt
            system_prompt = self.create_system_prompt(level)
            
            # Call your platform
            response = self.client.generate(
                prompt=system_prompt + "\n" + input_text,
                **kwargs
            )
            
            return response
        
        # Process through LFAS
        return self.lfas.process_request(user_input, generate_response)
```

### Step 2: Create a Client Wrapper

```python
class LFASMyPlatformClient:
    """Drop-in replacement for MyPlatform client."""
    
    def __init__(self, api_key=None):
        # Initialize your platform client
        from myplatform import Client
        self.client = Client(api_key=api_key)
        
        # Initialize LFAS middleware
        self.middleware = MyPlatformLFASMiddleware(self.client)
    
    def generate(self, prompt, **kwargs):
        """Generate with LFAS protection."""
        result = self.middleware.process_message(prompt, **kwargs)
        return MyPlatformResponse(result)
```

### Step 3: Create a Response Object

```python
class MyPlatformResponse:
    """Response object with LFAS metadata."""
    
    def __init__(self, lfas_result):
        self.text = lfas_result['response']
        self.lfas_metadata = lfas_result['metadata']
    
    @property
    def protection_level(self):
        return self.lfas_metadata['protection_level']
```

### Step 4: Export Your Integration

```python
# __init__.py
from .middleware import MyPlatformLFASMiddleware
from .client import LFASMyPlatformClient

__all__ = ['MyPlatformLFASMiddleware', 'LFASMyPlatformClient']
```

## Integration Patterns

### Pattern 1: Pre-Processing (Recommended)

Add LFAS before calling the AI:

```python
# 1. Detect vulnerabilities
detected = lfas.detector.detect(user_input)

# 2. Determine protection level
level = lfas.protection_manager.update(trigger_count)

# 3. Modify system prompt based on level
system_prompt = create_lfas_prompt(level)

# 4. Call AI with enhanced prompt
ai_response = platform.generate(system_prompt, user_input)

# 5. Apply final safeguards
safe_response = lfas.safeguard_engine.apply_safeguards(
    ai_response, level, detected_categories
)
```

### Pattern 2: Post-Processing

Add LFAS after getting the AI response:

```python
# 1. Call your AI platform
ai_response = platform.generate(user_input)

# 2. Apply LFAS protection
result = lfas.process_with_response(user_input, ai_response)

# 3. Use safe response
safe_response = result['response']
```

### Pattern 3: Hybrid (Best)

Combine both approaches:

```python
# 1. Pre-process: Enhance system prompt
level = get_protection_level(user_input)
system_prompt = create_lfas_prompt(level)

# 2. Generate AI response
ai_response = platform.generate(system_prompt, user_input)

# 3. Post-process: Apply additional safeguards
safe_response = apply_safeguards(ai_response, level)
```

## Platform-Specific Considerations

### For Chat APIs (OpenAI-style)

```python
def process_chat(messages):
    # Extract user message
    user_msg = messages[-1]['content']
    
    # Get protection level
    level = detect_and_determine_level(user_msg)
    
    # Add LFAS system message
    lfas_messages = [
        {"role": "system", "content": create_lfas_prompt(level)},
        *messages
    ]
    
    # Call platform
    response = platform.chat(lfas_messages)
    
    # Apply safeguards
    return apply_safeguards(response, level)
```

### For Completion APIs (Claude-style)

```python
def process_completion(prompt, system=None):
    # Get protection level
    level = detect_and_determine_level(prompt)
    
    # Enhance system prompt
    lfas_system = create_lfas_prompt(level)
    if system:
        lfas_system = system + "\n\n" + lfas_system
    
    # Call platform
    response = platform.complete(
        prompt=prompt,
        system=lfas_system
    )
    
    # Apply safeguards
    return apply_safeguards(response, level)
```

### For Streaming APIs

```python
async def process_streaming(prompt):
    # Get protection level first
    level = detect_and_determine_level(prompt)
    
    # Enhance prompt
    enhanced_prompt = create_lfas_prompt(level) + "\n" + prompt
    
    # Stream response
    full_response = ""
    async for chunk in platform.stream(enhanced_prompt):
        full_response += chunk
        yield chunk
    
    # Apply post-processing safeguards if needed
    if level >= ProtectionLevel.CRISIS:
        # Might need to prepend crisis resources
        crisis_text = get_crisis_resources()
        yield crisis_text
```

## Testing Your Integration

Create tests for your integration:

```python
import unittest
from integrations.core import ProtectionLevel

class TestMyIntegration(unittest.TestCase):
    def setUp(self):
        self.client = LFASMyPlatformClient(api_key="test")
    
    def test_standard_protection(self):
        response = self.client.generate("Hello")
        self.assertEqual(response.protection_level, 'STANDARD')
    
    def test_crisis_protection(self):
        response = self.client.generate(
            "I can't take it anymore. This is my last hope."
        )
        self.assertEqual(response.protection_level, 'CRISIS')
        self.assertIn('988', response.text)  # Crisis hotline
```

## Customization Options

### Custom Vulnerability Indicators

```python
from integrations.core import VulnerabilityDetector

class CustomDetector(VulnerabilityDetector):
    def __init__(self):
        super().__init__()
        # Add domain-specific indicators
        self.CRISIS_LANGUAGE.extend([
            "feeling hopeless about my startup",
            "business is failing"
        ])
```

### Custom Safeguards

```python
from integrations.core import SafeguardEngine

class CustomSafeguards(SafeguardEngine):
    def apply_safeguards(self, response, level, categories):
        # Apply base safeguards
        response = super().apply_safeguards(response, level, categories)
        
        # Add custom safeguards
        if 'financial_desperation' in categories:
            response = self.add_financial_resources(response)
        
        return response
    
    def add_financial_resources(self, response):
        return response + "\n\nFinancial counseling: 1-800-XXX-XXXX"
```

### Custom Protection Levels

```python
from integrations.core import ProtectionLevelManager

class CustomProtectionManager(ProtectionLevelManager):
    def determine_level(self, trigger_count):
        # More aggressive escalation
        if trigger_count >= 2:
            return ProtectionLevel.CRISIS
        elif trigger_count >= 1:
            return ProtectionLevel.ENHANCED
        else:
            return ProtectionLevel.STANDARD
```

## Best Practices

1. **Always use the core middleware** - Don't reimplement LFAS logic
2. **Preserve API compatibility** - Make your wrapper a drop-in replacement
3. **Include metadata** - Expose LFAS metadata to users
4. **Test with real scenarios** - Use examples from demonstrations/
5. **Document platform-specific features** - Explain how LFAS integrates
6. **Handle edge cases** - Streaming, errors, rate limits, etc.
7. **Keep it simple** - Wrapper should be thin, logic in core

## Example Integrations

Study these complete examples:

- `openai/` - Chat API integration
- `anthropic/` - Constitutional AI integration
- `google/` - Safety settings integration

## Support

Need help building your integration?

- 📧 Email: lfasprotocol@outlook.com
- 💬 Discussions: GitHub Discussions
- 🐛 Issues: GitHub Issues

## Contributing

If you build an integration for a popular platform, please consider contributing it back to the repository!

See CONTRIBUTING.md for guidelines.

---

**Ready to build? Start with the minimal integration above and expand as needed!**
