"""
LFAS Protocol v4 - Core Integration Module

This module provides the core LFAS protocol implementation that can be used
across different AI platforms and providers.
"""

from .middleware import LFASMiddleware
from .detector import VulnerabilityDetector
from .protection import ProtectionLevelManager, ProtectionLevel
from .safeguards import SafeguardEngine

__all__ = [
    'LFASMiddleware',
    'VulnerabilityDetector',
    'ProtectionLevelManager',
    'ProtectionLevel',
    'SafeguardEngine',
]

__version__ = '4.0.0'
