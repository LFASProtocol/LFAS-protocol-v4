"""
LFAS Protocol v4 - Specification Loader
Dynamic XML specification parser for vulnerability detection indicators
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any
from pathlib import Path


class SpecificationLoader:
    """
    Parses LFAS XML specifications to extract detection indicators,
    protection rules, and crisis resources.
    """
    
    def __init__(self, spec_path: Optional[str] = None):
        """
        Initialize the specification loader.
        
        Args:
            spec_path: Path to XML specification file. If None, uses default.
        """
        if spec_path is None:
            # Default to protocol directory relative to this file
            base_path = Path(__file__).parent.parent
            spec_path = base_path / "protocol" / "lfas-v4-specification.xml"
        
        self.spec_path = Path(spec_path)
        self._tree = None
        self._root = None
        self._load_spec()
    
    def _load_spec(self):
        """
        Load and parse the XML specification.
        
        Security Note: This uses standard ElementTree parsing. For production
        environments with untrusted XML sources, consider using defusedxml library
        to prevent XML External Entity (XXE) attacks.
        """
        try:
            self._tree = ET.parse(self.spec_path)
            self._root = self._tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse XML specification: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Specification file not found: {self.spec_path}")
    
    def get_detection_indicators(self) -> Dict[str, List[str]]:
        """
        Extract vulnerability detection indicators from specification.
        
        Returns:
            Dictionary mapping category names to lists of indicator strings
        """
        indicators = {}
        
        # Find the vulnerability detection engine section
        detection_engine = self._root.find(".//vulnerability_detection_engine")
        if detection_engine is None:
            return indicators
        
        # Find detection indicators section
        detection_indicators = detection_engine.find(".//detection_indicators")
        if detection_indicators is None:
            return indicators
        
        # Parse each category
        for category in detection_indicators:
            category_name = category.tag
            category_indicators = []
            
            for indicator_elem in category.findall("indicator"):
                if indicator_elem.text:
                    # Split on comma and strip whitespace
                    parts = [part.strip() for part in indicator_elem.text.split(',')]
                    category_indicators.extend(parts)
            
            if category_indicators:
                indicators[category_name] = category_indicators
        
        return indicators
    
    def get_protection_rules(self) -> Dict[str, str]:
        """
        Extract protection escalation rules from specification.
        
        Returns:
            Dictionary mapping rule descriptions to their conditions
        """
        rules = {}
        
        detection_engine = self._root.find(".//vulnerability_detection_engine")
        if detection_engine is None:
            return rules
        
        escalation_rules = detection_engine.find(".//protection_escalation_rules")
        if escalation_rules is None:
            return rules
        
        for rule_elem in escalation_rules.findall("rule"):
            if rule_elem.text:
                rule_text = rule_elem.text.strip()
                rules[rule_text] = rule_text
        
        return rules
    
    def get_crisis_resources(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Extract crisis support resources from VR-24 specification.
        
        Returns:
            Dictionary mapping crisis types to lists of resource information
        """
        resources = {
            "mental_health": [],
            "financial": [],
            "health": [],
            "abuse": []
        }
        
        # Default crisis resources based on VR-24 requirements
        # These are standard crisis hotlines and resources
        resources["mental_health"] = [
            {
                "name": "988 Suicide & Crisis Lifeline",
                "description": "24/7 crisis support for mental health emergencies",
                "contact": "Call or text 988",
                "availability": "24/7",
                "crisis_type": "mental_health"
            },
            {
                "name": "Crisis Text Line",
                "description": "Free 24/7 text support with trained crisis counselors",
                "contact": "Text HOME to 741741",
                "availability": "24/7",
                "crisis_type": "mental_health"
            }
        ]
        
        resources["financial"] = [
            {
                "name": "National Foundation for Credit Counseling",
                "description": "Free financial counseling and crisis assistance",
                "contact": "1-800-388-2227 or nfcc.org",
                "availability": "Business hours",
                "crisis_type": "financial"
            },
            {
                "name": "211 Community Resources",
                "description": "Local emergency financial assistance and resources",
                "contact": "Dial 211",
                "availability": "24/7",
                "crisis_type": "financial"
            }
        ]
        
        resources["health"] = [
            {
                "name": "Emergency Services",
                "description": "Immediate medical emergency response",
                "contact": "Call 911",
                "availability": "24/7",
                "crisis_type": "health"
            },
            {
                "name": "Health Resources & Services Administration",
                "description": "Find free/low-cost health centers",
                "contact": "findahealthcenter.hrsa.gov",
                "availability": "Always available",
                "crisis_type": "health"
            }
        ]
        
        resources["abuse"] = [
            {
                "name": "National Domestic Violence Hotline",
                "description": "24/7 support for domestic violence situations",
                "contact": "1-800-799-7233 or text START to 88788",
                "availability": "24/7",
                "crisis_type": "abuse"
            },
            {
                "name": "National Sexual Assault Hotline",
                "description": "24/7 confidential support for sexual assault survivors",
                "contact": "1-800-656-4673",
                "availability": "24/7",
                "crisis_type": "abuse"
            }
        ]
        
        return resources
    
    def get_verification_requirements(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract verification requirements (VR-20 through VR-25) from specification.
        
        Returns:
            Dictionary mapping VR codes to their requirements and details
        """
        requirements = {}
        
        vr_section = self._root.find(".//verification_requirements")
        if vr_section is None:
            return requirements
        
        # Parse each VR requirement
        for vr in vr_section:
            vr_code = vr.tag
            vr_data = {
                "name": "",
                "description": "",
                "checks": [],
                "actions": [],
                "indicators": []
            }
            
            # Extract name and description
            name_elem = vr.find("name")
            if name_elem is not None and name_elem.text:
                vr_data["name"] = name_elem.text.strip()
            
            desc_elem = vr.find("description")
            if desc_elem is not None and desc_elem.text:
                vr_data["description"] = desc_elem.text.strip()
            
            # Extract required checks
            checks = vr.find("required_checks")
            if checks is not None:
                vr_data["checks"] = [
                    check.text.strip() for check in checks.findall("check")
                    if check.text
                ]
            
            # Extract required actions
            actions = vr.find("required_actions")
            if actions is not None:
                vr_data["actions"] = [
                    action.text.strip() for action in actions.findall("action")
                    if action.text
                ]
            
            # Extract detection indicators
            indicators = vr.find("detection_indicators")
            if indicators is not None:
                vr_data["indicators"] = [
                    ind.text.strip() for ind in indicators.findall("indicator")
                    if ind.text
                ]
            
            requirements[vr_code] = vr_data
        
        return requirements
    
    def reload(self):
        """Reload the specification from file (useful for dynamic updates)"""
        self._load_spec()
