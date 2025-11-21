# LFAS Protocol v4 - Python Library Documentation

## Overview

The LFAS Protocol v4 Python library is a production-ready implementation of the **Logical Framework for AI Safety**. It provides vulnerability detection, protection level escalation, and crisis response safeguards for AI systems.

## Features

✅ **Vulnerability Detection** - Detects 4 categories of vulnerability indicators  
✅ **Protection Level Escalation** - Automatically escalates from Standard → Enhanced → Crisis  
✅ **VR-24 Crisis Safeguard** - Provides immediate crisis resources with empathetic responses  
✅ **Zero Dependencies** - Pure Python implementation  
✅ **Type Hints** - Full type annotations for better IDE support  
✅ **Comprehensive Tests** - 36 tests covering all functionality  
✅ **Multi-version Support** - Python 3.8 through 3.12  

## Installation

```bash
pip install lfas-protocol
```

For development:

```bash
git clone https://github.com/LFASProtocol/LFAS-protocol-v4
cd LFAS-protocol-v4
pip install -e ".[dev]"
```

## Quick Start

```python
from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard

# Initialize components
detector = VulnerabilityDetector()
safeguard = CrisisDetectionSafeguard()

# Detect vulnerability
result = detector.detect("I can't take it anymore, everything is hopeless")

# Check protection level
print(f"Protection Level: {result.protection_level.name}")  # CRISIS
print(f"Triggers: {result.trigger_count}")  # 2

# Generate safe response
if safeguard.should_activate(result):
    response = safeguard.generate_response(result)
    print(response.message)  # Includes 988 Lifeline, Crisis Text Line, etc.
```

## Core Components

### VulnerabilityDetector

Implements the **LISTEN** phase of LFAS Protocol by detecting vulnerability indicators.

**Detects 4 categories:**
- **Crisis Language** (VR-24): Suicidal ideation, hopelessness, unbearable distress
- **Financial Desperation**: Bankruptcy, financial ruin, severe money problems
- **Health Crisis**: Terminal illness, chronic pain, medical emergencies
- **Isolation**: Loneliness, abandonment, social disconnection

```python
from lfas_protocol import VulnerabilityDetector, VulnerabilityCategory

detector = VulnerabilityDetector()

# Basic detection
result = detector.detect("I'm feeling hopeless and broke")
print(f"Indicators found: {len(result.indicators)}")
for indicator in result.indicators:
    print(f"  - {indicator.category.value}")

# Add custom patterns
detector.add_pattern(
    VulnerabilityCategory.CRISIS_LANGUAGE,
    r'\b(custom pattern)\b'
)

# Get current patterns
patterns = detector.get_patterns()
```

### Protection Levels

The system automatically escalates protection based on trigger count:

| Triggers | Protection Level | Description |
|----------|-----------------|-------------|
| 0-1 | **STANDARD** | Basic honesty safeguards |
| 2 | **ENHANCED** | Vulnerability detected, increased caution |
| 3+ | **CRISIS** | Immediate danger, crisis resources provided |

```python
from lfas_protocol import ProtectionLevel

# Protection levels are automatically assigned
result = detector.detect(user_input)

if result.protection_level == ProtectionLevel.CRISIS:
    # Provide immediate crisis resources
    pass
elif result.protection_level == ProtectionLevel.ENHANCED:
    # Increase caution, be more supportive
    pass
else:
    # Standard AI response
    pass
```

### CrisisDetectionSafeguard

Implements the **ACT** phase of LFAS Protocol by providing appropriate responses.

**VR-24 Crisis Resources:**
- 988 Suicide & Crisis Lifeline (Call or text 988)
- Crisis Text Line (Text HOME to 741741)
- International Association for Suicide Prevention

```python
from lfas_protocol import CrisisDetectionSafeguard

safeguard = CrisisDetectionSafeguard()

# Check if safeguard should activate (CRISIS level only)
if safeguard.should_activate(result):
    response = safeguard.generate_response(result)
    
    print(response.message)  # Empathetic message with resources
    print(response.resources)  # List of crisis resources
    print(response.protection_level)  # CRISIS

# Get crisis resources anytime
resources = safeguard.get_crisis_resources()
for resource in resources:
    print(f"{resource['name']}: {resource['contact']}")
```

## Integration Examples

### Basic Integration

```python
from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard

def safe_ai_response(user_input: str) -> str:
    """Process user input through LFAS protection."""
    detector = VulnerabilityDetector()
    safeguard = CrisisDetectionSafeguard()
    
    # LISTEN - Detect vulnerability
    result = detector.detect(user_input)
    
    # REFLECT - Assess protection level
    # ACT - Apply safeguards
    if safeguard.should_activate(result):
        # Crisis: Provide resources, don't generate AI response
        response = safeguard.generate_response(result)
        return response.message
    
    # Standard/Enhanced: Proceed with AI response
    return generate_ai_response(user_input)
```

### OpenAI Integration

