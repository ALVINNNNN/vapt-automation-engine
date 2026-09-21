"""
Compliance Framework Mapping Engine

Maps vulnerabilities to compliance requirements across multiple frameworks:
- OWASP Top 10 & Testing Guide
- NIST Cybersecurity Framework
- PCI-DSS
- ISO 27001
"""

import logging
from typing import Dict, List, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ComplianceFramework(Enum):
    """Supported compliance frameworks"""
    OWASP = "owasp"
    NIST = "nist"
    PCI_DSS = "pci_dss"
    ISO_27001 = "iso_27001"


class FrameworkMapper:
    """Maps vulnerabilities to compliance framework requirements"""

    def __init__(self):
        """Initialize framework mapper"""
        self.owasp_mappings = self._init_owasp_mappings()
        self.nist_mappings = self._init_nist_mappings()
        self.pci_dss_mappings = self._init_pci_dss_mappings()
        self.iso27001_mappings = self._init_iso27001_mappings()

    def map_finding(
        self,
        finding_title: str,
        severity: str,
        issue_type: Optional[str] = None,
    ) -> Dict[str, List[str]]:
        """Map a finding to all applicable frameworks"""

        mappings = {
            "owasp": self._map_owasp(finding_title, issue_type),
            "nist": self._map_nist(severity),
            "pci_dss": self._map_pci_dss(finding_title, issue_type),
            "iso_27001": self._map_iso27001(finding_title, severity),
        }

        return mappings

    def _init_owasp_mappings(self) -> Dict[str, List[str]]:
        """OWASP Top 10 2021 mappings"""
        return {
            "injection": ["A03:2021 - Injection"],
            "sql": ["A03:2021 - Injection"],
            "cross_site_scripting": ["A07:2021 - Cross-Site Scripting (XSS)"],
            "xss": ["A07:2021 - Cross-Site Scripting (XSS)"],
            "broken_access_control": ["A01:2021 - Broken Access Control"],
            "authentication": ["A07:2021 - Identification and Authentication Failures"],
            "cryptography": ["A02:2021 - Cryptographic Failures"],
            "insecure_deserialization": ["A08:2021 - Software and Data Integrity Failures"],
            "xxe": ["A05:2021 - XML External Entities (XXE)"],
            "external_entity": ["A05:2021 - XML External Entities (XXE)"],
            "ssrf": ["A10:2021 - Server-Side Request Forgery (SSRF)"],
            "server_side_request_forgery": ["A10:2021 - Server-Side Request Forgery (SSRF)"],
            "weak_cryptography": ["A02:2021 - Cryptographic Failures"],
            "weak_authentication": ["A07:2021 - Identification and Authentication Failures"],
            "default_credentials": ["A07:2021 - Identification and Authentication Failures"],
        }

    def _init_nist_mappings(self) -> Dict[str, str]:
        """NIST CSF mappings"""
        return {
            "critical": "NIST CSF: Critical - Immediate remediation required",
            "high": "NIST CSF: High - Remediate within 30 days",
            "medium": "NIST CSF: Medium - Remediate within 90 days",
            "low": "NIST CSF: Low - Remediate within 1 year",
        }

    def _init_pci_dss_mappings(self) -> Dict[str, List[str]]:
        """PCI-DSS requirement mappings"""
        return {
            "weak_cryptography": ["PCI-DSS 3.2.1 - Strong cryptography"],
            "weak_ssl": ["PCI-DSS 4.1 - Strong cryptography for data in transit"],
            "default_credentials": ["PCI-DSS 2.1 - Change default passwords"],
            "authentication": ["PCI-DSS 6.5.1 - Injection flaws", "PCI-DSS 8 - User access"],
            "authorization": ["PCI-DSS 7.1 - Access control"],
            "information_disclosure": ["PCI-DSS 6.5.1-10 - Vulnerability prevention"],
            "sql_injection": ["PCI-DSS 6.5.1 - Injection flaws"],
            "cross_site_scripting": ["PCI-DSS 6.5.7 - Cross-Site Scripting"],
            "missing_access_control": ["PCI-DSS 7 - Restrict access to cardholder data"],
            "insecure_transport": ["PCI-DSS 4.1 - Use strong cryptography"],
        }

    def _init_iso27001_mappings(self) -> Dict[str, List[str]]:
        """ISO 27001:2013 control mappings"""
        return {
            "authentication": ["A.9.2.1 - User registration and de-registration"],
            "access_control": ["A.9.1 - Access control policy", "A.9.2 - User access management"],
            "cryptography": ["A.10.1 - Cryptographic controls"],
            "vulnerability": ["A.12.6 - Management of technical vulnerabilities"],
            "incident": ["A.13.1 - Incident management"],
            "business_continuity": ["A.17.1 - Information security continuity"],
            "compliance": ["A.18.1 - Compliance with legal requirements"],
        }

    def _map_owasp(self, finding_title: str, issue_type: Optional[str] = None) -> List[str]:
        """Map to OWASP framework"""
        title_lower = finding_title.lower()

        for keyword, categories in self.owasp_mappings.items():
            if keyword in title_lower or (issue_type and keyword in issue_type.lower()):
                return categories

        # Default to OWASP Top 10 2021
        return ["A06:2021 - Vulnerable and Outdated Components"]

    def _map_nist(self, severity: str) -> str:
        """Map to NIST framework"""
        return self.nist_mappings.get(severity.lower(), self.nist_mappings["medium"])

    def _map_pci_dss(self, finding_title: str, issue_type: Optional[str] = None) -> List[str]:
        """Map to PCI-DSS framework"""
        title_lower = finding_title.lower()

        for keyword, requirements in self.pci_dss_mappings.items():
            if keyword in title_lower or (issue_type and keyword in issue_type.lower()):
                return requirements

        # Default PCI-DSS mapping
        return ["PCI-DSS 6.5.1-10 - General vulnerability prevention"]

    def _map_iso27001(self, finding_title: str, severity: str) -> List[str]:
        """Map to ISO 27001 framework"""
        title_lower = finding_title.lower()

        for keyword, controls in self.iso27001_mappings.items():
            if keyword in title_lower:
                return controls

        # Default to vulnerability management
        return ["A.12.6.1 - Evaluation of technical vulnerabilities"]

    def generate_compliance_report(
        self,
        findings: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate compliance report with all framework mappings"""

        report = {
            "framework_coverage": {
                "owasp": set(),
                "nist": set(),
                "pci_dss": set(),
                "iso_27001": set(),
            },
            "findings_by_framework": {
                "owasp": {},
                "nist": {},
                "pci_dss": {},
                "iso_27001": {},
            },
        }

        for finding in findings:
            mappings = self.map_finding(
                finding.get("title", ""),
                finding.get("severity", ""),
                finding.get("issue_type"),
            )

            for framework, mapped_items in mappings.items():
                if isinstance(mapped_items, list):
                    for item in mapped_items:
                        report["framework_coverage"][framework].add(item)
                        if item not in report["findings_by_framework"][framework]:
                            report["findings_by_framework"][framework][item] = []
                        report["findings_by_framework"][framework][item].append(
                            finding.get("title", "")
                        )
                else:  # String (NIST)
                    report["framework_coverage"][framework].add(mapped_items)

        # Convert sets to lists for JSON serialization
        report["framework_coverage"] = {
            k: list(v) for k, v in report["framework_coverage"].items()
        }

        return report
