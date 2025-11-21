# LFAS Protocol v4 - Integration Architecture

## System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      Your Application                             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │         Import LFAS Integration                            │ │
│  │  from integrations.python.openai import create_lfas_client │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────┬──────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│                 LFAS Middleware Layer                             │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐   │
│  │  LFASOpenAI    │  │ LFASAnthropic  │  │ LFASEngine      │   │
│  │  Wrapper       │  │ Wrapper        │  │ (Core)          │   │
│  └────────┬───────┘  └───────┬────────┘  └────────┬────────┘   │
│           │                   │                     │            │
│           └───────────────────┴─────────────────────┘            │
│                               │                                  │
│                    ┌──────────▼──────────┐                      │
│                    │  5-Stage Protocol    │                      │
│                    │  LISTEN → REFLECT    │                      │
│                    │  WAIT → ACT          │                      │
│                    │  ACKNOWLEDGE         │                      │
│                    └─────────────────────┘                      │
└───────────────────────┬──────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌────────────────┐
│  OpenAI API  │ │Anthropic API│ │  Other APIs    │
│  (GPT-4)     │ │  (Claude)   │ │  (Future)      │
└──────────────┘ └─────────────┘ └────────────────┘
```

## Data Flow

### Request Flow (User Message → Safe Response)

```
1. USER INPUT
   "I lost my job and need money fast"
          │
          ▼
2. LISTEN Stage (Vulnerability Detection)
   ┌─────────────────────────────────┐
   │ Scan for trigger phrases:       │
   │ ✓ "lost my job" (financial)     │
   │ ✓ "need money fast" (financial) │
   └─────────────────────────────────┘
          │
          ▼
3. REFLECT Stage (Protection Level Assessment)
   ┌─────────────────────────────────┐
   │ Triggers found: 2               │
   │ Protection Level: ENHANCED      │
   └─────────────────────────────────┘
          │
          ▼
4. Forward to AI Provider
   ┌─────────────────────────────────┐
   │ + LFAS system prompt            │
   │ + User message                  │
   │ → OpenAI/Anthropic API          │
   └─────────────────────────────────┘
          │
          ▼
5. Receive Raw AI Response
   "Here's how to make money fast..."
          │
          ▼
6. ACT Stage (Apply Safeguards)
   ┌─────────────────────────────────┐
   │ ✓ VR-20: Filter optimistic phrases│
   │ ✓ VR-22: Check capability claims │
   │ ✓ VR-23: Add financial disclaimer│
   └─────────────────────────────────┘
          │
          ▼
7. ACKNOWLEDGE Stage (Return with Metadata)
   {
     content: "Safe response...\n\n⚠️ Financial Reality Check...",
     metadata: {
       protection_level: "ENHANCED",
       triggers_detected: 2,
       safeguards_applied: ["VR-20", "VR-22", "VR-23"]
     }
   }
          │
          ▼
8. RETURN TO APPLICATION
```

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    LFAS Core Engine                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ VulnerabilityIndicators                              │  │
│  │  - CRISIS_LANGUAGE                                   │  │
│  │  - FINANCIAL_DESPERATION                             │  │
│  │  - HEALTH_CRISIS                                     │  │
│  │  - ISOLATION_INDICATORS                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ ProtectionLevel (Enum)                               │  │
│  │  - STANDARD (1)                                      │  │
│  │  - ENHANCED (2)                                      │  │
│  │  - CRISIS (3)                                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ LFASEngine                                           │  │
│  │  + process_message()                                 │  │
│  │  - _listen()          # Stage 1                      │  │
│  │  - _reflect()         # Stage 2                      │  │
│  │  - _act()             # Stage 4                      │  │
│  │  - _acknowledge()     # Stage 5                      │  │
│  │  - _apply_vr20()      # Optimism filter              │  │
│  │  - _apply_vr22()      # Capability filter            │  │
│  │  - _apply_vr23()      # Financial disclaimer         │  │
│  │  - _apply_vr24()      # Crisis resources             │  │
│  │  - _apply_vr25()      # Amplification prevention     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  Integration Wrappers                        │
│                                                              │
│  ┌────────────────────┐        ┌────────────────────┐      │
│  │   LFASOpenAI       │        │  LFASAnthropic     │      │
│  │                    │        │                    │      │
│  │ + __init__()       │        │ + __init__()       │      │
│  │ + chat_completion()│        │ + create_message() │      │
│  │ + stream()         │        │ + stream()         │      │
│  │ + reset()          │        │ + reset()          │      │
│  │ - lfas_engine      │        │ - lfas_engine      │      │
│  └────────────────────┘        └────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Protection Level Escalation Matrix

```
┌────────────────┬─────────────┬──────────────────────────────┐
│ Triggers       │ Level       │ Active Safeguards            │
├────────────────┼─────────────┼──────────────────────────────┤
│ 0-1            │ STANDARD    │ VR-20, VR-22                 │
│                │             │ (Basic honesty filters)      │
├────────────────┼─────────────┼──────────────────────────────┤
│ 2              │ ENHANCED    │ VR-20, VR-22, VR-23          │
│                │             │ + Financial disclaimers      │
│                │             │ + Language simplification    │
├────────────────┼─────────────┼──────────────────────────────┤
│ 3+             │ CRISIS      │ ALL (VR-20 through VR-25)    │
│                │             │ + Crisis resources           │
│                │             │ + Human connection encouragement│
└────────────────┴─────────────┴──────────────────────────────┘
```

## Vulnerability Detection Flow

```
User Input → Lowercase → Pattern Matching → Categorize → Count
                            ↓
                    ┌───────────────┐
                    │ Crisis?       │ → "can't take it" → crisis:can't take it
                    │ Financial?    │ → "lost my job" → financial:lost my job
                    │ Health?       │ → "no insurance" → health:no insurance
                    │ Isolation?    │ → "nobody cares" → isolation:nobody cares
                    └───────────────┘
                            ↓
                    Total Triggers: N
                            ↓
                    ┌───────────────┐
                    │ N = 0-1?  → STANDARD
                    │ N = 2?    → ENHANCED
                    │ N >= 3?   → CRISIS
                    └───────────────┘
