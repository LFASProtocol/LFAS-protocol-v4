# Changelog
All notable changes to the LFAS Protocol v4 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2025-11-21

### Added
- Comprehensive test scenarios document (`documentation/test-scenarios.md`)
  - 15 detailed test scenarios covering all protection levels
  - Financial crisis, mental health, health crisis, and amplification scenarios
  - Validation criteria and success metrics for implementations
  
- Testing and validation guide (`documentation/testing-guide.md`)
  - Unit, integration, scenario, and user acceptance testing methodologies
  - Test execution process with code examples
  - Quality metrics and certification levels
  - Platform-specific testing considerations
  
- Public release checklist (`documentation/public-release-checklist.md`)
  - Comprehensive preparation checklist across 11 categories
  - Documentation, legal, quality, and community requirements
  - Critical path to public release
  - Ongoing maintenance guidelines
  
- NHS and health funding research (`research/nhs-health-funding-opportunities.md`)
  - NHS England AI Lab and Innovation Accelerator opportunities
  - NIHR AI for Health and Care Awards
  - Wellcome Trust and Health Foundation grants
  - Application strategy with priority rankings
  - Budget considerations and immediate action items

### Changed
- Fixed GitHub Actions workflow naming
  - Renamed workflows to use proper .yml extension
  - Changed from spaces to hyphens: `ci.yml`, `documentation-check.yml`, `license-check.yml`
  
- Consolidated protocol specification files
  - Removed duplicate XML files (kept `lfas-v4-specification.xml` as canonical version)
  - All four previously existing files were identical

### Removed
- Duplicate protocol specification files:
  - `lfas-v4-complete-specification.xml` (duplicate)
  - `lfas-v4-specifications.xml` (duplicate)
  - `lfas-v4-specificationss.xml` (duplicate)
  
- Placeholder file `research/p` (empty file)

### Fixed
- Repository structure cleanup for public release readiness
- GitHub Actions workflow file naming conventions

## [4.0.0-beta] - 2025-11

### Added
- Initial LFAS Protocol v4 specification
- Core documentation:
  - `README.md` with protocol overview
  - `LICENSE` with LFAS Protocol v4 License
  - `CONTRIBUTING.md` with contribution guidelines
  - `COMMERCIAL_LICENSING.md` with commercial terms
  - `implementation-guide.md` with step-by-step integration instructions
  
- Protocol specification (`protocol/lfas-v4-specification.xml`)
  - Five-phase interaction loop: LISTEN → REFLECT → WAIT → ACT → ACKNOWLEDGE
  - Vulnerability detection engine with crisis, financial, health, and isolation indicators
  - Protection level escalation system (Standard/Enhanced/Crisis)
  - Verification Requirements VR-20 through VR-25
  - Cross-platform implementation guidance
  
- Research evidence base:
  - `research/complete-research-compilation.md` - Four independent AI research studies
  - `research/claude-validation.md` - External validation
  
- Documentation:
  - `documentation/reality-gap-analysis.md` - Current AI safety system failures
  - `documentation/white-paper-outline.md` - White paper structure
  
- Demonstrations:
  - `demonstrations/lfas-basic-demo.md` - Financial and mental health crisis scenarios
  
- GitHub Actions workflows:
  - CI workflow for testing and linting
  - Documentation disclaimer check
  - License compliance check

### Core Features
- **Protection Levels**: Three-tier escalation system (Level 1: Standard, Level 2: Enhanced, Level 3: Crisis)
- **Vulnerability Detection**: Automated detection of crisis language, financial desperation, health emergencies, and isolation signals
- **Critical Safeguards**:
  - VR-20: Unfounded Optimism Prevention
  - VR-22: Realistic Capability Assessment
  - VR-23: Financial Realism Verification
  - VR-24: Crisis Detection & Response
  - VR-25: Vulnerable User Amplification Prevention
- **Cross-Platform Support**: Implementation guidance for ChatGPT, Gemini, Claude, and Grok

---

## Version Numbering

LFAS Protocol follows semantic versioning:
- **Major version (4.x.x)**: Core protocol architecture changes
- **Minor version (x.0.x)**: New safeguards, significant feature additions
- **Patch version (x.x.0)**: Bug fixes, documentation updates, clarifications

---

## Important Safety Disclaimer

**Not a Medical Device:** The LFAS Protocol is an algorithmic framework designed to improve AI logic. It is **not** a medical device, a substitute for professional mental health care, or an emergency response system.

**No Guarantee of Prevention:** While LFAS v4 includes safeguards (VR-20 through VR-25) designed to mitigate risk, the Creator **cannot and does not guarantee** that the Protocol will prevent all instances of self-harm, financial loss, or delusion.

---

[4.0.0]: https://github.com/LFASProtocol/LFAS-protocol-v4/releases/tag/v4.0.0
