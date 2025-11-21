# LFAS Protocol v4: Delegation Guidelines

## Purpose

This document clarifies which aspects of the LFAS Protocol v4 implementation can be delegated to individual teams, platforms, or integrators, and which elements are **non-negotiable** and must remain consistent across all implementations.

---

## 1. Non-Delegable Core Components

These elements are the foundational architecture of LFAS and **MUST NOT** be modified, skipped, or delegated differently:

### 1.1 The Five-Stage Mandatory Loop

The `LISTEN → REFLECT → WAIT → ACT → ACKNOWLEDGE` sequence is **non-negotiable**.

**Cannot be delegated:**
- The order of the five stages
- Skipping any of the five stages
- The fundamental purpose of each stage
- The requirement that all five stages execute for every interaction

**Why:** This loop is the core safety mechanism. Altering it breaks the protocol's ability to protect vulnerable users.

### 1.2 Verification Requirements (VR-20 through VR-25)

The specific safeguards defined in the protocol specification are **mandatory**.

**Cannot be delegated:**
- VR-20: Unfounded Optimism Prevention
- VR-22: Realistic Capability Assessment
- VR-23: Financial Realism Verification
- VR-24: Crisis Detection & Response
- VR-25: Vulnerable User Amplification Prevention

**Why:** These requirements represent the minimum safety threshold. Removing or weakening them puts vulnerable users at risk.

### 1.3 Protection Level Thresholds

The three-tier protection system is **non-negotiable**.

**Cannot be delegated:**
- Level 1 (Standard): Basic protection
- Level 2 (Enhanced): Vulnerability detected
- Level 3 (Crisis): Immediate danger
- The escalation rules (0 triggers → Level 1, 1-2 triggers → Level 2, 3+ triggers → Level 3)

**Why:** Standardized protection levels ensure consistent safety across platforms.

### 1.4 Vulnerability Detection Indicators

The core vulnerability signals must be monitored.

**Cannot be delegated:**
- Crisis language detection
- Financial desperation signals
- Health crisis indicators
- Isolation indicators

**Why:** These are empirically validated signals that predict user vulnerability.

---

## 2. Delegable Implementation Details

These aspects can and should be customized by integrators based on their platform, user base, and technical constraints:

### 2.1 Platform-Specific Integration

**Can be delegated:**
- How the LFAS layer integrates with the underlying AI model (pre-processing, post-processing, middleware)
- The technical architecture (API wrappers, prompt engineering, fine-tuning)
- Programming language and framework choices
- Deployment infrastructure (cloud, on-premise, edge)

**Constraints:**
- Must still implement all five stages
- Must apply all verification requirements
- Must achieve equivalent safety outcomes

### 2.2 User Interface & Experience

**Can be delegated:**
- How the "WAIT" phase is presented to users (delay, explicit confirmation prompt, visual indicator)
- The visual design of crisis resources
- The wording and tone of disclaimers (as long as they meet VR requirements)
- The format of acknowledgment messages

**Constraints:**
- Must not hide or obscure safety warnings
- Must make crisis resources easily accessible
- Must maintain transparency about AI limitations

### 2.3 Language and Cultural Adaptation

**Can be delegated:**
- Translation of vulnerability indicators to other languages
- Cultural adaptation of crisis resources
- Regional crisis hotline numbers and resources
- Culturally appropriate phrasing for safety messages

**Constraints:**
- Must maintain equivalent semantic meaning
- Must preserve the safety intent of each safeguard
- Must consult with local mental health and crisis experts

### 2.4 Lexicon and Keyword Tuning

**Can be delegated:**
- Adding platform-specific vulnerability indicators
- Expanding the keyword lexicon for better detection
- Adjusting keyword sensitivity based on false positive/negative rates
- Domain-specific indicator additions (e.g., for healthcare AI, financial AI)

**Constraints:**
- Cannot remove the core indicators defined in the protocol
- Cannot weaken the detection threshold to reduce false positives at the expense of safety
- Must document any additions or modifications

### 2.5 Testing and Validation Strategies

**Can be delegated:**
- The specific test cases and scenarios
- The testing framework and tools
- Performance benchmarks and metrics
- Continuous monitoring and alerting systems

**Constraints:**
- Must validate that all five stages execute correctly
- Must test all protection levels
- Must verify that all VRs are applied
- Must include the test scenarios from `/demonstrations/`

### 2.6 Response Wording and Tone

**Can be delegated:**
- The specific language used in AI responses (as long as VR requirements are met)
- The tone and personality of the AI (professional, casual, empathetic)
- The length and verbosity of responses
- The use of examples, analogies, or explanations

**Constraints:**
- Must not use forbidden language (e.g., "guaranteed success," "easy money")
- Must include required disclaimers and warnings
- Must maintain honesty and realism over false optimism

### 2.7 Logging and Analytics

**Can be delegated:**
- What data is logged (conversation metadata, vulnerability triggers, protection level changes)
- How logs are stored and analyzed
- Privacy and anonymization strategies
- Reporting and dashboard design

**Constraints:**
- Must respect user privacy and data protection laws
- Must not log sensitive personal information unnecessarily
- Should track safety intervention effectiveness

