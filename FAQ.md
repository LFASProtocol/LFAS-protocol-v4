# Frequently Asked Questions (FAQ)

## General Questions

### What is LFAS Protocol?

LFAS (Logical Framework for AI Safety) Protocol v4 is a safety framework designed to protect vulnerable users when interacting with AI systems. It detects vulnerability signals in user input and applies appropriate safeguards to prevent harm.

### Who should use LFAS Protocol?

LFAS Protocol is designed for:
- AI application developers integrating chatbots or virtual assistants
- Mental health platforms using AI
- Educational platforms with AI tutors
- Customer service systems with AI support
- Any AI system that interacts with potentially vulnerable users

### Is LFAS Protocol free to use?

Yes, for **non-commercial use** (personal, academic, research, non-profit). Commercial use requires a separate license. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSING.md](COMMERCIAL_LICENSING.md) for details.

### How does LFAS Protocol differ from other AI safety approaches?

Unlike static content filters, LFAS:
- **Actively listens** for vulnerability signals in conversation
- **Adapts protection levels** based on detected vulnerability
- **Focuses on vulnerable users** rather than general content moderation
- **Prevents false hope** and dangerous amplification loops
- **Based on research** from 4 independent AI research teams

## Technical Questions

### What programming languages does LFAS support?

The reference implementation is in Python 3.8+. The protocol specification (XML) can be implemented in any language. Community contributions for other languages are welcome!

### Can I use LFAS with [ChatGPT/Claude/Gemini/etc]?

Yes! LFAS can be integrated with any AI platform. The protocol can be:
- Added to system prompts
- Implemented as a pre/post-processing layer
- Integrated into your application code

See [implementation-guide.md](implementation-guide.md) for platform-specific guidance.

### What are the system requirements?

**Minimum:**
- Python 3.8 or higher
- 50MB disk space
- Minimal CPU/RAM (protocol is lightweight)

**Recommended:**
- Python 3.10+
- For production: Load balancing for high traffic

### How accurate is vulnerability detection?

The detection engine identifies phrases and patterns associated with vulnerability. Accuracy depends on:
- **Phrase coverage**: The XML spec contains research-validated indicators
- **Context sensitivity**: Some phrases may be false positives
- **Multiple triggers**: Higher trigger counts increase confidence

We recommend:
- Testing with your specific use case
- Monitoring false positive/negative rates
- Customizing indicators for your domain

### Can I customize the vulnerability indicators?

Yes! You can:
1. **Modify the XML specification** to add domain-specific indicators
2. **Adjust protection thresholds** (e.g., require more triggers for crisis level)
3. **Add custom safeguards** for your specific use case

See `protocol/lfas-v4-specification.xml` and the detector implementation.

## Safety and Ethics Questions

### What happens when LFAS detects a crisis?

When crisis-level vulnerability is detected (3+ triggers):
1. Normal AI response is suppressed
2. Crisis resources are provided immediately (suicide hotlines, etc.)
3. User is encouraged to seek human help
4. Safety takes absolute priority over functionality

### Does LFAS replace professional mental health care?

**No.** LFAS is a harm reduction tool, not a replacement for:
- Professional therapy or counseling
- Crisis intervention services
- Medical care
- Emergency services

The protocol always directs high-risk users to appropriate professional resources.

### How does LFAS protect user privacy?

The protocol:
- Processes data locally (no external API calls required)
- Doesn't store user data by default
- Logs only what integrators choose to log
- Includes privacy best practices in documentation

**Integrator responsibility:** You must implement appropriate privacy protections for any data you collect.

### What if LFAS misses a crisis?

LFAS is designed to reduce risk, not eliminate it. The protocol:
- Cannot detect all crisis situations
- May miss context-dependent crises
- Relies on keyword/phrase matching

**Critical safeguard:** Always include general safety resources in responses and encourage users to seek help if needed.

### Can LFAS be bypassed or manipulated?

Like any safety system, LFAS can potentially be bypassed by:
- Adversarial inputs designed to avoid triggers
- Obfuscated language
- Gradual escalation across multiple sessions

**Mitigation:**
- Combine with other safety measures
- Monitor for unusual patterns
- Update indicators based on observed bypasses
- Report bypasses via [SECURITY.md](SECURITY.md)

## Implementation Questions

### How long does it take to integrate LFAS?

**Basic integration:** 1-2 hours
- Install package
- Add detection to input processing
- Apply basic safeguards

**Production integration:** 1-2 weeks
- Custom indicator tuning
- Testing across use cases
- Privacy/security review
- Performance optimization

### Will LFAS slow down my application?

No. The protocol is very lightweight:
- XML parsing: Once at startup
- Detection: Simple string matching (milliseconds)
- No external API calls
- Minimal memory footprint

Performance impact is typically < 1ms per request.

### How do I test my LFAS integration?

1. **Use the test suite:**
   ```bash
   python -m pytest tests/
   ```

2. **Run example scripts:**
   ```bash
   python examples/basic_usage.py
   ```

3. **Test with documented harm scenarios** from `research/`

4. **Create custom test cases** for your domain

See `tests/` directory for examples.

### Can I use LFAS in production?

Yes, v4 is marked as "Implementation Ready." However:
- Test thoroughly with your specific use case
- Monitor for false positives/negatives
- Have escalation procedures for edge cases
- Consider commercial licensing if applicable
- Follow security best practices

### How do I update LFAS Protocol?

```bash
pip install --upgrade lfas-protocol
```

Always review release notes for:
- Breaking changes
- New safety features
- Updated indicators
- Security fixes

## Contributing and Community

### How can I contribute?

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code contributions
- Documentation improvements
- Research and evidence
- Bug reports and feature requests

### Where can I get help?

- **GitHub Issues**: Bug reports and feature requests
- **Email**: lfasprotocol@outlook.com
- **Documentation**: README.md, implementation-guide.md

### How do I report a security vulnerability?

See [SECURITY.md](SECURITY.md) for responsible disclosure process. For critical vulnerabilities that could harm users, email lfasprotocol@outlook.com directly.

### Can I add new crisis resources for my region?

Yes! We welcome contributions for:
- International crisis hotlines
- Regional resources
- Language-specific resources

Submit a pull request with updates to `lfas/crisis.py`.

## Licensing Questions

### What license is LFAS under?

LFAS Protocol v4 License (Share-Alike):
- **Free** for non-commercial use
- **Commercial license required** for business use
- **Derivative works** must use same license
- See [LICENSE](LICENSE) for full terms

### Do I need a commercial license?

You need a commercial license if:
- Using in a for-profit company
- Integrating into a paid product/service
- Using for internal business operations
- Government or healthcare use (unless exempted)

Contact: lfasprotocol@outlook.com

### Can I use LFAS in open source projects?

Yes! Open source projects can use LFAS under the non-commercial license. If your project becomes commercial, you'll need to obtain a commercial license.

### What if I modify LFAS Protocol?

Modifications and derivative works:
- Must be released under the same LFAS Protocol v4 License
- Must maintain attribution
- Can be contributed back to the project
- Share-Alike requirement applies

---

## Still have questions?

Contact us at **lfasprotocol@outlook.com** or [open an issue](https://github.com/LFASProtocol/LFAS-protocol-v4/issues/new).
