# LFAS Protocol v4 - Integration Templates

Welcome to the LFAS Protocol v4 integration templates! This directory contains drop-in middleware and turnkey solutions for integrating LFAS protection into popular AI platforms.

## Overview

The LFAS (Logical Framework for AI Safety) Protocol v4 provides a five-phase safety framework:
- **LISTEN**: Detect vulnerability indicators in user input
- **REFLECT**: Determine appropriate protection level
- **WAIT**: Implement safety pause for verification
- **ACT**: Apply safeguards to AI responses
- **ACKNOWLEDGE**: Track and prepare for next interaction

## Available Integrations

### ✅ OpenAI (ChatGPT)
Drop-in replacement for OpenAI client with LFAS protection.

### ✅ Anthropic (Claude)
Drop-in replacement for Anthropic client with LFAS protection.

### ✅ Google (Gemini)
Wrapper for Google Gemini with LFAS protection.

### ✅ Core Middleware
Platform-agnostic LFAS implementation for any AI system.

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/LFASProtocol/LFAS-protocol-v4.git
cd LFAS-protocol-v4/integrations

# No external dependencies required for core middleware
# For specific platforms, install their SDKs:
pip install openai          # For OpenAI integration
pip install anthropic       # For Anthropic integration
pip install google-generativeai  # For Google Gemini integration
```

### OpenAI Integration

```python
from integrations.openai import LFASOpenAIClient

# Drop-in replacement for OpenAI client
client = LFASOpenAIClient(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "I lost my job and need money fast"}
    ]
)

# Access the response
print(response.choices[0].message.content)

# Check LFAS metadata
print(f"Protection Level: {response.protection_level}")
print(f"Detected Vulnerabilities: {response.detected_vulnerabilities}")
print(f"Active Safeguards: {response.active_safeguards}")
```

### Anthropic Integration

```python
from integrations.anthropic import LFASAnthropicClient

# Drop-in replacement for Anthropic client
client = LFASAnthropicClient(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "I can't take it anymore, nothing matters"}
    ]
)

# Access the response
print(response.content[0].text)

# Check LFAS metadata
print(f"Protection Level: {response.protection_level}")
```

### Google Gemini Integration

```python
from integrations.google import LFASGeminiClient

# Create LFAS-protected Gemini client
client = LFASGeminiClient(
    model_name="gemini-pro",
    api_key="your-api-key"
)

response = client.generate_content(
    "I'm completely alone and nobody understands"
)

# Access the response
print(response.text)

# Check LFAS metadata
print(f"Protection Level: {response.protection_level}")
```

### Using Core Middleware (Platform-Agnostic)

```python
from integrations.core import LFASMiddleware

# Initialize middleware
lfas = LFASMiddleware()

# Define your AI response generator
def my_ai_generator(user_input):
    # Call your AI platform here
    return "Your AI's response"

# Process request through LFAS
result = lfas.process_request(
    user_input="I need help with something",
    ai_response_generator=my_ai_generator
)

print(result['response'])
print(result['metadata'])
```

## Protection Levels

LFAS automatically escalates protection based on detected vulnerability:

- **Level 1 (Standard)**: 0-1 vulnerability indicators
  - Basic safeguards: realistic assessments, risk disclosure
  
- **Level 2 (Enhanced)**: 2 vulnerability indicators
  - Additional safeguards: financial disclaimers, simplified language, crisis resources
  
- **Level 3 (Crisis)**: 3+ vulnerability indicators
  - Maximum protection: crisis intervention, safety resources, human connection encouragement

## Detected Vulnerabilities

LFAS detects four categories of vulnerability:

1. **Crisis Language**: Suicidal ideation, extreme hopelessness
2. **Financial Desperation**: Job loss, eviction, urgent money needs
3. **Health Crisis**: Untreated medical conditions, no healthcare access
4. **Isolation Indicators**: Complete loneliness, AI dependency signals

## Examples

See the `/examples` directory for complete working examples:
- `simple_chatbot.py`: Basic chatbot with LFAS protection
- `multi_platform_demo.py`: Demonstration across all platforms
- `custom_integration.py`: Building your own integration

## Testing

Run the test suite:

```bash
cd integrations
python -m pytest tests/ -v
```

## Architecture

```
integrations/
├── core/              # Platform-agnostic LFAS implementation
│   ├── detector.py    # Vulnerability detection (LISTEN phase)
│   ├── protection.py  # Protection level management (REFLECT phase)
│   ├── safeguards.py  # Safeguard application (ACT phase)
│   └── middleware.py  # Main orchestration
├── openai/            # OpenAI integration
├── anthropic/         # Anthropic integration
├── google/            # Google Gemini integration
├── examples/          # Working examples
└── tests/             # Test suite
```

## Advanced Usage

### Custom Vulnerability Indicators

```python
from integrations.core import VulnerabilityDetector

detector = VulnerabilityDetector()

# Add custom indicators
detector.FINANCIAL_DESPERATION.append("can't make rent")
detector.CRISIS_LANGUAGE.append("custom crisis phrase")
```

### Customizing Safeguards

```python
from integrations.core import SafeguardEngine

engine = SafeguardEngine()

# Customize crisis resources
engine.CRISIS_RESOURCES = """
Custom crisis resources here...
"""
```

### Middleware Without AI Integration

```python
from integrations.core import LFASMiddleware

lfas = LFASMiddleware()

# Just apply safeguards to existing response
result = lfas.process_with_response(
    user_input="User's message",
    raw_ai_response="AI's existing response"
)
```

## Contributing

We welcome contributions! Areas for improvement:
- Additional platform integrations (Azure OpenAI, Cohere, etc.)
- Enhanced vulnerability detection
- Additional safeguard types
- Improved documentation

## License

This integration code is part of the LFAS Protocol v4 and is licensed under the LFAS Protocol v4 License. See the main repository LICENSE file for details.

## Support

- **Email**: lfasprotocol@outlook.com
- **Issues**: GitHub Issues in main repository
- **Discussions**: GitHub Discussions

## Safety Disclaimer

The LFAS Protocol is a safety framework designed to reduce risk, but it **cannot guarantee** the prevention of all harmful outcomes. Organizations implementing LFAS retain full legal and ethical responsibility for their AI systems. This is not a medical device or emergency response system.

---

*"When the lighthouse becomes the rocks, we need better navigation systems." - Mehmet*
