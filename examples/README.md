# LFAS Protocol v4 - Examples

This directory contains example scripts demonstrating how to use the LFAS Protocol v4 in various scenarios.

## Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates the fundamental features of LFAS Protocol:
- Vulnerability detection
- Protection level determination
- Crisis response handling
- Safe response formatting

**Run it:**
```bash
python examples/basic_usage.py
```

**What you'll learn:**
- How to initialize the VulnerabilityDetector
- How to detect different levels of vulnerability
- How to handle crisis situations
- How to format safe responses

### 2. Chatbot Integration (`chatbot_integration.py`)

Shows how to integrate LFAS into a chatbot application following the 5-stage protocol loop:
- LISTEN: Monitor user input
- REFLECT: Assess vulnerability
- WAIT: Safety pause
- ACT: Generate safe response
- ACKNOWLEDGE: Log and confirm

**Run it:**
```bash
python examples/chatbot_integration.py
```

**What you'll learn:**
- How to implement the full LFAS interaction loop
- How to apply different safeguards based on protection level
- How to maintain conversation history with safety tracking
- How to generate appropriate responses for different vulnerability levels

## Additional Examples

### Quick Start - Detection Only

```python
from lfas import VulnerabilityDetector

detector = VulnerabilityDetector()
result = detector.detect("I lost my job and this is my last hope")

print(f"Protection Level: {result.protection_level.name}")
print(f"Triggers Found: {result.triggers_count}")
print(f"Categories: {result.detected_categories}")
```

### Quick Start - Crisis Handling

```python
from lfas import VulnerabilityDetector, CrisisDetector

vuln_detector = VulnerabilityDetector()
crisis_detector = CrisisDetector()

user_input = "I want to end my life"
detection = vuln_detector.detect(user_input)

if detection.is_crisis():
    crisis_response = crisis_detector.assess_crisis(detection)
    print(crisis_response.format_crisis_message())
```

## Integration Patterns

### Pattern 1: Pre-Processing Filter

Use LFAS as a pre-processing filter before your AI generates a response:

```python
def process_user_input(user_input: str) -> dict:
    detection = vulnerability_detector.detect(user_input)
    
    return {
        'input': user_input,
        'protection_level': detection.protection_level,
        'requires_special_handling': detection.is_vulnerable()
    }
```

### Pattern 2: Post-Processing Safety Layer

Use LFAS to modify AI-generated responses:

```python
def make_response_safe(ai_response: str, detection_result) -> str:
    if detection_result.is_crisis():
        crisis_response = crisis_detector.assess_crisis(detection_result)
        return crisis_detector.format_safe_response(
            crisis_response, 
            ai_response
        )
    return ai_response
```

### Pattern 3: Full Integration

Combine pre and post-processing for maximum safety:

```python
def safe_ai_interaction(user_input: str) -> str:
    # Pre-process: Detect vulnerability
    detection = vuln_detector.detect(user_input)
    
    # Handle crisis immediately
    if detection.is_crisis():
        crisis_response = crisis_detector.assess_crisis(detection)
        return crisis_response.format_crisis_message()
    
    # Generate AI response with context
    ai_response = your_ai_model.generate(
        user_input,
        protection_level=detection.protection_level
    )
    
    # Post-process: Apply safeguards
    return apply_safeguards(ai_response, detection)
```

## Testing Your Integration

Always test your integration with various inputs:

```python
test_cases = [
    ("Hello world", "Standard"),
    ("I lost my job", "Enhanced"),
    ("I can't take it anymore", "Crisis"),
]

for input_text, expected_level in test_cases:
    result = detector.detect(input_text)
    assert result.protection_level.name.upper() == expected_level.upper()
```

## Best Practices

1. **Always check for crisis first**: Crisis situations require immediate, specific responses
2. **Don't suppress crisis resources**: Never hide or deprioritize crisis helplines in responses
3. **Log protection levels**: Track which protection levels are being triggered for analysis
4. **Test with real scenarios**: Use the documented harm cases from the research to validate
5. **Respect user privacy**: Don't store sensitive vulnerability data longer than necessary

## Need Help?

- See the main [README.md](../README.md) for protocol overview
- Check [implementation-guide.md](../implementation-guide.md) for detailed integration steps
- Review the [protocol specification](../protocol/lfas-v4-specification.xml) for complete details
- Contact: lfasprotocol@outlook.com
