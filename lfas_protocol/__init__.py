"""
LFAS Protocol v4 - Python Reference Implementation
Logical Framework for AI Safety

Protects vulnerable users through:
- Vulnerability detection (LISTEN phase)
- Protection level escalation (REFLECT phase)
- Crisis response safeguards (ACT phase)

Usage:
    from lfas_protocol import VulnerabilityDetector, CrisisDetectionSafeguard

    detector = VulnerabilityDetector()
    safeguard = CrisisDetectionSafeguard()

    # Detect vulnerability
    result = detector.detect("I can't take it anymore")

    # Generate safe response
    if safeguard.should_activate(result):
        response = safeguard.generate_response(result)
        print(response.message)
"""

from .detector import VulnerabilityDetector
from .models import (
    DetectionResult,
    ProtectionLevel,
    SafeguardResponse,
    VulnerabilityCategory,
    VulnerabilityIndicator,
)
from .safeguards import CrisisDetectionSafeguard

__version__ = "4.0.0"
__author__ = "Mehmet (LFAS Protocol)"
__license__ = "LFAS Protocol v4 License"

__all__ = [
    # Models
    "ProtectionLevel",
    "VulnerabilityCategory",
    "VulnerabilityIndicator",
    "DetectionResult",
    "SafeguardResponse",
    # Core classes
    "VulnerabilityDetector",
    "CrisisDetectionSafeguard",
    # Metadata
    "__version__",
    "__author__",
    "__license__",
]
