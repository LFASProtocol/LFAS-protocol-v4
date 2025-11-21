# Contributing to LFAS Protocol

Thank you for your interest in contributing to the LFAS Protocol v4! This project aims to protect vulnerable users in AI systems, and your contributions can make a real difference.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Ways to Contribute

- **Protocol Improvements:** Review safeguards and suggest enhancements
- **Research & Evidence:** Contribute new research on AI safety
- **Implementation Help:** Develop reference implementations
- **Documentation:** Improve guides and translations
- **Bug Reports:** Help us identify and fix issues
- **Code Quality:** Improve tests, types, or performance

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Familiarity with AI safety concepts

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/LFAS-protocol-v4.git
   cd LFAS-protocol-v4
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   make install-dev
   # or manually:
   pip install -e .
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks**
   ```bash
   make pre-commit-install
   # or manually:
   pip install pre-commit
   pre-commit install
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clear, maintainable code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Run Quality Checks

Before committing, ensure all checks pass:

```bash
# Format code
make format

# Run all quality checks
make quality

# Or run individual checks:
make test          # Run tests
make lint          # Run linters
make type-check    # Run type checking
make test-cov      # Run tests with coverage
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

**Commit Message Guidelines:**
- Use conventional commit format: `type: description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Keep messages clear and concise

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] Linters pass (`make lint`)
- [ ] Type checking passes (`make type-check`)
- [ ] Coverage is maintained or improved
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated

### PR Description Should Include

- Clear description of the changes
- Motivation for the changes
- Any breaking changes
- Related issue numbers (if applicable)

### Review Process

1. Automated checks will run (CI)
2. Maintainers will review your code
3. Address any feedback
4. Once approved, your PR will be merged

## Code Style Guidelines

### Python Code Style

- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use isort for import sorting
- Use type hints where appropriate
- Write docstrings for public APIs

### Example:

```python
from typing import List, Optional

def detect_vulnerability(
    user_input: str,
    history: Optional[List[str]] = None
) -> DetectionResult:
    """
    Analyze user input for vulnerability indicators.

    Args:
        user_input: Current user message to analyze
        history: Optional conversation history

    Returns:
        DetectionResult with protection level and triggers
    """
    # Implementation here
    pass
```

### Testing Guidelines

- Write tests for all new features
- Maintain test coverage above 95%
- Use descriptive test names
- Test edge cases and error conditions

```python
class TestVulnerabilityDetector:
    """Test vulnerability detection functionality"""

    def test_detect_crisis_protection(self):
        """Should escalate to crisis level with 3+ triggers"""
        detector = VulnerabilityDetector()
        result = detector.detect("lost job, last hope, can't take it")

        assert result.protection_level == ProtectionLevel.CRISIS
        assert result.triggers_count >= 3
```

## Reporting Issues

### Bug Reports

Include:
- Clear problem description
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error messages/stack traces

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered
- Impact on existing functionality

### Security Issues

**Do not** report security vulnerabilities in public issues. Instead, email:
**lfasprotocol@outlook.com**

## Documentation

- Keep documentation up to date
- Use clear, simple language
- Include code examples
- Update CHANGELOG.md for user-facing changes

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (LFAS Protocol v4 License).

## Questions?

- Email: lfasprotocol@outlook.com
- GitHub Issues: For general questions and discussions

## Recognition

Contributors will be acknowledged in:
- CHANGELOG.md for significant contributions
- GitHub contributors page
- Project documentation (for major contributions)

Thank you for contributing to LFAS Protocol v4! 🙏
