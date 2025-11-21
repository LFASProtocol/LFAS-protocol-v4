# LFAS Protocol v4 - Usage Examples

This directory contains example scripts demonstrating the LFAS Protocol v4 AI-powered vulnerability and crisis detection system.

## Running the Examples

First, install the LFAS package:

```bash
pip install -e .
```

Then run any of the examples:

```bash
python examples/basic_usage.py
python examples/conversation_history.py
python examples/crisis_types.py
```

## Example Descriptions

### 1. Basic Usage (`basic_usage.py`)

Demonstrates the three protection levels:
- **Standard Protection (Level 1)**: Normal interaction with basic safeguards
- **Enhanced Protection (Level 2)**: Vulnerability detected (1-2 triggers)
- **Crisis Protection (Level 3)**: Immediate danger identified (3+ triggers)

Shows how to:
- Initialize the VulnerabilityDetector
- Detect vulnerability signals
- Activate crisis support when needed
- Access crisis resources and recommendations

### 2. Conversation History (`conversation_history.py`)

Demonstrates:
- How conversation history is tracked across multiple messages
- Escalation of protection levels over time
- Context maintenance for ongoing detection
- Real-time monitoring of vulnerability signals

### 3. Crisis Types (`crisis_types.py`)

Demonstrates:
- Different crisis type detection (mental health, financial, health, abuse)
- Crisis-specific resources and recommendations
- Mental health prioritization in mixed-crisis scenarios
- Appropriate resource mapping for each crisis type

## Key Features Demonstrated

✅ **Dynamic XML Specification Loading**: Indicators loaded from XML spec  
✅ **Protection Level Escalation**: Automatic escalation based on trigger count  
✅ **Crisis Type Detection**: Identifies specific crisis types  
✅ **Mental Health Prioritization**: Mental health takes priority in mixed situations  
✅ **Real-World Resources**: 988, Crisis Text Line, and other verified resources  
✅ **Conversation Context**: Maintains history for better detection  
✅ **User-Facing Messaging**: Professional, empathetic crisis communications

## Example Output

When a crisis is detected, the system provides:

```
⚠️ CRISIS SUPPORT ACTIVATED

I can see you're going through an extremely difficult time...

📞 IMMEDIATE RESOURCES:
• 988 Suicide & Crisis Lifeline: 988 (call or text)
• Crisis Text Line: Text HOME to 741741

🔒 RECOMMENDED ACTIONS:
• Talk to someone trained in crisis support - call 988
• Do not make any permanent decisions right now
• Reach out to one of the crisis resources listed above

Remember: You are not alone. Professional help is available 24/7.
```

## Integration Example

```python
from lfas import VulnerabilityDetector, CrisisDetector

# Initialize
detector = VulnerabilityDetector()

# Detect vulnerability
result = detector.detect("I lost my job, this is my last hope, can't take it anymore")

# Check protection level
if result.protection_level.value >= 3:
    # Activate crisis support
    crisis = CrisisDetector().assess_crisis(result)
    print(crisis.format_crisis_message())
```

## Notes

- All examples use the same XML specification file
- Crisis resources are real and verified
- Examples are designed for educational and integration purposes
- Test in a safe environment before production use
