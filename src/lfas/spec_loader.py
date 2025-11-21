"""
Specification Loader - Parses LFAS v4 XML Specification

This module provides functionality to load and parse the LFAS v4 XML specification
file to extract vulnerability indicators, safeguards, and protection rules.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class SpecificationLoader:
    """Loads and parses the LFAS v4 XML specification."""

    def __init__(self, spec_path: Optional[Union[Path, str]] = None):
        """
        Initialize the specification loader.

        Args:
            spec_path: Path to the LFAS v4 XML specification file.
                      If None, uses the default location in the repository.
        """
        if spec_path is None:
            # Default to the specification file in the repository
            self.spec_path = (
                Path(__file__).parent.parent.parent / "protocol" / "lfas-v4-specification.xml"
            )
        else:
            self.spec_path = Path(spec_path)

        self.tree: Optional[Any] = None
        self.root: Optional[Any] = None

    def load(self) -> None:
        """Load and parse the XML specification file."""
        if not self.spec_path.exists():
            raise FileNotFoundError(f"Specification file not found: {self.spec_path}")

        tree = ET.parse(self.spec_path)
        self.tree = tree
        self.root = tree.getroot()

    def get_vulnerability_indicators(self) -> Dict[str, List[str]]:
        """
        Extract vulnerability indicators from the specification.

        Returns:
            Dictionary mapping indicator categories to lists of indicator phrases.
            Categories include: crisis_language, financial_desperation, health_crisis,
            isolation_indicators.
        """
        if self.root is None:
            self.load()

        indicators: Dict[str, List[str]] = {
            "crisis_language": [],
            "financial_desperation": [],
            "health_crisis": [],
            "isolation_indicators": [],
        }

        if self.root is None:
            return indicators

        detection_engine = self.root.find(".//vulnerability_detection_engine/detection_indicators")
        if detection_engine is None:
            return indicators

        for category_name, category_list in indicators.items():
            category_elem = detection_engine.find(category_name)
            if category_elem is not None:
                for indicator_elem in category_elem.findall("indicator"):
                    if indicator_elem.text:
                        # Split comma-separated indicators
                        phrases = [phrase.strip() for phrase in indicator_elem.text.split(",")]
                        category_list.extend(phrases)

        return indicators

    def get_protection_escalation_rules(self) -> Dict[str, str]:
        """
        Extract protection level escalation rules from the specification.

        Returns:
            Dictionary of escalation rules.
        """
        if self.root is None:
            self.load()

        rules: Dict[str, str] = {}

        if self.root is None:
            return rules

        escalation_rules = self.root.find(
            ".//vulnerability_detection_engine/protection_escalation_rules"
        )
        if escalation_rules is not None:
            for rule_elem in escalation_rules.findall("rule"):
                if rule_elem.text:
                    rules[rule_elem.text] = rule_elem.text

        return rules

    def get_verification_requirement(self, vr_code: str) -> Optional[Dict[str, Any]]:
        """
        Extract a specific verification requirement (VR-20 through VR-25).

        Args:
            vr_code: The VR code (e.g., "VR-20", "VR-24")

        Returns:
            Dictionary with VR details or None if not found.
        """
        if self.root is None:
            self.load()

        if self.root is None:
            return None

        vr_elem = self.root.find(f".//verification_requirements/{vr_code}")
        if vr_elem is None:
            return None

        vr_data: Dict[str, Any] = {
            "code": vr_code,
            "name": "",
            "description": "",
            "details": {},
        }

        name_elem = vr_elem.find("name")
        if name_elem is not None and name_elem.text:
            vr_data["name"] = name_elem.text

        desc_elem = vr_elem.find("description")
        if desc_elem is not None and desc_elem.text:
            vr_data["description"] = desc_elem.text

        # Extract all other child elements as details
        for child in vr_elem:
            if child.tag not in ["name", "description"]:
                vr_data["details"][child.tag] = child

        return vr_data
