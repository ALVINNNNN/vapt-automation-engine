"""
YesWeHack Integration

Fetches and analyzes bug bounty reports from YesWeHack to learn
about real-world vulnerabilities and patterns.
"""

import logging
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import requests
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BugReport:
    """Represents a bug bounty report"""
    id: str
    title: str
    severity: str
    vulnerability_type: str
    description: str
    impact: str
    affected_technology: str
    discovery_method: str
    exploitation_steps: List[str]
    remediation: str
    cve: Optional[str] = None
    cvss_score: Optional[float] = None
    bounty_amount: Optional[int] = None
    source: str = "yeswehack"


class YesWeHackIntegration:
    """
    Integrates with YesWeHack to fetch and analyze bug reports.

    Learns from public bug bounty reports to identify:
    - Common vulnerability patterns
    - Discovery techniques
    - Exploitation methods
    - Impact indicators
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize YesWeHack integration"""
        self.cache_dir = cache_dir or Path("bug_bounty_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.reports: List[BugReport] = []
        self.patterns: Dict[str, Any] = {}

    def fetch_recent_reports(self, limit: int = 100) -> List[BugReport]:
        """
        Fetch recent bug reports from YesWeHack.

        Note: This uses web scraping of public reports.
        For production, use official YesWeHack API if available.
        """
        logger.info(f"Fetching up to {limit} recent reports from YesWeHack...")

        reports = []
        try:
            # Simulated fetch - in production would use actual YesWeHack API
            # or web scraping of their public reports
            reports = self._simulate_fetch_reports(limit)
        except Exception as e:
            logger.error(f"Error fetching YesWeHack reports: {e}")
            # Fall back to cached reports
            reports = self._load_cached_reports()

        self.reports.extend(reports)
        logger.info(f"Loaded {len(reports)} reports")

        return reports

    def _simulate_fetch_reports(self, limit: int) -> List[BugReport]:
        """
        Simulate fetching reports - in production would call YesWeHack API.
        Returns example high-impact vulnerabilities commonly found in bug bounties.
        """
        example_reports = [
            {
                "id": "yh-001",
                "title": "IDOR in User Profile API Allows Access to Any User Data",
                "severity": "high",
                "type": "Insecure Direct Object References (IDOR)",
                "description": "The /api/users/{id} endpoint does not properly validate authorization, allowing users to access any other user's profile information.",
                "impact": "Complete exposure of user personal data, email addresses, phone numbers, and account details.",
                "tech": "Node.js/Express + MongoDB",
                "method": "Endpoint enumeration through API documentation, parameter fuzzing",
                "steps": [
                    "Identify user ID parameter in API requests",
                    "Intercept request to /api/users/{id}",
                    "Change ID to different value",
                    "Observe full user data returned",
                    "Automate to dump all user records"
                ],
                "remediation": "Implement proper authorization checks: verify user owns resource before returning data",
                "cvss": 7.5,
                "cve": None,
                "bounty": 2000
            },
            {
                "id": "yh-002",
                "title": "Authentication Bypass via Weak JWT Implementation",
                "severity": "high",
                "type": "Authentication Bypass",
                "description": "JWT tokens are validated using a weak secret key found in source code, allowing token forgery.",
                "impact": "Complete account takeover of any user, including administrators.",
                "tech": "React + Python Flask",
                "method": "JavaScript code analysis, secret extraction",
                "steps": [
                    "Extract JavaScript files from application",
                    "Search for JWT library imports and secret usage",
                    "Analyze code for hardcoded secrets",
                    "Use jwt.io to decode captured token",
                    "Use identified secret to forge new tokens with admin role"
                ],
                "remediation": "Use strong, randomly generated secrets; store in environment variables; rotate regularly",
                "cvss": 8.1,
                "cve": None,
                "bounty": 3000
            },
            {
                "id": "yh-003",
                "title": "SQL Injection in Search Functionality",
                "severity": "high",
                "type": "SQL Injection",
                "description": "User input in search parameter is directly concatenated into SQL query without sanitization.",
                "impact": "Database breach, extraction of all user data including password hashes.",
                "tech": "PHP + MySQL",
                "method": "Parameter fuzzing, error-based SQL injection",
                "steps": [
                    "Identify search parameter",
                    "Test with SQL injection payload: ' OR '1'='1",
                    "Observe database error revealing SQL structure",
                    "Use UNION-based injection to extract data",
                    "Dump users table with password hashes"
                ],
                "remediation": "Use parameterized queries and prepared statements",
                "cvss": 9.0,
                "cve": None,
                "bounty": 5000
            },
            {
                "id": "yh-004",
                "title": "Privilege Escalation via Client-Side Role Check",
                "severity": "high",
                "type": "Broken Access Control",
                "description": "Admin panel access is checked only in JavaScript on client-side, not enforced server-side.",
                "impact": "Any authenticated user can access admin panel and modify application settings.",
                "tech": "Vue.js + Django",
                "method": "Network inspection, localStorage analysis",
                "steps": [
                    "Intercept network requests as regular user",
                    "Identify admin endpoint: /api/admin/settings",
                    "Access endpoint directly (client-side check doesn't prevent it)",
                    "Observe admin data returned",
                    "Modify application settings as regular user"
                ],
                "remediation": "Enforce authorization checks on server-side for all sensitive endpoints",
                "cvss": 8.2,
                "cve": None,
                "bounty": 2500
            },
            {
                "id": "yh-005",
                "title": "Exposed AWS S3 Bucket with Sensitive Files",
                "severity": "high",
                "type": "Misconfiguration",
                "description": "S3 bucket found in JavaScript is publicly accessible without authentication.",
                "impact": "Exposure of user-uploaded files, database backups, and source code.",
                "tech": "React + AWS S3",
                "method": "JavaScript analysis, S3 bucket enumeration",
                "steps": [
                    "Extract bucket name from JavaScript code",
                    "Test bucket accessibility: https://bucket.s3.amazonaws.com/",
                    "List bucket contents",
                    "Download sensitive files",
                    "Identify database backups and source code"
                ],
                "remediation": "Configure bucket policy to restrict access, use signed URLs for downloads",
                "cvss": 8.6,
                "cve": None,
                "bounty": 4000
            },
            {
                "id": "yh-006",
                "title": "API Rate Limiting Bypass Allows Brute Force Attacks",
                "severity": "medium",
                "type": "Brute Force / Rate Limiting Bypass",
                "description": "Login endpoint lacks rate limiting and accepts rapid successive requests.",
                "impact": "Ability to brute force user passwords, compromising accounts.",
                "tech": "Node.js/Express",
                "method": "Automated request testing, HTTP header analysis",
                "steps": [
                    "Identify login endpoint: POST /api/auth/login",
                    "Send multiple rapid requests with different passwords",
                    "Observe no rate limiting or blocking",
                    "Use password list to brute force accounts",
                    "Successfully gain access with weak passwords"
                ],
                "remediation": "Implement rate limiting, account lockout after failed attempts",
                "cvss": 6.5,
                "cve": None,
                "bounty": 1500
            },
            {
                "id": "yh-007",
                "title": "Reflected XSS in Error Messages",
                "severity": "medium",
                "type": "Cross-Site Scripting (XSS)",
                "description": "User input reflected in error messages without proper encoding.",
                "impact": "Session hijacking, credential theft, malware distribution.",
                "tech": "Express + EJS Templates",
                "method": "Parameter injection, browser console testing",
                "steps": [
                    "Identify error parameter: ?error=invalid_input",
                    "Inject payload: <img src=x onerror=alert('XSS')>",
                    "Observe alert execution",
                    "Craft cookie-stealing payload",
                    "Steal admin session tokens"
                ],
                "remediation": "HTML-encode all user input before rendering; use Content Security Policy",
                "cvss": 6.1,
                "cve": None,
                "bounty": 1000
            },
            {
                "id": "yh-008",
                "title": "Information Disclosure via Verbose Error Messages",
                "severity": "medium",
                "type": "Information Disclosure",
                "description": "Stack traces and database errors exposed in production error pages.",
                "impact": "Reveals system architecture, database structure, and potential attack vectors.",
                "tech": "Django + PostgreSQL",
                "method": "Trigger errors through invalid input",
                "steps": [
                    "Cause error by sending invalid data type",
                    "Observe detailed stack trace",
                    "Identify database table names and structure",
                    "Identify framework version and vulnerabilities",
                    "Use information for targeted attacks"
                ],
                "remediation": "Show generic errors to users; log detailed errors server-side only",
                "cvss": 5.3,
                "cve": None,
                "bounty": 800
            },
            {
                "id": "yh-009",
                "title": "CORS Misconfiguration Allows Credential Theft",
                "severity": "high",
                "type": "Cross-Origin Resource Sharing (CORS)",
                "description": "CORS allows wildcard origin with credentials, enabling cross-origin requests.",
                "impact": "Attackers can make authenticated requests on behalf of users.",
                "tech": "Express + Vue.js",
                "method": "Network inspection, CORS header analysis",
                "steps": [
                    "Capture API response and check CORS headers",
                    "Observe: Access-Control-Allow-Origin: *",
                    "Observe: Access-Control-Allow-Credentials: true",
                    "Create malicious page that makes API requests",
                    "Access user data when they visit malicious page"
                ],
                "remediation": "Restrict CORS to specific trusted origins; never use wildcard with credentials",
                "cvss": 8.0,
                "cve": None,
                "bounty": 3000
            },
            {
                "id": "yh-010",
                "title": "Insecure API Key Storage in Client Code",
                "severity": "high",
                "type": "Sensitive Data Exposure",
                "description": "Third-party API key exposed in JavaScript code.",
                "impact": "Unauthorized access to third-party services, potential account takeover.",
                "tech": "React",
                "method": "JavaScript source code analysis",
                "steps": [
                    "Extract JavaScript bundles",
                    "Search for API patterns: 'api_key=', 'sk-', 'Bearer '",
                    "Find hardcoded AWS key, Stripe key, etc.",
                    "Use key to access third-party API",
                    "Retrieve sensitive data or perform unauthorized actions"
                ],
                "remediation": "Never store secrets in client code; use backend proxy for API calls",
                "cvss": 7.5,
                "cve": None,
                "bounty": 2000
            }
        ]

        reports = []
        for data in example_reports[:limit]:
            report = BugReport(
                id=data["id"],
                title=data["title"],
                severity=data["severity"],
                vulnerability_type=data["type"],
                description=data["description"],
                impact=data["impact"],
                affected_technology=data["tech"],
                discovery_method=data["method"],
                exploitation_steps=data["steps"],
                remediation=data["remediation"],
                cve=data.get("cve"),
                cvss_score=data.get("cvss"),
                bounty_amount=data.get("bounty"),
            )
            reports.append(report)

        return reports

    def _load_cached_reports(self) -> List[BugReport]:
        """Load cached reports from local storage"""
        cache_file = self.cache_dir / "reports_cache.json"

        if cache_file.exists():
            with open(cache_file) as f:
                data = json.load(f)
                return [BugReport(**report) for report in data]

        return []

    def extract_patterns(self) -> Dict[str, Any]:
        """
        Extract common patterns from bug reports.
        Identifies:
        - Vulnerability types
        - Discovery techniques
        - Exploitation methods
        - Technology combinations
        """
        logger.info("Extracting patterns from reports...")

        patterns = {
            "vulnerability_types": {},
            "discovery_methods": {},
            "common_technologies": {},
            "high_impact_chains": [],
            "quick_wins": [],
        }

        for report in self.reports:
            # Track vulnerability types
            vuln_type = report.vulnerability_type
            if vuln_type not in patterns["vulnerability_types"]:
                patterns["vulnerability_types"][vuln_type] = {
                    "count": 0,
                    "examples": [],
                    "avg_cvss": 0
                }
            patterns["vulnerability_types"][vuln_type]["count"] += 1
            patterns["vulnerability_types"][vuln_type]["examples"].append({
                "title": report.title,
                "severity": report.severity,
                "bounty": report.bounty_amount
            })

            # Track discovery methods
            method = report.discovery_method
            if method not in patterns["discovery_methods"]:
                patterns["discovery_methods"][method] = {
                    "count": 0,
                    "techniques": []
                }
            patterns["discovery_methods"][method]["count"] += 1

            # Track technology combinations
            tech = report.affected_technology
            if tech not in patterns["common_technologies"]:
                patterns["common_technologies"][tech] = {
                    "count": 0,
                    "vulnerabilities": []
                }
            patterns["common_technologies"][tech]["count"] += 1
            patterns["common_technologies"][tech]["vulnerabilities"].append(
                report.vulnerability_type
            )

            # Track high-impact findings
            if report.severity == "high" and report.bounty_amount and report.bounty_amount > 2000:
                patterns["high_impact_chains"].append({
                    "vulnerability": report.title,
                    "type": report.vulnerability_type,
                    "bounty": report.bounty_amount,
                    "steps": report.exploitation_steps[:3]
                })

            # Track quick wins (medium impact, easy to find)
            if report.severity in ["medium", "high"] and "analysis" in report.discovery_method.lower():
                patterns["quick_wins"].append({
                    "vulnerability": report.title,
                    "method": report.discovery_method,
                    "bounty": report.bounty_amount,
                    "effort": "low"
                })

        self.patterns = patterns
        logger.info(f"Extracted {len(patterns['vulnerability_types'])} vulnerability types")

        return patterns

    def get_testing_checklist(self, technology_stack: List[str]) -> Dict[str, List[str]]:
        """
        Generate testing checklist based on technology stack.

        Uses bug bounty data to prioritize tests by:
        - How often vulnerabilities appear in this stack
        - Bounty amount (economic importance)
        - Severity
        """
        logger.info(f"Generating checklist for: {technology_stack}")

        checklist = {
            "high_priority": [],
            "medium_priority": [],
            "low_priority": [],
        }

        # Find reports matching technology stack
        matching_reports = [
            r for r in self.reports
            if any(tech.lower() in r.affected_technology.lower() for tech in technology_stack)
        ]

        # Sort by bounty (economic indicator of impact)
        matching_reports.sort(
            key=lambda x: (x.severity == "high", x.bounty_amount or 0),
            reverse=True
        )

        for report in matching_reports:
            item = {
                "vulnerability": report.title,
                "type": report.vulnerability_type,
                "discovery_method": report.discovery_method,
                "expected_bounty": report.bounty_amount,
                "steps": report.exploitation_steps[:3]
            }

            if report.severity == "high":
                checklist["high_priority"].append(item)
            elif report.severity == "medium":
                checklist["medium_priority"].append(item)
            else:
                checklist["low_priority"].append(item)

        return checklist

    def get_exploitation_guide(self, vulnerability_type: str) -> Optional[Dict[str, Any]]:
        """Get exploitation guide for a specific vulnerability type"""
        for report in self.reports:
            if vulnerability_type.lower() in report.vulnerability_type.lower():
                return {
                    "title": report.title,
                    "description": report.description,
                    "impact": report.impact,
                    "steps": report.exploitation_steps,
                    "remediation": report.remediation,
                    "cvss": report.cvss_score,
                    "similar_findings": [
                        r.title for r in self.reports
                        if r.vulnerability_type == report.vulnerability_type and r.id != report.id
                    ]
                }

        return None

    def get_high_impact_findings(self, min_bounty: int = 2000) -> List[BugReport]:
        """Get high-impact findings that are worth hunting for"""
        return [
            r for r in self.reports
            if r.severity == "high" and (r.bounty_amount or 0) >= min_bounty
        ]

    def save_cache(self) -> None:
        """Save reports to cache"""
        cache_file = self.cache_dir / "reports_cache.json"

        with open(cache_file, "w") as f:
            reports_data = [
                {
                    "id": r.id,
                    "title": r.title,
                    "severity": r.severity,
                    "vulnerability_type": r.vulnerability_type,
                    "description": r.description,
                    "impact": r.impact,
                    "affected_technology": r.affected_technology,
                    "discovery_method": r.discovery_method,
                    "exploitation_steps": r.exploitation_steps,
                    "remediation": r.remediation,
                    "cve": r.cve,
                    "cvss_score": r.cvss_score,
                    "bounty_amount": r.bounty_amount,
                }
                for r in self.reports
            ]
            json.dump(reports_data, f, indent=2)

    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary of bug bounty findings"""
        total_bounty = sum(r.bounty_amount or 0 for r in self.reports)
        avg_bounty = total_bounty / len(self.reports) if self.reports else 0

        severity_breakdown = {}
        for report in self.reports:
            severity = report.severity
            if severity not in severity_breakdown:
                severity_breakdown[severity] = 0
            severity_breakdown[severity] += 1

        return {
            "total_reports": len(self.reports),
            "total_potential_bounty": total_bounty,
            "average_bounty": avg_bounty,
            "severity_breakdown": severity_breakdown,
            "vulnerability_types": len(self.patterns.get("vulnerability_types", {})),
            "technologies_covered": len(self.patterns.get("common_technologies", {})),
            "high_impact_findings": len(self.get_high_impact_findings()),
        }
