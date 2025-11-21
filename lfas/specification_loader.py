"""
LFAS Protocol v4 - Specification Loader
Dynamically parses XML specification to extract detection indicators and crisis resources
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any
from pathlib import Path


class SpecificationLoader:
    """Loads and parses LFAS XML specification for dynamic detection"""
    
    def __init__(self, spec_path: Optional[str] = None):
        """
        Initialize specification loader
        
        Args:
            spec_path: Path to XML specification file. If None, uses default location.
        """
        if spec_path is None:
            # Default to protocol directory relative to this file
            base_dir = Path(__file__).parent.parent
            spec_path = base_dir / "protocol" / "lfas-v4-specification.xml"
        
        self.spec_path = Path(spec_path)
        if not self.spec_path.exists():
            raise FileNotFoundError(f"Specification file not found: {self.spec_path}")
        
        self.tree = ET.parse(str(self.spec_path))
        self.root = self.tree.getroot()
    
    def load_vulnerability_indicators(self) -> Dict[str, List[str]]:
        """
        Extract vulnerability detection indicators from XML spec
        
        Returns:
            Dictionary mapping category names to lists of indicator phrases
        """
        indicators = {}
        
        # Find the vulnerability detection engine section
        detection_engine = self.root.find(".//vulnerability_detection_engine")
        if detection_engine is None:
            return indicators
        
        # Find detection_indicators section
        detection_indicators = detection_engine.find("detection_indicators")
        if detection_indicators is None:
            return indicators
        
        # Parse each category
        for category in detection_indicators:
            category_name = category.tag
            category_indicators = []
            
            for indicator_elem in category.findall("indicator"):
                if indicator_elem.text:
                    # Split comma-separated indicators
                    phrases = [phrase.strip() for phrase in indicator_elem.text.split(',')]
                    category_indicators.extend(phrases)
            
            if category_indicators:
                indicators[category_name] = category_indicators
        
        return indicators
    
    def load_protection_escalation_rules(self) -> Dict[str, Any]:
        """
        Extract protection level escalation rules from XML spec
        
        Returns:
            Dictionary with escalation thresholds
        """
        rules = {
            'standard_max': 0,      # 0 triggers → Standard
            'enhanced_min': 1,      # 1-2 triggers → Enhanced
            'enhanced_max': 2,
            'crisis_min': 3,        # 3+ triggers → Crisis
            'deescalation_exchanges': 3  # Clear for 3+ exchanges → Standard
        }
        
        # Could parse from XML if rules become more complex
        escalation = self.root.find(".//protection_escalation_rules")
        if escalation is not None:
            # For now, use hardcoded defaults based on spec
            pass
        
        return rules
    
    def load_crisis_indicators(self) -> Dict[str, List[str]]:
        """
        Extract crisis-specific indicators from VR-24
        
        Returns:
            Dictionary mapping crisis types to indicator phrases
        """
        crisis_indicators = {}
        
        # Find VR-24 (Crisis Detection & Response)
        vr24 = self.root.find(".//VR-24")
        if vr24 is None:
            return crisis_indicators
        
        detection_indicators = vr24.find("detection_indicators")
        if detection_indicators is None:
            return crisis_indicators
        
        # Map indicator descriptions to crisis types
        crisis_mapping = {
            'suicidal ideation or self-harm': 'mental_health',
            'immediate financial crisis': 'financial',
            'health emergency': 'health',
            'domestic violence or abuse': 'abuse'
        }
        
        for indicator_elem in detection_indicators.findall("indicator"):
            if indicator_elem.text:
                text = indicator_elem.text.lower()
                for key_phrase, crisis_type in crisis_mapping.items():
                    if key_phrase in text:
                        if crisis_type not in crisis_indicators:
                            crisis_indicators[crisis_type] = []
                        crisis_indicators[crisis_type].append(indicator_elem.text)
        
        return crisis_indicators
    
    def load_crisis_resources(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract crisis resources from specification
        
        Returns:
            Dictionary mapping crisis types to resource lists
        """
        # Default crisis resources based on VR-24 requirements
        resources = {
            'mental_health': [
                {
                    'name': '988 Suicide & Crisis Lifeline',
                    'contact': '988 (call or text)',
                    'description': '24/7 free and confidential support for people in distress',
                    'available_247': True
                },
                {
                    'name': 'Crisis Text Line',
                    'contact': 'Text HOME to 741741',
                    'description': 'Free 24/7 crisis support via text message',
                    'available_247': True
                }
            ],
            'financial': [
                {
                    'name': 'National Debt Helpline',
                    'contact': '1-800-388-2227',
                    'description': 'Free financial counseling and debt assistance',
                    'available_247': False
                },
                {
                    'name': '211 Community Resources',
                    'contact': 'Call or text 211',
                    'description': 'Connect to local resources for food, housing, and financial assistance',
                    'available_247': True
                }
            ],
            'health': [
                {
                    'name': 'Emergency Services',
                    'contact': '911',
                    'description': 'For immediate medical emergencies',
                    'available_247': True
                },
                {
                    'name': 'Health Resources & Services',
                    'contact': '1-877-464-4772',
                    'description': 'Find local health centers and medical assistance',
                    'available_247': False
                }
            ],
            'abuse': [
                {
                    'name': 'National Domestic Violence Hotline',
                    'contact': '1-800-799-7233',
                    'description': '24/7 confidential support for domestic violence survivors',
                    'available_247': True
                },
                {
                    'name': 'National Sexual Assault Hotline',
                    'contact': '1-800-656-4673',
                    'description': '24/7 confidential support for sexual assault survivors',
                    'available_247': True
                }
            ]
        }
        
        # Could be extended to parse from XML if resources are added to spec
        return resources
    
    def get_metadata(self) -> Dict[str, str]:
        """
        Extract protocol metadata
        
        Returns:
            Dictionary with version, creator, status, etc.
        """
        metadata = {}
        meta_elem = self.root.find("metadata")
        
        if meta_elem is not None:
            for child in meta_elem:
                if child.text:
                    metadata[child.tag] = child.text.strip()
        
        return metadata
