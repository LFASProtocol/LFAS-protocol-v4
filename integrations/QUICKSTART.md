# LFAS Protocol v4 - Quick Start Guide

Get started with LFAS integrations in 5 minutes!

## What is LFAS?

LFAS (Logical Framework for AI Safety) is a protocol that adds vulnerability detection and protection to AI systems. It automatically detects when users are vulnerable and applies appropriate safety measures.

## Installation

```bash
# Clone the repository
git clone https://github.com/LFASProtocol/LFAS-protocol-v4.git
cd LFAS-protocol-v4/integrations

# No dependencies needed for core middleware!
# For platform integrations, install as needed:
pip install openai          # For OpenAI
pip install anthropic       # For Anthropic
pip install google-generativeai  # For Google Gemini
```

## Your First LFAS-Protected App (60 seconds)

### Option 1: Using Core Middleware (No API Key Needed)

```python
from integrations.core import LFASMiddleware

# Initialize
lfas = LFASMiddleware()

# Your AI function (replace with real AI)
def my_ai(user_input):
    return "I'm here to help!"

# Process through LFAS
result = lfas.process_request(
    user_input="I lost my job and need money fast",
    ai_response_generator=my_ai
)

print(result['response'])
print(f"Protection: {result['metadata']['protection_level']}")
```

### Option 2: OpenAI with LFAS (API Key Required)

```python
from integrations.openai import LFASOpenAIClient

# Drop-in replacement for OpenAI client
client = LFASOpenAIClient(api_key="your-key")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "I can't take it anymore"}]
)

print(response.choices[0].message.content)
print(f"Protection: {response.protection_level}")
```

### Option 3: Anthropic with LFAS (API Key Required)

```python
from integrations.anthropic import LFASAnthropicClient

# Drop-in replacement for Anthropic client
client = LFASAnthropicClient(api_key="your-key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Nobody understands me"}]
)

print(response.content[0].text)
print(f"Protection: {response.protection_level}")
```

## How It Works

LFAS implements a 5-phase protocol:

```
User Input
    ↓
[1. LISTEN] ─────→ Detect vulnerability indicators
    ↓
[2. REFLECT] ────→ Determine protection level (1-3)
    ↓
[3. WAIT] ───────→ Safety pause if needed
    ↓
[4. ACT] ────────→ Apply safeguards to response
    ↓
[5. ACKNOWLEDGE] → Track for next interaction
    ↓
Safe Output
```

## Protection Levels

| Level | Triggers | Safeguards |
|-------|----------|------------|
| **Standard** | 0-1 | Basic reality checks, risk disclosure |
| **Enhanced** | 2 | + Financial disclaimers, simplified language |
| **Crisis** | 3+ | + Crisis resources, safety focus only |

## Vulnerability Categories

LFAS detects 4 types of vulnerability:

1. **Crisis Language**: "can't take it anymore", "last hope"
2. **Financial Desperation**: "lost my job", "need money fast"  
3. **Health Crisis**: "can't see a doctor", "no insurance"
4. **Isolation**: "nobody understands", "completely alone"

## Test It Out

Run the example:

```bash
cd integrations
python examples/simple_chatbot.py
```

Try these test inputs:
- "Hello, how are you?" → Standard protection
- "I lost my job and need money fast" → Enhanced protection
- "I can't take it anymore, this is my last hope" → Crisis protection

## Next Steps

1. ✅ Try the examples in `examples/`
2. ✅ Run tests: `python -m unittest discover tests/`
3. ✅ Read full docs: `README.md`
4. ✅ Check platform-specific guides:
   - `openai/README.md` (coming soon)
   - `anthropic/README.md` (coming soon)
   - `google/README.md` (coming soon)

## Common Use Cases

### Add to Existing OpenAI App

```python
# Before:
from openai import OpenAI
client = OpenAI(api_key="...")

# After (just change one line!):
from integrations.openai import LFASOpenAIClient
client = LFASOpenAIClient(api_key="...")

# Everything else stays the same!
```

### Wrap Any AI Response

```python
from integrations.core import LFASMiddleware

lfas = LFASMiddleware()

# You already have the AI response
ai_response = your_ai_platform.generate("user input")

# Just add LFAS protection
result = lfas.process_with_response(
    user_input="I lost my job",
    raw_ai_response=ai_response
)

safe_response = result['response']
```

### Custom Vulnerability Detection

```python
from integrations.core import VulnerabilityDetector

detector = VulnerabilityDetector()

# Add your own indicators
detector.FINANCIAL_DESPERATION.append("can't make rent")
detector.CRISIS_LANGUAGE.append("feeling hopeless")

# Use as normal
detected = detector.detect("I'm feeling hopeless")
```

## Support

- 📧 Email: lfasprotocol@outlook.com
- 🐛 Issues: [GitHub Issues](https://github.com/LFASProtocol/LFAS-protocol-v4/issues)
- 📖 Full Docs: See `README.md`

## License

LFAS Protocol v4 License
- Free for non-commercial use
- Commercial license required for business use
- Contact: lfasprotocol@outlook.com

---

**Ready to protect your users? Start with one of the examples above! 🚀**