```python
from openai import OpenAI
from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard, ProtectionLevel

client = OpenAI()

def chat_with_protection(user_message: str) -> str:
    detector = VulnerabilityDetector()
    safeguard = CrisisDetectionSafeguard()
    
    # Detect vulnerability
    result = detector.detect(user_message)
    
    # Crisis level: Provide resources immediately
    if result.protection_level == ProtectionLevel.CRISIS:
        response = safeguard.generate_response(result)
        return response.message
    
    # Enhanced level: Modify system prompt
    if result.protection_level == ProtectionLevel.ENHANCED:
        system_msg = (
            "You are a helpful, empathetic AI assistant. "
            "The user may be going through a difficult time. "
            "Be supportive and avoid false optimism."
        )
        safeguard_response = safeguard.generate_response(result)
    else:
        system_msg = "You are a helpful AI assistant."
        safeguard_response = None
    
    # Generate AI response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_message}
        ]
    )
    
    ai_message = response.choices[0].message.content
    
    # Prepend safeguard message for enhanced level
    if safeguard_response and safeguard_response.should_activate:
        return f"{safeguard_response.message}\n\n{ai_message}"
    
    return ai_message
```

### Anthropic Claude Integration

```python
import anthropic
from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard, ProtectionLevel

client = anthropic.Anthropic()

def chat_with_protection(user_message: str) -> str:
    detector = VulnerabilityDetector()
    safeguard = CrisisDetectionSafeguard()
    
    result = detector.detect(user_message)
    
    if result.protection_level == ProtectionLevel.CRISIS:
        response = safeguard.generate_response(result)
        return response.message
    
    # Adjust system prompt based on protection level
    if result.protection_level == ProtectionLevel.ENHANCED:
        system = "Be empathetic and supportive. The user may be struggling."
    else:
        system = "You are a helpful AI assistant."
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user_message}]
    )
    
    return response.content[0].text
```

## Data Models

### DetectionResult

```python
@dataclass
class DetectionResult:
    text: str                                    # Original input text
    indicators: List[VulnerabilityIndicator]     # Detected indicators
    protection_level: ProtectionLevel            # Auto-calculated level
    trigger_count: int                           # Number of indicators
    metadata: Dict[str, Any]                     # Additional metadata
```

### SafeguardResponse

```python
@dataclass
class SafeguardResponse:
    should_activate: bool                        # Whether safeguard activated
    message: str                                 # Response message
    resources: List[Dict[str, str]]             # Crisis resources
    protection_level: ProtectionLevel            # Protection level
    metadata: Dict[str, Any]                     # Additional metadata
```

## Testing

The library includes 36 comprehensive tests:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_detector.py -v

# Run with coverage
pytest tests/ --cov=lfas_protocol --cov-report=html
```

## Development

### Code Quality Tools

```bash
# Format code
black lfas_protocol/ tests/

# Lint code
ruff check lfas_protocol/ tests/

# Type check
mypy lfas_protocol/

# Run all quality checks
black lfas_protocol/ tests/ && \
ruff check lfas_protocol/ tests/ && \
mypy lfas_protocol/ && \
pytest tests/ -v
```

### Building the Package

```bash
# Build distribution
python -m build

# Install locally
pip install -e ".[dev]"
```

## Examples

See the `examples/` directory for complete working examples:
- `basic_usage.py` - Basic vulnerability detection and safeguards
- `openai_integration.py` - Integration with OpenAI API

Run examples:

```bash
python examples/basic_usage.py
python examples/openai_integration.py
```

## Best Practices

### 1. Always Check Crisis Level First

```python
result = detector.detect(user_input)
if result.protection_level == ProtectionLevel.CRISIS:
    # Provide resources immediately, don't generate AI response
    return safeguard.generate_response(result).message
```

### 2. Adjust AI Behavior for Enhanced Level

```python
if result.protection_level == ProtectionLevel.ENHANCED:
    # Use more empathetic system prompts
    # Avoid false optimism
    # Provide supportive resources
```

### 3. Log Protection Events

```python
result = detector.detect(user_input)
if result.trigger_count > 0:
    logger.info(f"Vulnerability detected: {result.protection_level.name}")
    logger.info(f"Indicators: {[str(i) for i in result.indicators]}")
```

### 4. Don't Suppress Crisis Resources

```python
# ❌ DON'T: Suppress crisis messages
if result.protection_level == ProtectionLevel.CRISIS:
    return "I can help you with that."  # WRONG

# ✅ DO: Provide crisis resources
if result.protection_level == ProtectionLevel.CRISIS:
    response = safeguard.generate_response(result)
    return response.message  # Includes 988, Crisis Text Line, etc.
```

## License

LFAS Protocol v4 License - See [LICENSE](LICENSE) for details.

**Non-Commercial Use:** Free for personal, academic, research, and non-profit use.  
**Commercial Use:** Requires separate commercial license.

Contact: lfasprotocol@outlook.com

## Support

- **Documentation**: [GitHub Repository](https://github.com/LFASProtocol/LFAS-protocol-v4)
- **Issues**: [GitHub Issues](https://github.com/LFASProtocol/LFAS-protocol-v4/issues)
- **Email**: lfasprotocol@outlook.com

## Citation

If you use LFAS Protocol in your research or project, please cite:

```
Mehmet (2025). LFAS Protocol v4: Logical Framework for AI Safety.
GitHub: https://github.com/LFASProtocol/LFAS-protocol-v4
```
