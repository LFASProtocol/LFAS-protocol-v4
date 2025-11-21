"""
Test utilities and helpers for LFAS Protocol tests
"""

import os
from pathlib import Path


def get_spec_path() -> str:
    """
    Get the path to the LFAS specification file.
    
    This function resolves the path dynamically based on the test file location,
    making tests more portable across different environments.
    
    Returns:
        str: Absolute path to the specification file
    """
    # Get the directory containing this file (tests/)
    test_dir = Path(__file__).parent
    
    # Go up one level to project root, then into protocol/
    spec_path = test_dir.parent / "protocol" / "lfas-v4-specification.xml"
    
    if not spec_path.exists():
        raise FileNotFoundError(
            f"LFAS specification not found at {spec_path}. "
            "Ensure you're running tests from the project root."
        )
    
    return str(spec_path)
