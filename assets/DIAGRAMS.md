# LFAS Protocol v4 - Visual Flow Diagrams

This directory contains visual diagrams and assets for the LFAS Protocol.

## Protocol Flow Diagram

### Five-Stage LFAS Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INPUT                                   │
│              "I lost my job, this is my last hope"              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1: LISTEN                                                │
│  ─────────────────                                              │
│  • Extract context and intent                                   │
│  • Scan for vulnerability indicators                            │
│  • Identify high-stakes domains                                 │
│                                                                  │
│  Result: 2 triggers detected (financial_desperation,            │
│           crisis_language)                                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2: REFLECT                                               │
│  ─────────────────                                              │
│  • Declare assumptions                                          │
│  • Assess risks and uncertainties                               │
│  • Apply verification requirements                              │
│                                                                  │
│  Decision: ENHANCED Protection Level (VR-20, VR-22, VR-23)      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 3: WAIT                                                  │
│  ─────────────────                                              │
│  • Safety pause for confirmation                                │
│  • Disclose critical risks                                      │
│  • Require explicit user intent                                 │
│                                                                  │
│  Action: Prepare safeguarded response                           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 4: ACT                                                   │
│  ─────────────────                                              │
│  • Execute within verified scope                                │
│  • Apply active safeguards:                                     │
│    ✓ VR-20: Prevent unfounded optimism                          │
│    ✓ VR-22: Realistic capability assessment                     │
│    ✓ VR-23: Financial realism verification                      │
│  • Provide crisis resources if needed                           │
│                                                                  │
│  Output: Safe, reality-based response                           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 5: ACKNOWLEDGE                                           │
│  ─────────────────                                              │
│  • Confirm action completion                                    │
│  • State limitations and transparency level                     │
│  • Log intervention for monitoring                              │
│  • Reset for next interaction                                   │
│                                                                  │
│  Status: Intervention logged, ready for next input              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
              ┌───────────────┐
              │  SAFE OUTPUT  │
              └───────────────┘
```

## Protection Level Escalation

```
┌─────────────────────────────────────────────────────────────────┐
│                   INPUT ANALYSIS                                │
└───────────────────┬─────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
  0 TRIGGERS              1-2 TRIGGERS              3+ TRIGGERS
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌────────────────┐     ┌────────────────┐
│   LEVEL 1     │      │    LEVEL 2     │     │    LEVEL 3     │
│   STANDARD    │      │   ENHANCED     │     │    CRISIS      │
├───────────────┤      ├────────────────┤     ├────────────────┤
│ • VR-20       │      │ • All Level 1  │     │ • All Level 2  │
│ • VR-22       │      │ • Enhanced     │     │ • VR-24        │
│ • VR-23       │      │   checks       │     │ • VR-25        │
│               │      │ • Simplified   │     │ • Emergency    │
│ Basic         │      │   language     │     │   protocol     │
│ safeguards    │      │ • Crisis       │     │ • Human        │
│               │      │   resources    │     │   escalation   │
└───────────────┘      └────────────────┘     └────────────────┘
```

## Crisis Detection Flow

```
                        ┌─────────────────┐
                        │   USER INPUT    │
                        └────────┬────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  Vulnerability Check   │
                    │  (3+ triggers?)        │
                    └────────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │ NO          YES │
                    ▼                 ▼
          ┌──────────────┐   ┌─────────────────┐
          │   Continue    │   │  CRISIS DETECTED│
          │   Normal      │   └────────┬────────┘
          │   Processing  │            │
          └──────────────┘             ▼
                              ┌──────────────────┐
                              │ Identify Crisis  │
                              │ Type             │
                              └────────┬─────────┘
                                       │
                     ┌─────────────────┼─────────────────┬──────────┐
                     │                 │                 │          │
                     ▼                 ▼                 ▼          ▼
              ┌───────────┐    ┌──────────┐    ┌──────────┐  ┌─────────┐
              │ Suicidal  │    │Financial │    │  Health  │  │Domestic │
              │ Ideation  │    │  Crisis  │    │Emergency │  │Violence │
              └─────┬─────┘    └────┬─────┘    └────┬─────┘  └────┬────┘
                    │               │               │             │
                    └───────────────┼───────────────┴─────────────┘
                                    ▼
                          ┌──────────────────┐
                          │ Provide:         │
                          │ • Crisis hotlines│
                          │ • Resources      │
                          │ • Action steps   │
                          │ • Safety priority│
                          └──────────────────┘
