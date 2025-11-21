"""
LFAS Protocol v4 - Python Reference Implementation

A reference implementation of the LFAS (Logical Framework for AI Safety) Protocol v4.
This library provides tools for detecting user vulnerability and applying appropriate
safety safeguards in AI interactions.

Key Components:
- VulnerabilityDetector: Detects vulnerability indicators in user input
- ProtectionLevel: Determines appropriate protection level (1, 2, or 3)
- Safeguards: Implements VR-20 through VR-25 verification requirements

For more information, see: https://github.com/LFASProtocol/LFAS-protocol-v4
"""

__version__ = "0.1.0"
__author__ = "Mehmet"
__email__ = "lfasprotocol@outlook.com"

from .detector import ProtectionLevel, VulnerabilityDetector
from .spec_loader import SpecificationLoader

__all__ = [
    "VulnerabilityDetector",
    "ProtectionLevel",
    "SpecificationLoader",
]
