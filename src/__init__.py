"""
VAPT Automation Engine - Penetration Testing Automation Framework

A professional-grade penetration testing automation engine supporting both
Network VAPT (nVAPT) and Application VAPT (AVAPT) with integrated tool
orchestration, compliance framework mapping, and enterprise-ready reporting.

Version: 1.0.0
Author: Alvin Seah
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Alvin Seah"
__license__ = "MIT"

from src.logger import get_logger

logger = get_logger(__name__)