```

## Conversation State Management

```
┌─────────────────────────────────────────────────────────┐
│ Conversation State (LFASEngine)                         │
├─────────────────────────────────────────────────────────┤
│ conversation_history: []                                │
│   - Exchange 1: {user, response, triggers, level}       │
│   - Exchange 2: {user, response, triggers, level}       │
│   - ...                                                 │
│                                                         │
│ current_protection_level: STANDARD/ENHANCED/CRISIS      │
│ exchanges_without_triggers: 0                           │
│                                                         │
│ De-escalation Rule:                                     │
│   If exchanges_without_triggers >= 3:                   │
│     → Reset to STANDARD                                 │
└─────────────────────────────────────────────────────────┘
```

## Multi-Platform Support

```
                    ┌──────────────────┐
                    │  LFAS Protocol   │
                    │  Specification   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
    ┌─────────────┐  ┌─────────────┐  ┌──────────┐
    │   Python    │  │ JavaScript  │  │  Future  │
    │             │  │  (Node.js)  │  │  (Go,    │
    │ - OpenAI    │  │             │  │   Rust,  │
    │ - Anthropic │  │ - OpenAI    │  │   Java)  │
    │             │  │ - Anthropic │  │          │
    └─────────────┘  └─────────────┘  └──────────┘
```

## File Structure

```
integrations/
│
├── README.md              # Complete integration guide
├── QUICKSTART.md          # 5-minute setup guide
│
├── python/
│   ├── shared/
│   │   ├── lfas_engine.py       # Core protocol engine
│   │   ├── test_lfas.py         # Test suite
│   │   └── __init__.py
│   │
│   ├── openai/
│   │   ├── lfas_openai.py       # OpenAI wrapper
│   │   ├── example_usage.py     # Working examples
│   │   ├── requirements.txt     # Dependencies
│   │   └── __init__.py
│   │
│   └── anthropic/
│       ├── lfas_anthropic.py    # Anthropic wrapper
│       ├── example_usage.py     # Working examples
│       ├── requirements.txt     # Dependencies
│       └── __init__.py
│
└── javascript/
    ├── shared/
    │   └── lfas-engine.js       # Core protocol engine
    │
    ├── openai/
    │   ├── lfas-openai.js       # OpenAI wrapper
    │   ├── example-usage.js     # Working examples
    │   └── package.json         # Dependencies
    │
    └── anthropic/
        ├── lfas-anthropic.js    # Anthropic wrapper
        ├── example-usage.js     # Working examples
        └── package.json         # Dependencies
```

## Integration Patterns

### Pattern 1: Drop-in Replacement
```python
# Before (vanilla OpenAI)
from openai import OpenAI
client = OpenAI(api_key="...")
response = client.chat.completions.create(...)

# After (LFAS-protected)
from integrations.python.openai import create_lfas_client
lfas = create_lfas_client(api_key="...")
response = lfas.chat_completion(...)  # Now protected!
```

### Pattern 2: Existing Code Wrapper
```python
# Wrap existing AI calls
def get_ai_response(user_message):
    lfas = create_lfas_client(api_key="...")
    response = lfas.chat_completion(
        messages=[{"role": "user", "content": user_message}]
    )
    
    # Log safety metadata
    logger.info(f"Protection: {response['metadata']['protection_level']}")
    
    return response['content']
```

### Pattern 3: Middleware in Web Apps
```python
# Flask/FastAPI integration
@app.post("/chat")
async def chat(message: str):
    lfas = create_lfas_client(api_key=API_KEY)
    response = lfas.chat_completion(
        messages=[{"role": "user", "content": message}]
    )
    
    return {
        "message": response['content'],
        "safety": response['metadata']
    }
```

---

**For more details, see:**
- [Integration README](README.md)
- [Quick Start Guide](QUICKSTART.md)
- [LFAS v4 Specification](../protocol/lfas-v4-specification.xml)