```

## Safeguard Application Matrix

```
┌────────────────┬──────────┬──────────┬──────────┐
│ Safeguard      │ Level 1  │ Level 2  │ Level 3  │
├────────────────┼──────────┼──────────┼──────────┤
│ VR-20          │    ✓     │    ✓     │    ✓     │
│ Optimism       │          │          │          │
│ Prevention     │          │          │          │
├────────────────┼──────────┼──────────┼──────────┤
│ VR-22          │    ✓     │    ✓     │    ✓     │
│ Capability     │          │          │          │
│ Assessment     │          │          │          │
├────────────────┼──────────┼──────────┼──────────┤
│ VR-23          │    ✓     │    ✓     │    ✓     │
│ Financial      │          │          │          │
│ Realism        │          │          │          │
├────────────────┼──────────┼──────────┼──────────┤
│ VR-24          │    -     │    -     │    ✓     │
│ Crisis         │          │          │          │
│ Detection      │          │          │          │
├────────────────┼──────────┼──────────┼──────────┤
│ VR-25          │    -     │    -     │    ✓     │
│ Amplification  │          │          │          │
│ Prevention     │          │          │          │
└────────────────┴──────────┴──────────┴──────────┘

Legend: ✓ = Active, - = Inactive
```

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR APPLICATION                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │      LFAS PROTOCOL LAYER          │
        │  ┌─────────────────────────────┐  │
        │  │   Vulnerability Detection   │  │
        │  └──────────┬──────────────────┘  │
        │             │                      │
        │  ┌──────────▼──────────────────┐  │
        │  │   Protection Level          │  │
        │  │   Determination             │  │
        │  └──────────┬──────────────────┘  │
        │             │                      │
        │  ┌──────────▼──────────────────┐  │
        │  │   Safeguard Application     │  │
        │  └──────────┬──────────────────┘  │
        └─────────────┼──────────────────────┘
                      │
                      ▼
        ┌─────────────────────────────────┐
        │      AI MODEL / LLM             │
        │   (ChatGPT, Claude, etc.)       │
        └─────────────┬───────────────────┘
                      │
                      ▼
        ┌─────────────────────────────────┐
        │    LFAS POST-PROCESSING         │
        │  • Response validation          │
        │  • Crisis resource injection    │
        │  • Safety confirmation          │
        └─────────────┬───────────────────┘
                      │
                      ▼
              ┌───────────────┐
              │  SAFE OUTPUT  │
              │  TO USER      │
              └───────────────┘
```

## Usage in Code

### Basic Flow
```python
from lfas import VulnerabilityDetector, CrisisDetector

# Initialize
vuln_detector = VulnerabilityDetector()
crisis_detector = CrisisDetector()

# LISTEN
user_input = "I lost my job, this is my last hope"
detection = vuln_detector.detect(user_input)

# REFLECT
protection_level = detection.protection_level

# ACT
if detection.is_crisis():
    crisis_response = crisis_detector.assess_crisis(detection)
    output = crisis_response.format_crisis_message()
else:
    output = your_ai_generate_response(user_input, protection_level)

# ACKNOWLEDGE
log_intervention(detection)
return output
```

---

For more details, see:
- [API Documentation](../API.md)
- [Examples](../examples/README.md)
- [Implementation Guide](../implementation-guide.md)
