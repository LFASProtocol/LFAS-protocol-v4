# LFAS Protocol v4 - Python Implementation Guide

## Overview

The LFAS Protocol v4 Python implementation provides an AI-powered vulnerability and crisis detection system that:

- Dynamically parses XML specifications to extract behavioral indicators
- Escalates protection levels based on detected vulnerability signals
- Triggers crisis detection when thresholds are breached
- Provides real-world support resources (988, Crisis Text Line, etc.)
- Maintains conversation history for ongoing detection

## Installation

```bash
pip install git+https://github.com/LFASProtocol/LFAS-protocol-v4.git
```

Or for development:

```bash
git clone https://github.com/LFASProtocol/LFAS-protocol-v4.git
cd LFAS-protocol-v4
pip install -e .
```

## Quick Start

```python
from lfas import VulnerabilityDetector, CrisisDetector

# Initialize detector
detector = VulnerabilityDetector()

# Detect vulnerability
result = detector.detect("I lost my job, this is my last hope, can't take it anymore")

print(f"Protection Level: {result.protection_level.name}")
print(f"Triggers Detected: {result.triggers_count}")
print(f"Categories: {result.detected_categories}")

# Activate crisis support if needed
if result.protection_level.value >= 3:
    crisis_detector = CrisisDetector()
    crisis_result = crisis_detector.assess_crisis(result)
    
    print(f"\nCrisis Type: {crisis_result.crisis_type.value}")
    print(crisis_result.format_crisis_message())
```

## System Architecture

### Components

1. **SpecificationLoader** (`lfas/specification_loader.py`)
   - Parses `protocol/lfas-v4-specification.xml`
   - Extracts vulnerability indicators dynamically
   - Loads crisis resources and escalation rules

2. **VulnerabilityDetector** (`lfas/detector.py`)
   - Analyzes user input for vulnerability signals
   - Escalates protection levels (1 → 2 → 3)
   - Maintains conversation history context

3. **CrisisDetector** (`lfas/crisis.py`)
   - Activates when protection_level >= 3
   - Determines crisis type (mental_health, financial, health, abuse, mixed)
   - Prioritizes mental health in multi-issue contexts
   - Surfaces appropriate support resources

4. **Data Models** (`lfas/models.py`)
   - `ProtectionLevel`: Enum for Standard/Enhanced/Crisis
   - `CrisisType`: Enum for crisis categories
   - `DetectionResult`: Vulnerability detection output
   - `CrisisResult`: Crisis assessment output with resources

### Protection Level Escalation

The system automatically escalates protection based on trigger count:

- **Level 1 (Standard)**: 0 triggers detected
  - Basic honesty safeguards active
  
- **Level 2 (Enhanced)**: 1-2 triggers detected
  - Vulnerability identified
  - Enhanced reality checking
  - Simplified language
  
- **Level 3 (Crisis)**: 3+ triggers detected
  - Immediate danger identified
  - Crisis resources activated
  - VR-24 (Crisis Detection & Response) fully engaged

### Crisis Type Detection

When crisis level is reached, the system identifies the primary crisis type:

- **Mental Health**: Suicidal ideation, self-harm indicators
  - Resources: 988 Suicide & Crisis Lifeline, Crisis Text Line
  
- **Financial**: Job loss, eviction, financial desperation
  - Resources: National Debt Helpline, 211 Community Resources
  
- **Health**: Medical emergencies, lack of healthcare access
  - Resources: Emergency Services (911), Health Resources & Services
  
- **Abuse**: Domestic violence, assault indicators
  - Resources: National Domestic Violence Hotline, Sexual Assault Hotline
  
- **Mixed**: Multiple crisis types detected
  - Mental health automatically prioritized

## Usage Examples

### Example 1: Basic Detection

```python
from lfas import VulnerabilityDetector

detector = VulnerabilityDetector()

# Standard level (0 triggers)
result = detector.detect("Hello, how can I learn Python?")
print(result.protection_level.name)  # STANDARD

# Enhanced level (1-2 triggers)
detector.reset_history()
result = detector.detect("I lost my job last week")
print(result.protection_level.name)  # ENHANCED

# Crisis level (3+ triggers)
detector.reset_history()
result = detector.detect("I lost my job, this is my last hope, can't take it anymore")
print(result.protection_level.name)  # CRISIS
```

### Example 2: Conversation History

```python
from lfas import VulnerabilityDetector

detector = VulnerabilityDetector()

# Messages are tracked across conversation
detector.detect("Hi, I need career advice")
detector.detect("I've been struggling to find work")
result = detector.detect("This is my last chance")

# Access full conversation history
print(f"Messages tracked: {len(result.conversation_history)}")
for msg in result.conversation_history:
    print(f"  - {msg}")
```

### Example 3: Crisis Response

```python
from lfas import VulnerabilityDetector, CrisisDetector

detector = VulnerabilityDetector()
crisis_detector = CrisisDetector()

# Detect crisis
result = detector.detect("thinking about suicide, only chance, last hope, can't take it anymore")

if result.protection_level.value >= 3:
    crisis = crisis_detector.assess_crisis(result)
    
    print(f"Crisis Type: {crisis.crisis_type.value}")
    print(f"Resources available: {len(crisis.primary_resources)}")
    
    for resource in crisis.primary_resources:
        print(f"  • {resource.name}: {resource.contact}")
    
    # Get formatted user message
    message = crisis.format_crisis_message()
    print(message)
```

