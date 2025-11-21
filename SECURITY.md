# Security Policy

## Reporting a Vulnerability

The LFAS Protocol is designed to protect vulnerable users. If you discover a security vulnerability that could compromise user safety, please help us address it responsibly.

### For Critical Vulnerabilities

**If the vulnerability could directly harm users** (e.g., bypass of crisis detection, manipulation of safety protections), please report it privately:

📧 **Email:** lfasprotocol@outlook.com  
📋 **Subject:** "SECURITY VULNERABILITY - CONFIDENTIAL"

**Include in your report:**
- Description of the vulnerability
- Steps to reproduce
- Potential impact on user safety
- Suggested fix (if you have one)
- Your contact information

**Response time:** We aim to respond within **48 hours** and provide a fix timeline within **7 days**.

### For Non-Critical Issues

For lower-severity security issues that don't pose immediate danger:
- Open a [Security Vulnerability issue](https://github.com/LFASProtocol/LFAS-protocol-v4/issues/new?template=security_vulnerability.md)
- Mark as "security" label
- We'll review and respond within 5 business days

## What Qualifies as a Security Vulnerability?

### Critical (Report Privately)
- Bypass of crisis detection (VR-24)
- Bypass of vulnerable user protections (VR-25)
- Manipulation of protection levels
- Code injection vulnerabilities
- Data leakage of user vulnerability information
- Denial of service affecting safety features

### Important (Can Report Publicly)
- Dependency vulnerabilities in requirements
- Information disclosure (non-user data)
- Configuration issues
- Documentation errors about security features

### Not Security Vulnerabilities
- Feature requests
- General bugs that don't affect safety
- Performance issues
- Cosmetic issues

## Our Commitment

When you report a vulnerability:

1. **We will not take legal action** against researchers who:
   - Report vulnerabilities in good faith
   - Make a good faith effort to avoid privacy violations and service disruption
   - Do not exploit vulnerabilities beyond what's necessary to demonstrate the issue

2. **We will respond promptly** and work with you to:
   - Understand and validate the issue
   - Develop and test a fix
   - Coordinate disclosure timing

3. **We will credit you** (if desired) in:
   - Security advisories
   - Release notes
   - Acknowledgments documentation

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 4.x     | ✅ Yes             |
| < 4.0   | ❌ No              |

Only the latest v4.x release receives security updates. Please upgrade to the latest version before reporting issues.

## Security Update Process

When we release security updates:

1. **Immediate notification** to users via:
   - GitHub Security Advisory
   - Release notes
   - Email to known integrators

2. **Clear documentation** including:
   - Nature of vulnerability
   - Affected versions
   - Upgrade instructions
   - Mitigation steps if upgrade not immediately possible

3. **Rapid deployment** timeline:
   - Critical: Fix within 7 days
   - High: Fix within 30 days
   - Medium: Fix within 90 days

## Best Practices for Integrators

If you're integrating LFAS Protocol:

### Recommended Security Practices

1. **Keep Updated**
   ```bash
   pip install --upgrade lfas-protocol
   ```

2. **Monitor Dependencies**
   - Regularly check for dependency updates
   - Use tools like `pip-audit` or `safety`

3. **Validate Input**
   - Don't trust external input to detection system
   - Sanitize before processing

4. **Secure Configuration**
   - Don't disable safety features
   - Use appropriate protection levels
   - Log security events

5. **Privacy Protection**
   - Don't store vulnerability detection results longer than necessary
   - Encrypt sensitive logs
   - Follow data minimization principles

### Testing Your Integration

Always test your integration's security:

```python
# Test that crisis detection cannot be bypassed
def test_crisis_detection_not_bypassable():
    detector = VulnerabilityDetector()
    
    # These should all be detected
    crisis_inputs = [
        "I want to end my life",
        "suicide hotline please",
        "thinking about killing myself"
    ]
    
    for test_input in crisis_inputs:
        result = detector.detect(test_input)
        assert result.protection_level.value >= 2, \
            f"Failed to detect crisis in: {test_input}"
```

## Vulnerability Disclosure Timeline

Our typical disclosure process:

1. **Day 0**: Vulnerability reported
2. **Day 0-2**: Initial response and validation
3. **Day 2-7**: Develop and test fix
4. **Day 7**: Release fix (for critical issues)
5. **Day 7+30**: Public disclosure (coordinated with reporter)

For critical vulnerabilities affecting user safety, we may accelerate this timeline.

## Security Research

We welcome security research on LFAS Protocol! When conducting security research:

### In Scope
- ✅ Detection bypass techniques
- ✅ Manipulation of protection levels
- ✅ Code vulnerabilities
- ✅ Dependency issues
- ✅ Configuration weaknesses

### Out of Scope
- ❌ Social engineering
- ❌ Physical attacks
- ❌ Attacks on users' systems
- ❌ Denial of service attacks
- ❌ Third-party services

### Responsible Research
- Use test environments, not production systems
- Don't access, modify, or delete user data
- Don't disrupt service for others
- Report findings promptly
- Allow reasonable time for fixes before disclosure

## Contact

**Security Team:** lfasprotocol@outlook.com  
**PGP Key:** Available upon request  
**Response Time:** 48 hours for critical issues  

---

Thank you for helping keep LFAS Protocol and its users safe! 🛡️
