# LFAS Protocol Python Reference Implementation

A Python reference implementation of the **LFAS Protocol v4** (Logical Framework for AI Safety), providing tools for detecting user vulnerability and applying appropriate safety safeguards in AI interactions.

## 🎯 Overview

The LFAS Protocol is designed to protect vulnerable users in AI interactions by:
- **Detecting** vulnerability indicators in user input (LISTEN phase)
- **Determining** appropriate protection levels (Level 1, 2, or 3)
- **Applying** safety safeguards based on detected vulnerability

This library provides a minimal viable implementation focused on the vulnerability detection component (Week 1 of the implementation plan).

## 🚀 Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/LFASProtocol/LFAS-protocol-v4.git
cd LFAS-protocol-v4

# Install the package
pip install -e .

# For development (includes testing tools)
pip install -e ".[dev]"
```

### Future PyPI Installation (Coming Soon)

```bash
pip install lfas-protocol
```

## 📖 Quick Start

### Basic Usage

```python
from lfas import VulnerabilityDetector, ProtectionLevel

# Initialize the detector
detector = VulnerabilityDetector()

# Analyze user input
user_input = "I lost my job and can't pay my bills. This is my last hope."
result = detector.detect(user_input)

# Check the protection level
print(f"Protection Level: {result.protection_level.name}")
print(f"Triggers Found: {result.trigger_count}")
print(f"Categories: {result.triggered_categories}")

# Output:
# Protection Level: CRISIS
# Triggers Found: 3
# Categories: {'financial_desperation', 'crisis_language'}
```

### With Conversation History

```python
from lfas import VulnerabilityDetector

detector = VulnerabilityDetector()

# Track conversation history for context
conversation_history = [
    "I've been feeling down lately.",
    "I lost my job last week."
]

# Analyze current input with history
current_input = "I don't know what to do anymore."
result = detector.detect(current_input, conversation_history=conversation_history)

if result.protection_level.value >= 2:
    print("⚠️ Enhanced protection required")
    print(f"Detected indicators: {result.triggered_indicators}")
```

### Protection Level-Based Response

```python
from lfas import VulnerabilityDetector, ProtectionLevel

detector = VulnerabilityDetector()

user_input = "I'm thinking about ending it all."
result = detector.detect(user_input)

if result.protection_level == ProtectionLevel.CRISIS:
    print("🚨 CRISIS DETECTED")
    print("Immediate safety resources should be provided:")
    print("- National Suicide Prevention Lifeline: 988")
    print("- Crisis Text Line: Text HOME to 741741")
    
elif result.protection_level == ProtectionLevel.ENHANCED:
    print("⚠️ ENHANCED PROTECTION")
    print("Apply additional safeguards and reality checking")
    
else:
    print("✅ STANDARD PROTECTION")
    print("Apply basic honesty safeguards")
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/lfas --cov-report=term-missing

# Run specific test file
pytest tests/test_detector.py -v
```

## 🔧 Development

### Code Quality Tools

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

### Running All Checks

```bash
# Format, lint, type check, and test
black src/ tests/ && \
ruff check src/ tests/ && \
mypy src/ && \
pytest
```

## 📊 Features

### Current Implementation (Week 1)

- ✅ **Vulnerability Detection Engine**
  - Crisis language detection
  - Financial desperation indicators
  - Health crisis signals
  - Isolation indicators
  
- ✅ **Protection Level Escalation**
  - Level 1: Standard (0-1 triggers)
  - Level 2: Enhanced (2 triggers)
  - Level 3: Crisis (3+ triggers)
  
- ✅ **XML Specification Parser**
  - Loads indicators from LFAS v4 specification
  - Spec-driven detection (not hardcoded)
  
- ✅ **Comprehensive Testing**
  - 26 test cases
  - 95%+ code coverage
  - Type-checked with mypy

### Planned Features (Future Weeks)

- ⏳ **Week 2**: VR-24 Crisis Detection & Response
- ⏳ **Week 3**: OpenAI API Wrapper Integration
- ⏳ **Week 4**: Additional Safeguards (VR-20, VR-22, VR-23, VR-25)

## 🔍 How It Works

The detector implements the **LISTEN** phase of the LFAS Protocol:

1. **Load Specification**: Parses the XML specification to extract vulnerability indicators
2. **Scan Input**: Analyzes user input (and optional conversation history) for indicator phrases
3. **Count Triggers**: Tracks number and categories of detected indicators
4. **Determine Level**: Assigns protection level based on trigger count:
   - 0-1 triggers → Standard Protection
   - 2 triggers → Enhanced Protection
   - 3+ triggers → Crisis Protection

## 📚 Documentation

- **Full Protocol Specification**: `/protocol/lfas-v4-specification.xml`
- **Implementation Guide**: `/implementation-guide.md`
- **Research & Evidence**: `/research/` directory
- **White Paper**: `/documentation/white-paper-outline.md`

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Key areas for contribution:
- Additional vulnerability indicators
- Improved detection algorithms
- Integration examples
- Documentation improvements
- Bug fixes and testing

## 📄 License

This work is licensed under the **LFAS Protocol v4 License**:
- **Non-Commercial Use**: Free for personal, academic, research, and non-profit use
- **Commercial Use**: Requires separate commercial license

See [LICENSE](LICENSE) for full details.

## ⚠️ Safety Disclaimer

**Important**: The LFAS Protocol is a safety framework, not a guarantee of harm prevention.

- This is **not** a medical device or emergency response system
- It does **not** replace professional mental health care
- Implementers retain full responsibility for their AI systems
- No warranty is provided for prevention of crisis events

For mental health emergencies:
- **US**: National Suicide Prevention Lifeline: **988**
- **US**: Crisis Text Line: Text **HOME** to **741741**
- **International**: [Find resources at findahelpline.com](https://findahelpline.com)

## 📧 Contact

- **Email**: lfasprotocol@outlook.com
- **Repository**: https://github.com/LFASProtocol/LFAS-protocol-v4
- **Issues**: https://github.com/LFASProtocol/LFAS-protocol-v4/issues

## 🙏 Acknowledgments

The LFAS Protocol was created to address real documented failures in AI safety systems. We thank the AI safety research community for their validation and feedback.

---

*"When the lighthouse becomes the rocks, we need better navigation systems."* - Mehmet
