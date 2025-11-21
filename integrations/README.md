# LFAS Protocol v4 - Integration Templates

This directory contains **drop-in middleware** and **turnkey solutions** for integrating the LFAS Protocol v4 with major AI providers.

## 🎯 Quick Start

### OpenAI Integration (Python)

```python
from integrations.python.openai import create_lfas_client

# Create LFAS-protected OpenAI client
lfas = create_lfas_client(api_key="your-openai-key")

# Use it like normal OpenAI, but with LFAS protection
response = lfas.chat_completion(
    messages=[{"role": "user", "content": "I need help"}]
)

print(response['content'])  # LFAS-protected response
print(response['metadata'])  # Protection level, triggers, safeguards
```

### Anthropic Integration (Python)

```python
from integrations.python.anthropic import create_lfas_client

# Create LFAS-protected Anthropic client
lfas = create_lfas_client(api_key="your-anthropic-key")

# Use it like normal Anthropic, but with LFAS protection
response = lfas.create_message(
    messages=[{"role": "user", "content": "I need help"}]
)

print(response['content'])  # LFAS-protected response
print(response['metadata'])  # Protection level, triggers, safeguards
```

## 📁 Directory Structure

```
integrations/
├── python/
│   ├── shared/
│   │   ├── lfas_engine.py          # Core LFAS Protocol engine
│   │   └── __init__.py
│   ├── openai/
│   │   ├── lfas_openai.py          # OpenAI integration
│   │   ├── example_usage.py        # Usage examples
│   │   ├── requirements.txt        # Dependencies
│   │   └── __init__.py
│   └── anthropic/
│       ├── lfas_anthropic.py       # Anthropic integration
│       ├── example_usage.py        # Usage examples
│       ├── requirements.txt        # Dependencies
│       └── __init__.py
└── javascript/                      # (Coming soon)
    ├── openai/
    └── anthropic/
```

## 🚀 Installation

### OpenAI Integration

```bash
cd integrations/python/openai
pip install -r requirements.txt
```

### Anthropic Integration

```bash
cd integrations/python/anthropic
pip install -r requirements.txt
```

## 📖 How It Works

The LFAS Protocol implements a **5-stage safety framework**:

### 1. LISTEN 👂
Analyzes user input for vulnerability indicators:
- Crisis language (suicide, self-harm)
- Financial desperation
- Health crises
- Isolation indicators

### 2. REFLECT 🧠
Determines protection level based on detected triggers:
- **Level 1 (Standard)**: 0-1 triggers
- **Level 2 (Enhanced)**: 2 triggers
- **Level 3 (Crisis)**: 3+ triggers

### 3. WAIT ⏸️
Safety pause before generating response (conceptual stage for confirmation)

### 4. ACT 🛡️
Applies appropriate safeguards:
- **VR-20**: Unfounded Optimism Prevention
- **VR-22**: Realistic Capability Assessment
- **VR-23**: Financial Realism Verification
- **VR-24**: Crisis Detection & Response
- **VR-25**: Vulnerable User Amplification Prevention

### 5. ACKNOWLEDGE ✅
Logs intervention and provides metadata feedback

## 💡 Usage Examples

### Example 1: Standard Conversation (No Triggers)

```python
from integrations.python.openai import create_lfas_client

lfas = create_lfas_client(api_key="your-key")
response = lfas.chat_completion(
    messages=[{"role": "user", "content": "How do I learn Python?"}]
)

# Protection Level: STANDARD
# Safeguards: VR-20, VR-22
```

### Example 2: Financial Vulnerability Detected

```python
response = lfas.chat_completion(
    messages=[{
        "role": "user", 
        "content": "I lost my job and need money fast"
    }]
)

# Protection Level: ENHANCED
# Safeguards: VR-20, VR-22, VR-23 (Financial Realism)
# Response includes financial reality disclaimers
```

### Example 3: Crisis Situation

```python
response = lfas.chat_completion(
    messages=[{
        "role": "user",
        "content": "I can't take it anymore. Nobody understands."
    }]
)

# Protection Level: CRISIS
# Safeguards: All (VR-20, VR-22, VR-23, VR-24, VR-25)
# Response includes crisis resources and encourages human connection
```

## 🔧 Advanced Usage

### Accessing Metadata

```python
response = lfas.chat_completion(messages)

metadata = response['metadata']
print(f"Protection Level: {metadata['protection_level']}")
print(f"Triggers Detected: {metadata['triggers_detected']}")
print(f"Trigger Details: {metadata['trigger_details']}")
print(f"Safeguards Applied: {metadata['safeguards_applied']}")
```

### Conversation History

```python
# Get conversation history with LFAS metadata
history = lfas.get_conversation_history()

for exchange in history:
    print(f"User: {exchange['user']}")
    print(f"Protection Level: {exchange['level'].name}")
    print(f"Triggers: {exchange['triggers']}")
```

### Resetting Conversation State

```python
# Reset protection level and conversation history
lfas.reset_conversation()
```

## 🎨 Customization

The LFAS engine can be customized by modifying:

1. **Vulnerability Indicators** (`lfas_engine.py`):
   - Add domain-specific trigger phrases
   - Adjust sensitivity levels

2. **Protection Levels** (`lfas_engine.py`):
   - Customize escalation thresholds
   - Modify de-escalation logic

3. **Safeguards** (`lfas_engine.py`):
   - Add custom verification requirements
   - Adjust disclaimer text

## 🧪 Testing

Run the example files to test the integrations:

```bash
# Set your API key
export OPENAI_API_KEY="your-key"
# or
export ANTHROPIC_API_KEY="your-key"

# Run examples
python integrations/python/openai/example_usage.py
python integrations/python/anthropic/example_usage.py
```

## 🌟 Features

- ✅ **Drop-in replacement**: Minimal code changes required
- ✅ **Automatic protection**: No manual safeguard implementation needed
- ✅ **Transparent metadata**: Full visibility into LFAS decisions
- ✅ **Conversation tracking**: Maintains state across exchanges
- ✅ **Crisis detection**: Automatic crisis resource provision
- ✅ **Multi-level protection**: Escalates based on vulnerability

## 📋 Requirements

- Python 3.7+
- OpenAI Python SDK (for OpenAI integration)
- Anthropic Python SDK (for Anthropic integration)

## 🔐 Security & Privacy

- LFAS processing happens **locally** in your application
- No data is sent to third parties beyond the AI provider
- Vulnerability detection runs **before** sending to AI
- Safeguards are applied **after** receiving AI response

## 📚 Additional Resources

- [LFAS v4 Specification](/protocol/lfas-v4-specification.xml)
- [Implementation Guide](/implementation-guide.md)
- [Protocol README](/README.md)

## ⚠️ Important Notes

1. **Not a Medical Device**: LFAS is a safety framework, not a substitute for professional help
2. **No Guarantees**: LFAS improves safety but cannot prevent all harm
3. **Integrator Responsibility**: You remain responsible for your AI system's behavior
4. **Continuous Improvement**: Update trigger lists and safeguards based on your domain

## 🤝 Contributing

To add integrations for other providers:

1. Create a new directory under `python/` or `javascript/`
2. Implement the 5-stage LFAS protocol
3. Reuse the `lfas_engine.py` core logic
4. Add example usage and tests
5. Submit a pull request

## 📝 License

These integration templates are part of the LFAS Protocol v4 project and are licensed under the LFAS Protocol v4 License. See [LICENSE](/LICENSE) for details.

---

**Questions?** Contact: lfasprotocol@outlook.com
