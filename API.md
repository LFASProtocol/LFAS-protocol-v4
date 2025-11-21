# LFAS Protocol v4 - API Reference

Complete API documentation for the LFAS Protocol Python implementation.

## Table of Contents

- [Core Modules](#core-modules)
  - [VulnerabilityDetector](#vulnerabilitydetector)
  - [CrisisDetector](#crisisdetector)
- [Data Models](#data-models)
  - [ProtectionLevel](#protectionlevel)
  - [DetectionResult](#detectionresult)
  - [CrisisResponse](#crisisresponse)
  - [SafeguardViolation](#safeguardviolation)
- [Usage Examples](#usage-examples)

---

## Core Modules

### VulnerabilityDetector

**Module:** `lfas.detector`

The main class for detecting vulnerability indicators in user input.

#### Constructor

```python
VulnerabilityDetector(spec_path: str = "protocol/lfas-v4-specification.xml")
```

**Parameters:**
- `spec_path` (str, optional): Path to the XML specification file. Defaults to `"protocol/lfas-v4-specification.xml"`.

**Example:**
```python
from lfas import VulnerabilityDetector

# Default specification
detector = VulnerabilityDetector()

# Custom specification
detector = VulnerabilityDetector(spec_path="/custom/path/spec.xml")
```

#### Methods

##### `detect(user_input: str) -> DetectionResult`

Analyze user input for vulnerability indicators.

**Parameters:**
- `user_input` (str): The user's message to analyze

**Returns:**
- `DetectionResult`: Object containing detection results

**Example:**
```python
result = detector.detect("I lost my job and this is my last hope")
print(f"Protection Level: {result.protection_level.name}")
print(f"Triggers: {result.triggers_count}")
```

**Detection Logic:**
- Scans input for phrases from the XML specification
- Case-insensitive matching
- Counts triggers across all categories
- Determines protection level based on trigger count:
  - 0 triggers → STANDARD (Level 1)
  - 1-2 triggers → ENHANCED (Level 2)
  - 3+ triggers → CRISIS (Level 3)

---

### CrisisDetector

**Module:** `lfas.crisis`

Handles crisis detection and response generation.

#### Constructor

```python
CrisisDetector()
```

No parameters required. Initializes with built-in crisis resources.

**Example:**
```python
from lfas import CrisisDetector

crisis_detector = CrisisDetector()
```

#### Methods

##### `assess_crisis(detection_result: DetectionResult) -> CrisisResponse`

Assess if a detection result indicates a crisis and provide appropriate resources.

**Parameters:**
- `detection_result` (DetectionResult): Result from VulnerabilityDetector

**Returns:**
- `CrisisResponse`: Object containing crisis assessment and resources

**Example:**
```python
detection = vuln_detector.detect("I want to end my life")
crisis_response = crisis_detector.assess_crisis(detection)

if crisis_response.is_crisis:
    print(crisis_response.format_crisis_message())
```

**Crisis Types Detected:**
- `suicidal_ideation`: Suicide-related statements
- `financial_crisis`: Severe financial distress
- `health_emergency`: Medical emergencies
- `domestic_violence`: Abuse situations
- `general_crisis`: Other crisis situations

##### `format_safe_response(crisis_response: CrisisResponse, original_ai_response: str = "") -> str`

Format a safe response that prioritizes crisis resources.

**Parameters:**
- `crisis_response` (CrisisResponse): The crisis assessment
- `original_ai_response` (str, optional): Original AI response (will be suppressed for crisis)

**Returns:**
- `str`: Safe formatted response

**Example:**
```python
safe_response = crisis_detector.format_safe_response(
    crisis_response, 
    "Here are some tips..."
)
print(safe_response)
```

---

## Data Models

### ProtectionLevel

**Module:** `lfas.models`

Enum representing protection levels.

```python
class ProtectionLevel(Enum):
    STANDARD = 1  # No vulnerability detected
    ENHANCED = 2  # Vulnerability detected (1-2 triggers)
    CRISIS = 3    # Crisis situation (3+ triggers)
```

**Usage:**
```python
from lfas import ProtectionLevel

if result.protection_level == ProtectionLevel.CRISIS:
    # Handle crisis
```

---

### DetectionResult

**Module:** `lfas.models`

Result object from vulnerability detection.

#### Attributes

- `protection_level` (ProtectionLevel): Detected protection level
- `triggers_count` (int): Number of vulnerability triggers found
- `detected_categories` (List[str]): Categories of triggers detected
- `original_input` (str): The original user input

#### Methods

##### `is_crisis() -> bool`

Check if result indicates a crisis situation.

```python
if result.is_crisis():
    # Handle crisis
```

##### `is_vulnerable() -> bool`

Check if result indicates any vulnerability (ENHANCED or CRISIS).

```python
if result.is_vulnerable():
    # Apply enhanced safeguards
```

##### `__str__() -> str`

String representation of the detection result.

```python
print(result)
# Output: Protection Level: ENHANCED (Triggers: 2, Categories: financial_desperation)
```

#### Example

```python
from lfas import VulnerabilityDetector

detector = VulnerabilityDetector()
result = detector.detect("I lost my job")

print(f"Level: {result.protection_level.name}")
print(f"Triggers: {result.triggers_count}")
print(f"Categories: {result.detected_categories}")
print(f"Is vulnerable: {result.is_vulnerable()}")
print(f"Is crisis: {result.is_crisis()}")
```

---

### CrisisResponse

**Module:** `lfas.models`

Response object for crisis situations.

#### Attributes

- `is_crisis` (bool): Whether this is a crisis situation
- `crisis_type` (Optional[str]): Type of crisis detected
- `resources` (List[str]): Crisis resources and hotlines
- `recommended_actions` (List[str]): Recommended actions for the user

#### Methods

##### `format_crisis_message() -> str`

Format a complete crisis response message.

```python
message = crisis_response.format_crisis_message()
print(message)
```

**Output format:**
```
⚠️ CRISIS SUPPORT NEEDED

Detected: suicidal_ideation

IMMEDIATE RESOURCES:
• National Suicide Prevention Lifeline: 988 (US)
• Crisis Text Line: Text HOME to 741741
...

RECOMMENDED ACTIONS:
• Call or text a crisis helpline immediately
• Reach out to a trusted friend or family member
...
```

#### Example

```python
from lfas import VulnerabilityDetector, CrisisDetector

vuln_detector = VulnerabilityDetector()
crisis_detector = CrisisDetector()

detection = vuln_detector.detect("I want to end my life")
crisis_response = crisis_detector.assess_crisis(detection)

if crisis_response.is_crisis:
    print(f"Crisis Type: {crisis_response.crisis_type}")
    print(f"Resources: {len(crisis_response.resources)}")
    print(crisis_response.format_crisis_message())
```

---

### SafeguardViolation

**Module:** `lfas.models`

Record of a safeguard violation (for future use in response validation).

#### Attributes

- `safeguard_id` (str): ID of violated safeguard (e.g., "VR-20")
- `safeguard_name` (str): Name of the safeguard
- `violation_type` (str): Type of violation
- `original_text` (str): Text that violated the safeguard
- `suggested_replacement` (Optional[str]): Suggested safe alternative

**Note:** This model is defined for future response validation features.

---

## Usage Examples

### Basic Detection

```python
from lfas import VulnerabilityDetector

detector = VulnerabilityDetector()

# Standard input
result = detector.detect("Hello, how are you?")
assert result.protection_level.name == "STANDARD"

# Vulnerable input
result = detector.detect("I lost my job and need help")
assert result.is_vulnerable() == True
```

### Crisis Handling

```python
from lfas import VulnerabilityDetector, CrisisDetector

vuln_detector = VulnerabilityDetector()
crisis_detector = CrisisDetector()

user_input = "I want to end my life, nobody understands, this is the end"
detection = vuln_detector.detect(user_input)

if detection.is_crisis():
    crisis_response = crisis_detector.assess_crisis(detection)
    safe_response = crisis_detector.format_safe_response(
        crisis_response,
        "Here's some advice..."  # This will be suppressed
    )
    print(safe_response)
```

### Full Integration

```python
from lfas import VulnerabilityDetector, CrisisDetector, ProtectionLevel

class SafeAI:
    def __init__(self):
        self.vuln_detector = VulnerabilityDetector()
        self.crisis_detector = CrisisDetector()
    
    def process(self, user_input: str) -> str:
        # LISTEN: Detect vulnerability
        detection = self.vuln_detector.detect(user_input)
        
        # REFLECT & ACT: Handle based on protection level
        if detection.protection_level == ProtectionLevel.CRISIS:
            crisis_response = self.crisis_detector.assess_crisis(detection)
            return crisis_response.format_crisis_message()
        
        elif detection.protection_level == ProtectionLevel.ENHANCED:
            return self._generate_enhanced_response(user_input)
        
        else:
            return self._generate_standard_response(user_input)
    
    def _generate_enhanced_response(self, input_text: str) -> str:
        return "I understand this is difficult. [Enhanced safeguards applied]"
    
    def _generate_standard_response(self, input_text: str) -> str:
        return "How can I help you today?"

# Usage
ai = SafeAI()
response = ai.process("I lost my job, this is my last hope, I can't go on")
print(response)
```

---

## Error Handling

### Common Errors

**XML Parse Error:**
```python
try:
    detector = VulnerabilityDetector("invalid.xml")
except xml.etree.ElementTree.ParseError as e:
    print(f"Invalid XML specification: {e}")
```

**File Not Found:**
```python
try:
    detector = VulnerabilityDetector("nonexistent.xml")
except FileNotFoundError as e:
    print(f"Specification file not found: {e}")
```

---

## Type Hints

All modules use Python type hints for better IDE support:

```python
from typing import List, Dict, Optional
from lfas import VulnerabilityDetector, DetectionResult

def analyze_conversation(messages: List[str]) -> List[DetectionResult]:
    detector = VulnerabilityDetector()
    return [detector.detect(msg) for msg in messages]
```

---

## Thread Safety

The detector classes are thread-safe for reading:
- Multiple threads can share a `VulnerabilityDetector` instance
- `CrisisDetector` is stateless and thread-safe

For high-concurrency applications, consider using a detector pool or creating instances per thread.

---

## Performance Considerations

- **XML parsing**: Done once at initialization (~1ms)
- **Detection**: Simple string matching (~0.1-1ms per input)
- **Memory**: Minimal (~1-5MB depending on specification size)
- **No external dependencies**: No network calls, all local processing

**Optimization tips:**
- Reuse detector instances (don't create per request)
- For very high traffic, consider caching detection results
- Profile your specific use case

---

## Version Compatibility

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Dependencies**: lxml (for XML parsing), requests (for future features)

---

## See Also

- [Implementation Guide](implementation-guide.md)
- [Examples](examples/README.md)
- [FAQ](FAQ.md)
- [Protocol Specification](protocol/lfas-v4-specification.xml)