---

## 3. Decision Framework for Integrators

When deciding whether a modification is acceptable, ask:

1. **Does this change weaken user protection?** → If yes, **not delegable**.
2. **Does this skip or alter the five-stage loop?** → If yes, **not delegable**.
3. **Does this remove a verification requirement?** → If yes, **not delegable**.
4. **Does this lower the sensitivity of vulnerability detection?** → If yes, **not delegable**.
5. **Is this a technical, UI, or language adaptation that maintains equivalent safety?** → If yes, **delegable with constraints**.

---

## 4. Governance and Compliance

### 4.1 Who Approves Delegated Changes?

**For non-delegable components:**
- No modifications are permitted without explicit approval from the LFAS Protocol creator.
- Commercial licensees must adhere to the specification as-is.
- For governance inquiries, contact: lfasprotocol@outlook.com

**For delegable components:**
- Integrators have full autonomy within the documented constraints.
- Recommended: Share significant modifications with the community for peer review.

### 4.2 Verification of Compliance

Integrators should:
1. Document all delegated decisions and modifications.
2. Test against the protocol's reference test suite.
3. Validate that all five stages execute in every interaction.
4. Confirm that all VRs are applied at the correct protection levels.

### 4.3 Community Contributions

If an integrator discovers:
- A new vulnerability indicator that should be added to the core protocol
- A missing VR or safeguard that improves safety
- An ambiguity or gap in the specification

**Action:** Submit a Pull Request or issue to the LFAS Protocol repository for community review and potential inclusion in future versions.

---

## 5. Examples of Delegation in Practice

### Example 1: Healthcare AI Integration (Delegable)

**Scenario:** A hospital wants to integrate LFAS into a patient-facing AI.

**Delegable decisions:**
- Add healthcare-specific vulnerability indicators (e.g., "can't afford treatment")
- Customize crisis resources to include hospital social workers and patient advocates
- Translate the protocol to the primary language of the patient population
- Integrate with the hospital's existing escalation protocols

**Non-delegable requirements:**
- Must still implement the five-stage loop
- Must apply VR-24 (Crisis Detection) for suicidal ideation
- Must escalate to Level 3 protection for crisis situations

### Example 2: Financial Planning AI (Delegable)

**Scenario:** A fintech company wants to use LFAS in their AI-powered financial advisor.

**Delegable decisions:**
- Expand VR-23 disclaimers to include investment-specific risks
- Add financial-specific vulnerability indicators (e.g., "facing bankruptcy")
- Customize the "WAIT" phase to require explicit confirmation before investment advice
- Design a UI that highlights risk disclosures prominently

**Non-delegable requirements:**
- Must apply VR-23 (Financial Realism Verification) for all financial advice
- Must detect financial desperation signals
- Cannot use forbidden language like "guaranteed returns" or "easy money"

### Example 3: Open-Source Chatbot (Delegable)

**Scenario:** A developer wants to add LFAS to their open-source chatbot framework.

**Delegable decisions:**
- Implement LFAS as a middleware module in their preferred language (Python, JavaScript, etc.)
- Allow users to configure which crisis resources to display based on their region
- Provide a configuration file for customizing the keyword lexicon
- Design a logging system that respects user privacy

**Non-delegable requirements:**
- The middleware must enforce the five-stage loop
- All VRs must be configurable "on" but not "off"
- Protection level escalation must follow the protocol's rules
- Must include the core vulnerability detection indicators

---

## 6. Summary Table

| Component | Delegable? | Key Constraints |
|-----------|-----------|-----------------|
| Five-stage loop (LISTEN → REFLECT → WAIT → ACT → ACKNOWLEDGE) | ❌ No | Must execute all stages in order |
| Verification Requirements (VR-20 to VR-25) | ❌ No | Must apply all VRs at appropriate protection levels |
| Protection level thresholds | ❌ No | Must use 0, 1-2, 3+ trigger escalation rules |
| Core vulnerability indicators | ❌ No | Must monitor all defined indicators |
| Platform integration method | ✅ Yes | Must achieve equivalent safety outcomes |
| User interface design | ✅ Yes | Must not hide safety warnings |
| Language and cultural adaptation | ✅ Yes | Must preserve safety intent and semantic meaning |
| Additional vulnerability indicators | ✅ Yes | Cannot remove core indicators |
| Testing strategies | ✅ Yes | Must validate all stages and VRs |
| Response wording and tone | ✅ Yes | Must meet VR requirements and avoid forbidden language |
| Logging and analytics | ✅ Yes | Must respect privacy and data protection laws |

---

## 7. Contact and Support

**Questions about delegation?**
- Email: lfasprotocol@outlook.com
- Submit an issue on GitHub: [LFAS Protocol v4 Repository](https://github.com/LFASProtocol/LFAS-protocol-v4)

**Commercial licensing inquiries:**
- For healthcare, government, or enterprise implementations requiring custom delegation guidance, contact lfasprotocol@outlook.com for a commercial license.

---

*"Delegation enables adaptation, but the core safety guarantees must never be compromised." - LFAS Protocol v4*
