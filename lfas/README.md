# LFAS Protocol v4 - Python Implementation

## AI-Powered Vulnerability and Crisis Detection System

This directory contains the Python implementation of the LFAS Protocol v4, an AI-driven detection pipeline that identifies behavioral indicators, escalates user protection levels based on vulnerability signals, and triggers crisis detection mechanisms.

## Architecture

The system consists of four main components:

### 1. **SpecificationLoader** (`spec_loader.py`)
Dynamically parses XML specifications to extract:
- Vulnerability detection indicators (crisis language, financial desperation, health crisis, isolation)
- Protection escalation rules
- Crisis resources (988 Lifeline, Crisis Text Line, etc.)
- Verification requirements (VR-20 through VR-25)

### 2. **VulnerabilityDetector** (`detector.py`)
Analyzes user input for vulnerability indicators and determines protection levels:
- **Level 1 (Standard)**: 0 triggers - Basic protection
- **Level 2 (Enhanced)**: 1-2 triggers - Vulnerability detected
- **Level 3 (Crisis)**: 3+ triggers - Crisis protection activated

Features:
- Conversation history tracking
- Case-insensitive detection
- Dynamic specification reloading
- Multi-category indicator matching

### 3. **CrisisDetector** (`crisis.py`)
Implements VR-24: Crisis Detection & Response
- Assesses crisis type (mental health, financial, health, abuse, mixed)
- **Mental health prioritization** in multi-issue contexts
- Severity determination (moderate, high, critical)
- Crisis resource provision
- Recommended action generation
- User-facing crisis messaging

### 4. **Data Models** (`models.py`)
Type-safe data structures:
- `ProtectionLevel`: Enum for protection levels
- `CrisisType`: Enum for crisis categories
- `DetectionResult`: Vulnerability detection output
- `CrisisResult`: Crisis assessment output
- `CrisisResource`: Crisis support resource information

## Installation

```bash
# Install from repository
pip install git+https://github.com/LFASProtocol/LFAS-protocol-v4.git

# Or install in development mode
git clone https://github.com/LFASProtocol/LFAS-protocol-v4.git
cd LFAS-protocol-v4
pip install -e .
```

## Quick Start

```python
from lfas import VulnerabilityDetector, CrisisDetector

# Detect vulnerability
detector = VulnerabilityDetector()
result = detector.detect("I lost my job, this is my last hope, can't take it anymore")

print(f"Protection Level: {result.protection_level.name}")
print(f"Triggers Detected: {result.triggers_count}")

# Crisis response
if result.protection_level.value >= 3:
    crisis = CrisisDetector().assess_crisis(result)
    print(crisis.format_crisis_message())
```

## Key Features

### Dynamic XML Specification Loading
- Indicators loaded from `protocol/lfas-v4-specification.xml`
- Supports runtime specification updates
- Extensible detection patterns

### VR-24 Crisis Detection & Response
When protection level reaches 3:
1. Pause normal processing
2. Assess crisis type (mental health prioritized)
3. Provide immediate crisis resources
4. Generate intervention message
5. Recommend specific actions

### Crisis Resources Included
- **Mental Health**: 988 Suicide & Crisis Lifeline, Crisis Text Line
- **Financial**: National Foundation for Credit Counseling, 211 Resources
- **Health**: Emergency Services (911), HRSA Health Centers
- **Abuse**: National Domestic Violence Hotline, Sexual Assault Hotline

### Conversation History
- Maintains context across multiple interactions
- Supports escalation detection over time
- Optional history tracking for privacy

## Examples

See the `examples/` directory for detailed usage:

1. **basic_usage.py** - Core detection and crisis response workflow
2. **conversation_history.py** - Multi-turn conversation handling
3. **custom_specification.py** - Custom XML specification loading

Run examples:
```bash
python examples/basic_usage.py
python examples/conversation_history.py
python examples/custom_specification.py
```

## Testing

The implementation includes comprehensive test coverage (96%):

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=lfas --cov-report=term-missing

# Run specific test file
pytest tests/test_detector.py -v
```

Test suite includes:
- 59 tests across all modules
- Unit tests for each component
- Integration tests for full pipeline
- Edge case handling
- Crisis type coverage

## API Reference

### VulnerabilityDetector

```python
detector = VulnerabilityDetector(spec_path: Optional[str] = None)
```

**Methods:**
- `detect(user_input: str, maintain_history: bool = True) -> DetectionResult`
- `reset_history()` - Clear conversation history
- `reload_specification()` - Reload XML specification

### CrisisDetector

```python
crisis_detector = CrisisDetector(spec_loader: Optional[SpecificationLoader] = None)
```

**Methods:**
- `assess_crisis(detection_result: DetectionResult) -> CrisisResult`

**Requirements:**
- `detection_result.protection_level.value >= 3`

### SpecificationLoader

```python
loader = SpecificationLoader(spec_path: Optional[str] = None)
```

**Methods:**
- `get_detection_indicators() -> Dict[str, List[str]]`
- `get_protection_rules() -> Dict[str, str]`
- `get_crisis_resources() -> Dict[str, List[Dict]]`
- `get_verification_requirements() -> Dict[str, Dict]`
- `reload()` - Reload specification from file

## Detection Indicators

The system detects four categories of vulnerability:

### Crisis Language
- "last hope", "only chance", "can't take it anymore"
- "nobody understands", "completely alone"
- "if this doesn't work, I'm done"
- Suicidal ideation signals

### Financial Desperation
- "lost my job", "last $100", "need money fast"
- "desperate for income", "can't pay bills"
- "behind on rent", "facing eviction"

### Health Crisis
- "can't see a doctor", "no insurance"
- "pain won't stop", "no medical help"
- "can't afford medication"

### Isolation Indicators
- "no one to talk to", "family doesn't understand"
- "you're the only one who listens"
- "completely alone in this"

## Protection Levels

### Level 1: Standard Protection
- Active: VR-20, VR-22, VR-23
- Basic honesty safeguards
- Reality-based responses

### Level 2: Enhanced Protection
- All Level 1 safeguards plus:
- Enhanced reality checking
- Simplified language
- Repeated verification
- Crisis resource awareness

### Level 3: Crisis Protection
- All Level 2 safeguards plus:
- VR-24: Crisis Detection & Response (full activation)
- VR-25: Vulnerable User Amplification Prevention
- Emergency protocol activation
- Immediate safety focus

## Mental Health Prioritization

In mixed-crisis contexts (multiple crisis types detected), the system **prioritizes mental health**:

```python
# Example: Financial + Mental Health detected
# Result: Mental health crisis type with appropriate resources
```

This ensures that suicidal ideation or self-harm signals always receive immediate mental health intervention.

## Contributing

See the main repository [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

LFAS Protocol v4 License - See [LICENSE](../LICENSE) for details.

**Commercial Use:** Requires separate commercial license.  
**Contact:** lfasprotocol@outlook.com

## Support

For questions, issues, or commercial licensing:
- Email: lfasprotocol@outlook.com
- GitHub Issues: https://github.com/LFASProtocol/LFAS-protocol-v4/issues

---

**⚠️ Important Safety Note:**

This is a detection framework, not a substitute for professional mental health care or emergency services. Always direct users in crisis to:
- 988 Suicide & Crisis Lifeline (Call or text 988)
- 911 for immediate emergencies
- Local crisis resources

The system aids in detection and resource provision but does not replace human intervention.