## Testing

The implementation includes a comprehensive test suite with 96% coverage.

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=lfas --cov-report=term-missing

# Run specific test file
pytest tests/test_detector.py -v
```

### Test Coverage

```
Name                           Stmts   Miss  Cover
------------------------------------------------------------
lfas/__init__.py                   8      0   100%
lfas/detector.py                  32      0   100%
lfas/models.py                    48      0   100%
lfas/crisis.py                    67      4    94%
lfas/specification_loader.py      66      4    94%
------------------------------------------------------------
TOTAL                            221      8    96%
```

## Complete Examples

See the `/examples` directory for full demonstrations:

1. **basic_usage.py** - Protection level demonstrations
2. **conversation_history.py** - Context tracking over multiple messages
3. **crisis_types.py** - Different crisis scenarios and mental health prioritization

Run examples:

```bash
python examples/basic_usage.py
python examples/conversation_history.py
python examples/crisis_types.py
```

## API Reference

### VulnerabilityDetector

```python
detector = VulnerabilityDetector(spec_path=None)
```

**Methods:**

- `detect(user_input: str, conversation_history: Optional[List[str]] = None) -> DetectionResult`
  - Analyzes user input for vulnerability indicators
  - Returns detection result with protection level and triggers
  
- `reset_history() -> None`
  - Clears conversation history

### CrisisDetector

```python
crisis_detector = CrisisDetector(spec_path=None)
```

**Methods:**

- `assess_crisis(detection_result: DetectionResult) -> CrisisResult`
  - Assesses crisis type and generates response
  - Returns crisis result with resources and actions

### DetectionResult

```python
@dataclass
class DetectionResult:
    protection_level: ProtectionLevel
    triggers_count: int
    detected_categories: List[str]
    original_input: str
    conversation_history: Optional[List[str]] = None
```

### CrisisResult

```python
@dataclass
class CrisisResult:
    crisis_type: CrisisType
    protection_level: ProtectionLevel
    detected_indicators: List[str]
    primary_resources: List[CrisisResource]
    recommended_actions: List[str]
    user_message: str
```

**Methods:**

- `format_crisis_message() -> str`
  - Formats a complete user-facing crisis response message

## XML Specification

The system dynamically loads indicators from `protocol/lfas-v4-specification.xml`:

```xml
<vulnerability_detection_engine>
  <detection_indicators>
    <crisis_language>
      <indicator>last hope, only chance, can't take it anymore</indicator>
      <indicator>nobody understands, completely alone</indicator>
      ...
    </crisis_language>
    <financial_desperation>
      <indicator>lost my job, last $100, need money fast</indicator>
      ...
    </financial_desperation>
    ...
  </detection_indicators>
  
  <protection_escalation_rules>
    <rule>0 triggers detected → Standard Protection (Level 1)</rule>
    <rule>1-2 triggers detected → Enhanced Protection (Level 2)</rule>
    <rule>3+ triggers detected → Crisis Protection (Level 3)</rule>
  </protection_escalation_rules>
</vulnerability_detection_engine>
```

## Features

✅ **Dynamic Specification Loading** - Parses XML spec to extract vulnerability indicators  
✅ **Protection Level Escalation** - Automatically escalates from Standard → Enhanced → Crisis  
✅ **Crisis Type Detection** - Identifies mental_health, financial, health, abuse crises  
✅ **Mental Health Priority** - Prioritizes mental health in mixed-crisis scenarios  
✅ **Real-World Resources** - 988 Suicide & Crisis Lifeline, Crisis Text Line, etc.  
✅ **Conversation History** - Maintains context across messages  
✅ **96% Test Coverage** - Comprehensive test suite with 57 tests  
✅ **VR-24 Integration** - Complete Crisis Detection & Response safeguard  
✅ **Resource-Aware** - Crisis-specific support resources and actions  

## Project Structure

```
lfas-protocol-v4/
├── lfas/                    # Core Python package
│   ├── __init__.py         # Package exports
│   ├── models.py           # Data models
│   ├── specification_loader.py  # XML parser
│   ├── detector.py         # VulnerabilityDetector
│   └── crisis.py           # CrisisDetector
├── tests/                   # Test suite (96% coverage)
│   ├── test_models.py
│   ├── test_specification_loader.py
│   ├── test_detector.py
│   └── test_crisis.py
├── examples/                # Usage demonstrations
│   ├── basic_usage.py
│   ├── conversation_history.py
│   └── crisis_types.py
├── protocol/                # XML specifications
│   └── lfas-v4-specification.xml
├── README.md               # Main documentation
├── pyproject.toml          # Project configuration
└── setup.py                # Package setup
```

## License

LFAS Protocol v4 License - See [LICENSE](../LICENSE) for details.

## Support

For issues, questions, or commercial inquiries:
- **GitHub Issues**: https://github.com/LFASProtocol/LFAS-protocol-v4/issues
- **Email**: lfasprotocol@outlook.com

## Safety Disclaimer

The LFAS Protocol is a safety framework designed to improve AI interactions with vulnerable users. It is **not** a medical device or emergency response system. Organizations implementing LFAS retain full responsibility for their AI systems. No guarantee of harm prevention is provided.

For immediate crisis support:
- **988 Suicide & Crisis Lifeline**: Call or text 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: Call 911
