# LFAS Protocol Python Reference Library

A Python implementation of the LFAS Protocol v4 (Logical Framework for AI Safety) - protecting vulnerable users in AI systems through intelligent vulnerability detection and crisis response.

## Features

- 🔍 **Vulnerability Detection**: Automatically detects crisis language, financial desperation, health crises, and isolation indicators
- 📊 **Protection Level Escalation**: Dynamically adjusts safety measures from Standard → Enhanced → Crisis levels
- 🆘 **Crisis Response (VR-24)**: Activates immediate crisis support resources when needed
- 🧪 **Well-Tested**: Comprehensive test suite with 24+ test cases
- 📦 **Zero Dependencies**: Pure Python implementation with no external runtime dependencies
- 🚀 **Easy Integration**: Simple API for adding safety layers to any AI system

## Installation

### From Source (Current)

```bash
git clone https://github.com/LFASProtocol/LFAS-protocol-v4.git
cd LFAS-protocol-v4
pip install -e .
```

### From PyPI (Coming Soon)

```bash
pip install lfas-protocol
```

## Quick Start

```python
from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard

# Initialize components
detector = VulnerabilityDetector()
safeguard = CrisisDetectionSafeguard()

# Analyze user input
user_input = "I can't take it anymore, everything is hopeless"
result = detector.detect(user_input)

print(f"Protection Level: {result.protection_level.name}")
# Output: Protection Level: CRISIS

# Generate appropriate response
if safeguard.should_activate(result):
    response = safeguard.generate_response(result)
    print(response)
    # Provides crisis resources and supportive messaging
```

## How It Works

The LFAS Protocol implements a five-phase safety loop:

1. **LISTEN**: Detect vulnerability indicators in user input
2. **REFLECT**: Assess protection level based on detected signals
3. **WAIT**: Pause for safety verification (implemented in your application)
4. **ACT**: Apply appropriate safeguards
5. **ACKNOWLEDGE**: Confirm safety measures and log intervention

### Protection Levels

- **Level 1 (Standard)**: 0 vulnerability indicators detected
- **Level 2 (Enhanced)**: 1-2 indicators detected - requires enhanced safeguards
- **Level 3 (Crisis)**: 3+ indicators detected - activates crisis protocols

### Vulnerability Categories

The detector identifies four types of vulnerability indicators:

1. **Crisis Language**: Suicidal ideation, self-harm, hopelessness
2. **Financial Desperation**: Job loss, eviction, urgent money needs
3. **Health Crisis**: No insurance, can't afford medication, untreated pain
4. **Isolation**: No support network, family doesn't understand

## Examples

### Example 1: Financial Crisis Detection

```python
detector = VulnerabilityDetector()
result = detector.detect("I lost my job and have $100 left. I need to make money fast.")

print(f"Protection Level: {result.protection_level.name}")
# Output: Protection Level: ENHANCED

print(f"Categories: {', '.join(result.categories)}")
# Output: Categories: financial_desperation
```

### Example 2: Mental Health Crisis Response

```python
from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard

detector = VulnerabilityDetector()
safeguard = CrisisDetectionSafeguard()

crisis_input = "I can't take it anymore, everything is hopeless"
result = detector.detect(crisis_input)

if safeguard.should_activate(result):
    response = safeguard.generate_response(result)
    # Response includes:
    # - Empathetic acknowledgment
    # - 988 Suicide & Crisis Lifeline
    # - Crisis Text Line (741741)
    # - Encouragement to seek help
```

### Example 3: Viewing All Indicators

```python
detector = VulnerabilityDetector()
categories = detector.get_indicator_categories()

for category, indicators in categories.items():
    print(f"{category}: {len(indicators)} indicators")
```

Run the complete examples:

```bash
python examples/basic_usage.py
```

## Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=lfas_protocol --cov-report=html
```

All 24 tests should pass, covering:
- Vulnerability detection across all categories
- Protection level escalation
- Crisis safeguard activation
- Response generation
- Scenarios from the protocol demonstration

## Integration Guide

### Basic Integration Pattern

```python
from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard

