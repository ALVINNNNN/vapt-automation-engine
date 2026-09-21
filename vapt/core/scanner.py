"""
Scanner Abstraction Layer

Provides unified interface for multiple security scanning tools.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


class ScannerType(Enum):
    """Scanner types"""
    NETWORK = "network"
    WEB_APPLICATION = "web_application"
    SSL_TLS = "ssl_tls"
    EXPLOITATION = "exploitation"


@dataclass
class ScanResult:
    """Standardized scan result"""
    scanner_name: str
    scan_type: ScannerType
    timestamp: str
    targets: List[str]
    vulnerabilities: List[Dict[str, Any]]
    details: Dict[str, Any]
    duration_seconds: float


class BaseScanner(ABC):
    """Abstract base class for all scanners"""

    def __init__(self, name: str, scanner_type: ScannerType):
        """Initialize scanner"""
        self.name = name
        self.scanner_type = scanner_type
        self.config: Dict[str, Any] = {}
        self.is_configured = False

    @abstractmethod
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure scanner with parameters"""
        pass

    @abstractmethod
    def validate_configuration(self) -> bool:
        """Validate that scanner is properly configured"""
        pass

    @abstractmethod
    def execute(self, targets: List[str]) -> ScanResult:
        """Execute scan against targets"""
        pass

    @abstractmethod
    def parse_results(self, raw_output: Any) -> List[Dict[str, Any]]:
        """Parse raw scanner output to standardized format"""
        pass

    def _create_result(
        self,
        targets: List[str],
        vulnerabilities: List[Dict[str, Any]],
        details: Dict[str, Any],
        duration: float,
    ) -> ScanResult:
        """Helper to create standardized result"""
        return ScanResult(
            scanner_name=self.name,
            scan_type=self.scanner_type,
            timestamp=datetime.now().isoformat(),
            targets=targets,
            vulnerabilities=vulnerabilities,
            details=details,
            duration_seconds=duration,
        )


class ScannerRegistry:
    """Registry for managing multiple scanners"""

    def __init__(self):
        """Initialize scanner registry"""
        self.scanners: Dict[str, BaseScanner] = {}
        self.results: Dict[str, List[ScanResult]] = {}

    def register_scanner(self, scanner: BaseScanner) -> None:
        """Register a scanner"""
        if scanner.name in self.scanners:
            logger.warning(f"Scanner {scanner.name} already registered, overwriting")

        self.scanners[scanner.name] = scanner
        logger.info(f"Scanner registered: {scanner.name}")

    def get_scanner(self, name: str) -> Optional[BaseScanner]:
        """Get scanner by name"""
        return self.scanners.get(name)

    def get_scanners_by_type(self, scanner_type: ScannerType) -> List[BaseScanner]:
        """Get all scanners of a specific type"""
        return [
            scanner for scanner in self.scanners.values()
            if scanner.scanner_type == scanner_type
        ]

    def execute_scanner(self, scanner_name: str, targets: List[str]) -> Optional[ScanResult]:
        """Execute a specific scanner"""
        scanner = self.get_scanner(scanner_name)
        if not scanner:
            logger.error(f"Scanner not found: {scanner_name}")
            return None

        if not scanner.validate_configuration():
            logger.error(f"Scanner not properly configured: {scanner_name}")
            return None

        logger.info(f"Executing scanner: {scanner_name}")
        result = scanner.execute(targets)

        if scanner_name not in self.results:
            self.results[scanner_name] = []
        self.results[scanner_name].append(result)

        return result

    def execute_by_type(self, scanner_type: ScannerType, targets: List[str]) -> List[ScanResult]:
        """Execute all scanners of a specific type"""
        scanners = self.get_scanners_by_type(scanner_type)
        results = []

        for scanner in scanners:
            result = self.execute_scanner(scanner.name, targets)
            if result:
                results.append(result)

        return results

    def get_results(self, scanner_name: Optional[str] = None) -> Dict[str, List[ScanResult]]:
        """Get results from scanner(s)"""
        if scanner_name:
            return {scanner_name: self.results.get(scanner_name, [])}
        return self.results

    def get_all_findings(self) -> List[Dict[str, Any]]:
        """Extract all findings from all scan results"""
        findings = []
        for results_list in self.results.values():
            for result in results_list:
                findings.extend(result.vulnerabilities)
        return findings
