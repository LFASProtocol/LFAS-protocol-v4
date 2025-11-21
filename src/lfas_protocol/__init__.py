"""
LFAS Protocol v4
Logical Framework for AI Safety - Protecting Vulnerable Users

This package provides tools for detecting user vulnerability in AI interactions
and applying appropriate safety safeguards.
"""

from .detector import VulnerabilityDetector, ProtectionLevel
from .safeguards import SafeguardEngine
from .parser import SpecificationParser

__version__ = "4.0.0"
__author__ = "Mehmet"
__email__ = "lfasprotocol@outlook.com"

__all__ = [
    "VulnerabilityDetector",
    "ProtectionLevel",
    "SafeguardEngine",
    "SpecificationParser",
]
