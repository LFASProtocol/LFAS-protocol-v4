# LFAS Protocol Integration Examples

This document provides examples of integrating LFAS Protocol v4 with popular AI frameworks and libraries.

## Table of Contents

- [Basic Integration](#basic-integration)
- [OpenAI API Integration](#openai-api-integration)
- [LangChain Integration](#langchain-integration)
- [Custom LLM Integration](#custom-llm-integration)
- [FastAPI Web Service](#fastapi-web-service)

## Basic Integration

The simplest way to integrate LFAS into your AI application:

```python
from lfas import VulnerabilityDetector, CrisisDetector

# Initialize detectors
vulnerability_detector = VulnerabilityDetector()
crisis_detector = CrisisDetector()

def safe_ai_response(user_input: str) -> dict:
    """Process user input with LFAS safety checks"""

    # Step 1: Detect vulnerability level
    detection = vulnerability_detector.detect(user_input)

    # Step 2: Check for crisis
    if detection.protection_level.value >= 3:
        crisis = crisis_detector.assess_crisis(detection)
        return {
            "requires_intervention": True,
            "crisis_message": crisis.format_crisis_message(),
            "resources": crisis.primary_resources,
        }

    # Step 3: Adjust AI behavior based on protection level
    if detection.protection_level.value == 2:
        return {
            "requires_intervention": False,
            "enhanced_protection": True,
            "note": "User may be vulnerable - use careful language",
        }

    # Standard response for protection level 1
    return {
        "requires_intervention": False,
        "enhanced_protection": False,
    }
```

## OpenAI API Integration

Integrate LFAS with OpenAI's GPT models:

```python
import openai
from lfas import VulnerabilityDetector, CrisisDetector

class SafeOpenAIClient:
    """OpenAI client with LFAS safety layer"""

    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.vulnerability_detector = VulnerabilityDetector()
        self.crisis_detector = CrisisDetector()

    def chat_completion(self, messages: list) -> dict:
        """Create chat completion with safety checks"""

        # Get user's latest message
        user_message = messages[-1]["content"]

        # Run LFAS detection
        detection = self.vulnerability_detector.detect(user_message)

        # Crisis intervention
        if detection.protection_level.value >= 3:
            crisis = self.crisis_detector.assess_crisis(detection)
            return {
                "role": "assistant",
                "content": crisis.user_message,
                "crisis_resources": [
                    {"name": r.name, "contact": r.contact}
                    for r in crisis.primary_resources
                ],
                "requires_intervention": True,
            }

        # Enhanced protection mode
        if detection.protection_level.value == 2:
            # Add system message for careful response
            enhanced_messages = [
                {
                    "role": "system",
                    "content": (
                        "The user may be vulnerable. Respond with extra care, "
                        "empathy, and avoid unfounded optimism. Do not make "
                        "promises about outcomes you cannot guarantee."
                    ),
                }
            ] + messages

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=enhanced_messages,
            )
        else:
            # Standard response
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
            )

        return {
            "role": "assistant",
            "content": response.choices[0].message.content,
            "protection_level": detection.protection_level.name,
            "requires_intervention": False,
        }


# Usage
client = SafeOpenAIClient(api_key="your-api-key")
result = client.chat_completion([
    {"role": "user", "content": "I lost my job and feel hopeless"}
])
```

## LangChain Integration

Create a LFAS-protected LangChain component:

```python
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import HumanMessage, SystemMessage
from lfas import VulnerabilityDetector, CrisisDetector


class LFASCallbackHandler(BaseCallbackHandler):
    """LangChain callback handler for LFAS safety checks"""

    def __init__(self):
        self.vulnerability_detector = VulnerabilityDetector()
        self.crisis_detector = CrisisDetector()
        self.intervention_required = False
        self.crisis_message = None

    def on_llm_start(self, serialized, prompts, **kwargs):
        """Check prompts before LLM execution"""
        for prompt in prompts:
            detection = self.vulnerability_detector.detect(prompt)

            if detection.protection_level.value >= 3:
                crisis = self.crisis_detector.assess_crisis(detection)
                self.intervention_required = True
                self.crisis_message = crisis.format_crisis_message()
                # Could raise exception to stop LLM execution
                raise InterventionRequired(self.crisis_message)


class InterventionRequired(Exception):
    """Exception raised when crisis intervention is needed"""
    pass


# Usage with LangChain
from langchain.chat_models import ChatOpenAI

callback_handler = LFASCallbackHandler()
llm = ChatOpenAI(callbacks=[callback_handler])

try:
    response = llm([HumanMessage(content="I want to end it all")])
except InterventionRequired as e:
    print(f"Crisis intervention activated: {e}")
```

## Custom LLM Integration

Wrap any LLM with LFAS protection:

```python
from typing import Optional, List
from lfas import VulnerabilityDetector, CrisisDetector, ProtectionLevel


class LFASProtectedLLM:
    """Generic wrapper for any LLM with LFAS protection"""

    def __init__(self, llm_instance):
        self.llm = llm_instance
        self.vulnerability_detector = VulnerabilityDetector()
        self.crisis_detector = CrisisDetector()
        self.conversation_history: List[str] = []

    def generate(self, prompt: str) -> dict:
        """Generate response with safety checks"""

        # Detect vulnerability with conversation context
        detection = self.vulnerability_detector.detect(
            prompt,
            conversation_history=self.conversation_history
        )

        # Update history
        self.conversation_history.append(prompt)

        # Crisis intervention
        if detection.protection_level == ProtectionLevel.CRISIS:
            crisis = self.crisis_detector.assess_crisis(detection)
            return {
                "response": crisis.user_message,
                "resources": crisis.primary_resources,
                "actions": crisis.recommended_actions,
                "bypass_llm": True,
            }

        # Modify prompt based on protection level
        safe_prompt = self._apply_protection(prompt, detection.protection_level)

        # Generate LLM response
        llm_response = self.llm.generate(safe_prompt)

        return {
            "response": llm_response,
            "protection_level": detection.protection_level.name,
            "triggers_detected": detection.triggers_count,
            "bypass_llm": False,
        }

    def _apply_protection(self, prompt: str, level: ProtectionLevel) -> str:
        """Apply protection-level specific modifications"""

        if level == ProtectionLevel.ENHANCED:
            # Add safety instructions to prompt
            return (
                "[SAFETY: User may be vulnerable. Respond with care and empathy. "
                "Avoid unfounded optimism and unrealistic promises.]\n\n"
                f"{prompt}"
            )

        return prompt

    def reset(self):
        """Reset conversation history"""
        self.conversation_history.clear()
        self.vulnerability_detector.reset_history()
```

## FastAPI Web Service

Create a web API with LFAS protection:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from lfas import VulnerabilityDetector, CrisisDetector

app = FastAPI(title="LFAS Protected AI Service")

# Initialize detectors
vulnerability_detector = VulnerabilityDetector()
crisis_detector = CrisisDetector()


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[str]] = None


class ChatResponse(BaseModel):
    response: str
    protection_level: str
    requires_intervention: bool
    crisis_resources: Optional[List[dict]] = None


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process chat message with LFAS safety checks"""

    # Detect vulnerability
    detection = vulnerability_detector.detect(
        request.message,
        conversation_history=request.conversation_history
    )

    # Crisis handling
    if detection.protection_level.value >= 3:
        crisis = crisis_detector.assess_crisis(detection)

        return ChatResponse(
            response=crisis.user_message,
            protection_level=detection.protection_level.name,
            requires_intervention=True,
            crisis_resources=[
                {
                    "name": r.name,
                    "contact": r.contact,
                    "description": r.description,
                }
                for r in crisis.primary_resources
            ],
        )

    # Enhanced protection
    if detection.protection_level.value == 2:
        # Here you would call your LLM with enhanced safety prompts
        ai_response = f"[Enhanced protection mode] I understand you're going through a difficult time..."
    else:
        # Standard response
        ai_response = "Standard AI response here..."

    return ChatResponse(
        response=ai_response,
        protection_level=detection.protection_level.name,
        requires_intervention=False,
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "lfas_version": "4.0.0"}


# Run with: uvicorn integration_examples:app --reload
```

## Best Practices

1. **Always check before LLM generation**: Run LFAS detection before sending prompts to your LLM
2. **Maintain conversation context**: Pass conversation history for better detection accuracy
3. **Handle crisis immediately**: Don't proceed with normal LLM generation during crisis
4. **Log interventions**: Track when LFAS intervenes for monitoring and improvement
5. **Test thoroughly**: Test with crisis scenarios to ensure proper integration

## Testing Your Integration

```python
def test_integration():
    """Test LFAS integration with various scenarios"""

    test_cases = [
        {
            "input": "Hello, how are you?",
            "expected_level": "STANDARD",
            "should_intervene": False,
        },
        {
            "input": "I lost my job and struggling financially",
            "expected_level": "ENHANCED",
            "should_intervene": False,
        },
        {
            "input": "I lost my job, this is my last hope, can't take it anymore",
            "expected_level": "CRISIS",
            "should_intervene": True,
        },
    ]

    for case in test_cases:
        result = safe_ai_response(case["input"])
        assert result["protection_level"] == case["expected_level"]
        assert result["requires_intervention"] == case["should_intervene"]

    print("All integration tests passed!")
```

## Additional Resources

- [LFAS Protocol Specification](../protocol/lfas-v4-specification.xml)
- [Implementation Guide](../IMPLEMENTATION.md)
- [API Reference](../README.md)

## Support

For integration questions or issues:
- GitHub Issues: https://github.com/LFASProtocol/LFAS-protocol-v4/issues
- Email: lfasprotocol@outlook.com
