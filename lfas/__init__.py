"""
LFAS Protocol v4 - Logical Framework for AI Safety
AI-Powered Vulnerability and Crisis Detection System
"""

from .detector import VulnerabilityDetector
from .crisis import CrisisDetector
from .spec_loader import SpecificationLoader
from .models import (
    DetectionResult, 
    ProtectionLevel, 
    CrisisResult, 
    CrisisType,
    CrisisResource
)

__version__ = "4.0.0"
__author__ = "Mehmet Bagbozan"
__email__ = "lfasprotocol@outlook.com"

__all__ = [
    "VulnerabilityDetector",
    "CrisisDetector",
    "SpecificationLoader",
    "DetectionResult",
    "ProtectionLevel",
    "CrisisResult",
    "CrisisType",
    "CrisisResource"
]
