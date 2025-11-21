"""
LFAS Protocol v4 - Python Reference Implementation
Logical Framework for AI Safety

A Python library for implementing AI safety safeguards that protect vulnerable users.
"""

__version__ = "0.1.0"
__author__ = "Mehmet"
__email__ = "lfasprotocol@outlook.com"

from .detector import VulnerabilityDetector, ProtectionLevel
from .safeguards import CrisisDetectionSafeguard

__all__ = [
    "VulnerabilityDetector",
    "ProtectionLevel",
    "CrisisDetectionSafeguard",
]
