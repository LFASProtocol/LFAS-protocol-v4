"""
LFAS Protocol v4 - Logical Framework for AI Safety
"""

from .detector import VulnerabilityDetector
from .crisis import CrisisDetector
from .models import DetectionResult, ProtectionLevel

__version__ = "4.0.0"
__author__ = "Mehmet Bagbozan"
__email__ = "lfasprotocol@outlook.com"

__all__ = [
    "VulnerabilityDetector",
    "CrisisDetector", 
    "DetectionResult",
    "ProtectionLevel"
]
