"""
VAPT Automation Engine - Penetration Testing Automation

A comprehensive platform for nVAPT and AVAPT assessments in regulated environments.
"""

__version__ = "1.0.0"
__author__ = "VAPT Team"
__email__ = "alvinseahsq@gmail.com"

from .core.assessment import Assessment
from .core.scanner import ScannerRegistry, BaseScanner
from .core.reporter import Reporter

__all__ = [
    "Assessment",
    "ScannerRegistry",
    "BaseScanner",
    "Reporter",
    "__version__",
]
