# Changelog

All notable changes to the LFAS Protocol v4 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Code quality improvements with Black formatter
- Type checking with mypy
- Requirements files for dependency management
- Development requirements for code quality tools

### Fixed
- Fixed type annotations in specification_loader.py
- Fixed whitespace issues across all Python files

## [4.0.0] - 2025-11

### Added
- Initial release of LFAS Protocol v4
- VulnerabilityDetector for analyzing user input
- CrisisDetector for crisis assessment and resource provision
- SpecificationLoader for dynamic XML-based configuration
- Comprehensive test suite (57 tests, 96% coverage)
- Documentation and examples
- Crisis resources integration (988, Crisis Text Line, etc.)

### Features
- Protection level escalation (Standard, Enhanced, Crisis)
- Conversation history tracking
- Mixed-crisis prioritization
- Mental health prioritization in multi-issue contexts
- Real-world support resources
- User-facing crisis messaging

[Unreleased]: https://github.com/LFASProtocol/LFAS-protocol-v4/compare/v4.0.0...HEAD
[4.0.0]: https://github.com/LFASProtocol/LFAS-protocol-v4/releases/tag/v4.0.0
