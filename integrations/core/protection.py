"""
LFAS Protocol v4 - Protection Level Manager

This module implements the REFLECT phase of the LFAS protocol,
managing protection level escalation based on detected vulnerabilities.
"""

from enum import IntEnum
from typing import Dict, List


class ProtectionLevel(IntEnum):
    """Protection levels as defined in LFAS v4 specification."""
    STANDARD = 1  # 0 triggers
    ENHANCED = 2  # 1-2 triggers
    CRISIS = 3    # 3+ triggers


class ProtectionLevelManager:
    """Manages protection level escalation and de-escalation."""
    
    def __init__(self):
        """Initialize the protection level manager."""
        self.current_level = ProtectionLevel.STANDARD
        self.trigger_history = []
        self.exchanges_since_clear = 0
    
    def determine_level(self, trigger_count: int) -> ProtectionLevel:
        """
        Determine the protection level based on trigger count.
        
        Args:
            trigger_count: Number of vulnerability indicators detected
            
        Returns:
            Appropriate ProtectionLevel
        """
        if trigger_count >= 3:
            return ProtectionLevel.CRISIS
        elif trigger_count >= 1:
            return ProtectionLevel.ENHANCED
        else:
            return ProtectionLevel.STANDARD
    
    def update(self, trigger_count: int) -> ProtectionLevel:
        """
        Update the protection level based on new trigger count.
        
        Args:
            trigger_count: Number of vulnerability indicators detected
            
        Returns:
            Updated ProtectionLevel
        """
        new_level = self.determine_level(trigger_count)
        
        # Track trigger history
        self.trigger_history.append(trigger_count)
        
        # Check for de-escalation (3+ exchanges with no triggers)
        if trigger_count == 0:
            self.exchanges_since_clear += 1
            if self.exchanges_since_clear >= 3:
                new_level = ProtectionLevel.STANDARD
        else:
            self.exchanges_since_clear = 0
        
        self.current_level = new_level
        return new_level
    
    def get_current_level(self) -> ProtectionLevel:
        """
        Get the current protection level.
        
        Returns:
            Current ProtectionLevel
        """
        return self.current_level
    
    def reset(self):
        """Reset the protection level manager to initial state."""
        self.current_level = ProtectionLevel.STANDARD
        self.trigger_history = []
        self.exchanges_since_clear = 0
    
    def get_active_safeguards(self) -> List[str]:
        """
        Get the list of active safeguards for the current protection level.
        
        Returns:
            List of active safeguard names
        """
        safeguards = [
            'VR-20: Unfounded Optimism Prevention',
            'VR-22: Realistic Capability Assessment',
            'VR-23: Financial Realism Verification'
        ]
        
        if self.current_level >= ProtectionLevel.ENHANCED:
            safeguards.extend([
                'Enhanced reality checking',
                'Simplified language requirements',
                'Repeated verification steps',
                'Crisis resource provision'
            ])
        
        if self.current_level >= ProtectionLevel.CRISIS:
            safeguards.extend([
                'VR-24: Crisis Detection & Response',
                'VR-25: Vulnerable User Amplification Prevention',
                'Emergency protocol activation',
                'Human escalation paths',
                'Immediate safety focus only'
            ])
        
        return safeguards
