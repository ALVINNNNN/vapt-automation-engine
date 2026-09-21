"""
Burp Suite Professional Integration

Handles web application vulnerability scanning via Burp Suite API.
"""

import logging
import requests
import time
from typing import Dict, List, Any, Optional
from pathlib import Path

from vapt.core.scanner import BaseScanner, ScannerType, ScanResult

logger = logging.getLogger(__name__)


class BurpScanner(BaseScanner):
    """Burp Suite Professional integration for web app scanning"""

    def __init__(self):
        super().__init__("burp", ScannerType.WEB_APPLICATION)
        self.api_url: str = ""
        self.api_key: str = ""
        self.timeout: int = 3600
        self.session_timeout: int = 300

    def configure(self, config: Dict[str, Any]) -> None:
        """Configure Burp Suite scanner"""
        self.config = config

        self.api_url = config.get("api_url", "http://localhost:1337")
        self.api_key = config.get("api_key", "")
        self.timeout = config.get("timeout", 3600)
        self.session_timeout = config.get("session_timeout", 300)

        self.is_configured = self._verify_connection()

    def validate_configuration(self) -> bool:
        """Verify Burp Suite is accessible"""
        return self.is_configured

    def _verify_connection(self) -> bool:
        """Test connection to Burp Suite API"""
        try:
            response = requests.get(
                f"{self.api_url}/v2/project/status",
                headers=self._get_headers(),
                timeout=5,
            )
            return response.status_code in [200, 401]  # 401 if auth required
        except Exception as e:
            logger.error(f"Cannot connect to Burp Suite: {e}")
            return False

    def execute(self, targets: List[str]) -> ScanResult:
        """Execute Burp Suite scan"""
        start_time = time.time()

        logger.info(f"Starting Burp Suite scan on {len(targets)} target(s)")

        vulnerabilities = []
        details = {}

        for target in targets:
            try:
                # Create scan
                scan_id = self._create_scan(target)
                if not scan_id:
                    logger.error(f"Failed to create scan for {target}")
                    continue

                # Wait for scan completion
                self._wait_for_scan(scan_id)

                # Retrieve results
                issues = self._get_scan_issues(scan_id)
                vulnerabilities.extend(issues)

                details[target] = {
                    "scan_id": scan_id,
                    "issues_found": len(issues),
                }

                # Delete scan
                self._delete_scan(scan_id)

            except Exception as e:
                logger.error(f"Error scanning {target}: {e}")

        duration = time.time() - start_time

        return self._create_result(
            targets=targets,
            vulnerabilities=vulnerabilities,
            details=details,
            duration=duration,
        )

    def parse_results(self, raw_output: Any) -> List[Dict[str, Any]]:
        """Parse Burp Suite output"""
        vulnerabilities = []

        if isinstance(raw_output, dict):
            if "issues" in raw_output:
                for issue in raw_output["issues"]:
                    vulnerabilities.append(self._format_issue(issue))

        return vulnerabilities

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        headers = {
            "Content-Type": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        return headers

    def _create_scan(self, target: str) -> Optional[str]:
        """Create a new Burp scan"""
        try:
            payload = {
                "urls": [target],
                "crawl_strategy": "deep",
                "scan_speed": "fast",
            }

            response = requests.post(
                f"{self.api_url}/v2/scan",
                json=payload,
                headers=self._get_headers(),
                timeout=10,
            )

            if response.status_code == 201:
                scan_data = response.json()
                return scan_data.get("scan_id")
            else:
                logger.error(f"Burp API error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error creating Burp scan: {e}")
            return None

    def _wait_for_scan(self, scan_id: str) -> None:
        """Wait for scan to complete"""
        start = time.time()

        while time.time() - start < self.timeout:
            try:
                response = requests.get(
                    f"{self.api_url}/v2/scan/{scan_id}",
                    headers=self._get_headers(),
                    timeout=10,
                )

                if response.status_code == 200:
                    scan_data = response.json()

                    if scan_data.get("scan_status") == "succeeded":
                        logger.info(f"Scan {scan_id} completed successfully")
                        return

                    elif scan_data.get("scan_status") == "failed":
                        logger.error(f"Scan {scan_id} failed")
                        return

                time.sleep(10)  # Check every 10 seconds

            except Exception as e:
                logger.error(f"Error checking scan status: {e}")
                time.sleep(10)

        logger.warning(f"Scan {scan_id} did not complete within timeout")

    def _get_scan_issues(self, scan_id: str) -> List[Dict[str, Any]]:
        """Retrieve issues from completed scan"""
        vulnerabilities = []

        try:
            response = requests.get(
                f"{self.api_url}/v2/scan/{scan_id}/issues",
                headers=self._get_headers(),
                timeout=30,
            )

            if response.status_code == 200:
                issues_data = response.json()

                for issue in issues_data.get("issues", []):
                    vulnerabilities.append(self._format_issue(issue))

        except Exception as e:
            logger.error(f"Error retrieving scan issues: {e}")

        return vulnerabilities

    def _format_issue(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Format Burp issue to standardized format"""
        severity_map = {
            "high": "High",
            "medium": "Medium",
            "low": "Low",
            "information": "Info",
        }

        return {
            "host": issue.get("origin", ""),
            "title": issue.get("name", ""),
            "severity": severity_map.get(issue.get("severity", "low"), "Low"),
            "cvss_score": self._estimate_cvss(issue.get("severity", "low")),
            "description": issue.get("description", ""),
            "remediation": issue.get("remediation", ""),
            "evidence": issue.get("http_messages", []),
            "tool_source": "burp",
            "issue_type": issue.get("issue_type", ""),
            "confidence": issue.get("confidence", "firm"),
        }

    def _estimate_cvss(self, severity: str) -> float:
        """Estimate CVSS score from Burp severity"""
        severity_cvss = {
            "high": 7.5,
            "medium": 5.5,
            "low": 3.5,
            "information": 0.0,
        }
        return severity_cvss.get(severity.lower(), 5.0)

    def _delete_scan(self, scan_id: str) -> None:
        """Delete scan from Burp Suite"""
        try:
            requests.delete(
                f"{self.api_url}/v2/scan/{scan_id}",
                headers=self._get_headers(),
                timeout=10,
            )
            logger.info(f"Scan {scan_id} deleted")
        except Exception as e:
            logger.error(f"Error deleting scan: {e}")
