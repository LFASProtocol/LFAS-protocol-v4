"""
LFAS Protocol v4 - Logical Framework for AI Safety
"""

from .crisis import CrisisDetector
from .detector import VulnerabilityDetector
from .models import CrisisResource, CrisisResult, CrisisType, DetectionResult, ProtectionLevel
from .specification_loader import SpecificationLoader

__version__ = "4.0.0"
__author__ = "Mehmet Bagbozan"
__email__ = "lfasprotocol@outlook.com"

__all__ = [
    "VulnerabilityDetector",
    "CrisisDetector",
    "DetectionResult",
    "ProtectionLevel",
    "CrisisType",
    "CrisisResult",
    "CrisisResource",
    "SpecificationLoader",
]