class SafeAIWrapper:
    def __init__(self, ai_model):
        self.ai_model = ai_model
        self.detector = VulnerabilityDetector()
        self.crisis_safeguard = CrisisDetectionSafeguard()
    
    def generate_response(self, user_input):
        # LISTEN: Detect vulnerabilities
        detection = self.detector.detect(user_input)
        
        # REFLECT & WAIT: Check protection level
        if detection.protection_level >= ProtectionLevel.ENHANCED:
            # ACT: Apply safeguards
            if self.crisis_safeguard.should_activate(detection):
                return self.crisis_safeguard.generate_response(detection)
        
        # Standard AI response for non-crisis situations
        return self.ai_model.generate(user_input)
```

### OpenAI Wrapper Example

```python
from openai import OpenAI
from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard, ProtectionLevel

client = OpenAI()
detector = VulnerabilityDetector()
safeguard = CrisisDetectionSafeguard()

def safe_chat_completion(user_message):
    # Detect vulnerability
    result = detector.detect(user_message)
    
    # Handle crisis situations
    if safeguard.should_activate(result):
        return safeguard.generate_response(result)
    
    # Add protection level to system prompt
    system_prompt = "You are a helpful assistant."
    if result.protection_level == ProtectionLevel.ENHANCED:
        system_prompt += " Be especially careful with financial advice and provide realistic assessments."
    
    # Generate response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    
    return response.choices[0].message.content
```

## Current Implementation Status

### ✅ Completed (Week 1)

- [x] Vulnerability detection engine (LISTEN phase)
- [x] Protection level escalation (REFLECT phase)
- [x] VR-24: Crisis Detection & Response safeguard
- [x] Comprehensive test suite
- [x] Package configuration and structure
- [x] Examples and documentation

### 🚧 Planned (Future Releases)

- [ ] VR-20: Unfounded Optimism Prevention
- [ ] VR-22: Realistic Capability Assessment  
- [ ] VR-23: Financial Realism Verification
- [ ] VR-25: Vulnerable User Amplification Prevention
- [ ] Conversation history tracking
- [ ] Multi-language support
- [ ] Custom indicator configuration
- [ ] Integration helpers for popular AI platforms

## Contributing

We welcome contributions! The LFAS Protocol's mission to protect vulnerable users requires collective expertise.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Important**: All contributions are subject to the LFAS Protocol v4 License.

## License

**LFAS Protocol v4 License**  
Copyright (c) 2025 Mehmet (LFASProtocol). All Rights Reserved.

- **Non-Commercial Use**: Free for personal, academic, research, and non-profit use
- **Commercial Use**: Requires separate commercial license
- **No Warranty**: This is a safety framework, not a guarantee of harm prevention

See [LICENSE](LICENSE) for full license text.  
Commercial inquiries: lfasprotocol@outlook.com

## Safety Disclaimer

⚠️ **IMPORTANT**

1. **Not a Medical Device**: The LFAS Protocol is an algorithmic framework, not a substitute for professional mental health care or emergency services.

2. **No Guarantee**: While designed to mitigate risk, the Protocol cannot and does not guarantee prevention of all harm.

3. **Integrator Responsibility**: Organizations implementing LFAS retain full legal and ethical responsibility for their AI systems.

**In crisis situations, always encourage users to contact:**
- 988 Suicide & Crisis Lifeline (US)
- Emergency services (911 in US)
- Local crisis support resources

## Research & Validation

The LFAS Protocol is based on documented real-world cases and validated by independent AI research teams. See the [research](research/) directory for:

- Complete research compilation
- Independent validation studies
- Reality gap analysis
- Evidence of current AI system failures

## Citation

If you use this library in your research or product, please cite:

```bibtex
@software{lfas_protocol_2025,
  author = {Mehmet},
  title = {LFAS Protocol v4: Logical Framework for AI Safety},
  year = {2025},
  url = {https://github.com/LFASProtocol/LFAS-protocol-v4}
}
```

## Resources

- **Repository**: https://github.com/LFASProtocol/LFAS-protocol-v4
- **Documentation**: [implementation-guide.md](implementation-guide.md)
- **Protocol Specification**: [protocol/lfas-v4-specification.xml](protocol/lfas-v4-specification.xml)
- **Demonstrations**: [demonstrations/lfas-basic-demo.md](demonstrations/lfas-basic-demo.md)
- **Email**: lfasprotocol@outlook.com

---

*"When the lighthouse becomes the rocks, we need better navigation systems." - Mehmet*
