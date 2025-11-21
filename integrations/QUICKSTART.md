# LFAS Protocol v4 - Quick Start Guide

Get started with LFAS-protected AI in 5 minutes! 🚀

## Choose Your Platform

### Option 1: Python + OpenAI

**1. Install dependencies:**
```bash
cd integrations/python/openai
pip install -r requirements.txt
```

**2. Set your API key:**
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

**3. Copy this code into `my_app.py`:**
```python
from integrations.python.openai import create_lfas_client

# Create LFAS-protected client (one line!)
lfas = create_lfas_client(api_key="your-openai-key", model="gpt-4")

# Use it like normal OpenAI
response = lfas.chat_completion(
    messages=[
        {"role": "user", "content": "I lost my job and need money fast"}
    ]
)

print(response['content'])
print(f"\nProtection Level: {response['metadata']['protection_level']}")
print(f"Safeguards: {', '.join(response['metadata']['safeguards_applied'])}")
```

**4. Run it:**
```bash
python my_app.py
```

---

### Option 2: Python + Anthropic (Claude)

**1. Install dependencies:**
```bash
cd integrations/python/anthropic
pip install -r requirements.txt
```

**2. Set your API key:**
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

**3. Copy this code into `my_app.py`:**
```python
from integrations.python.anthropic import create_lfas_client

# Create LFAS-protected client
lfas = create_lfas_client(api_key="your-anthropic-key")

# Use it like normal Anthropic
response = lfas.create_message(
    messages=[
        {"role": "user", "content": "I can't take it anymore"}
    ]
)

print(response['content'])
print(f"\nProtection Level: {response['metadata']['protection_level']}")
```

**4. Run it:**
```bash
python my_app.py
```

---

### Option 3: JavaScript + OpenAI

**1. Install dependencies:**
```bash
cd integrations/javascript/openai
npm install
```

**2. Set your API key:**
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

**3. Copy this code into `my-app.js`:**
```javascript
const { createLFASClient } = require('./lfas-openai');

async function main() {
  // Create LFAS-protected client
  const lfas = createLFASClient(process.env.OPENAI_API_KEY, 'gpt-4');
  
  // Use it like normal OpenAI
  const response = await lfas.chatCompletion([
    { role: 'user', content: 'I need money fast, facing eviction' }
  ]);
  
  console.log(response.content);
  console.log(`\nProtection Level: ${response.metadata.protectionLevel}`);
  console.log(`Safeguards: ${response.metadata.safeguardsApplied.join(', ')}`);
}

main().catch(console.error);
```

**4. Run it:**
```bash
node my-app.js
```

---

### Option 4: JavaScript + Anthropic

**1. Install dependencies:**
```bash
cd integrations/javascript/anthropic
npm install
```

**2. Set your API key:**
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

**3. Copy this code into `my-app.js`:**
```javascript
const { createLFASClient } = require('./lfas-anthropic');

async function main() {
  const lfas = createLFASClient(process.env.ANTHROPIC_API_KEY);
  
  const response = await lfas.createMessage([
    { role: 'user', content: "I'm completely alone. Nobody understands." }
  ]);
  
  console.log(response.content);
  console.log(`\nProtection Level: ${response.metadata.protectionLevel}`);
}

main().catch(console.error);
```

**4. Run it:**
```bash
node my-app.js
```

---

## What Just Happened? 🤔

When you run any of the examples above, LFAS automatically:

1. **👂 LISTEN**: Scans user input for vulnerability indicators
   - Crisis language ("can't take it", "last hope")
   - Financial desperation ("lost job", "need money fast")
   - Health crises
   - Isolation indicators

2. **🧠 REFLECT**: Determines protection level
   - **STANDARD** (0-1 triggers): Basic safeguards
   - **ENHANCED** (2 triggers): Extra protection + financial disclaimers
   - **CRISIS** (3+ triggers): Full protection + crisis resources

3. **⏸️ WAIT**: Safety pause (conceptual validation step)

4. **🛡️ ACT**: Applies safeguards to the response
   - Filters unrealistic promises ("guaranteed success")
   - Adds reality checks and disclaimers
   - Provides crisis resources when needed
   - Encourages human consultation

5. **✅ ACKNOWLEDGE**: Returns metadata
   - Protection level used
   - Triggers detected
   - Safeguards applied

---

## Common Scenarios

### Scenario 1: Normal Conversation (No Triggers)
```
User: "How do I learn Python?"
Protection Level: STANDARD
Safeguards: VR-20, VR-22 (basic honesty filters)
```

### Scenario 2: Financial Vulnerability (2 Triggers)
```
User: "I lost my job and need money fast"
Triggers: "lost my job", "need money fast"
Protection Level: ENHANCED
Safeguards: VR-20, VR-22, VR-23 (+ financial disclaimers)
```

### Scenario 3: Crisis (3+ Triggers)
```
User: "I can't take it anymore. This is my last hope. Nobody understands."
Triggers: "can't take it anymore", "last hope", "nobody understands"
Protection Level: CRISIS
Safeguards: ALL (VR-20, VR-22, VR-23, VR-24, VR-25)
Response includes: Crisis hotline numbers, encouragement to seek help
```

---

## Next Steps

- 📖 Read the [Integration Guide](integrations/README.md) for advanced usage
- 🧪 Run the example files in each integration directory
- 🔧 Customize vulnerability indicators for your domain
- 📊 Access metadata to log safety interventions
- 🔄 Track conversation history for multi-turn safety

---

## Troubleshooting

**"Module not found"**
- Make sure you're in the correct directory
- Run `pip install -r requirements.txt` or `npm install`

**"API key not set"**
- Export your API key: `export OPENAI_API_KEY="..."`
- Or pass it directly: `create_lfas_client(api_key="your-key")`

**"Protection level not changing"**
- LFAS maintains state across messages
- Use `lfas.reset_conversation()` to reset
- Protection de-escalates after 3+ exchanges without triggers

---

## Questions?

- 📧 Email: lfasprotocol@outlook.com
- 📄 Docs: See `/integrations/README.md`
- 🔍 Examples: See `example_usage.py` or `example-usage.js` files

---

**Ready to build safer AI? Start coding! 🚀**
