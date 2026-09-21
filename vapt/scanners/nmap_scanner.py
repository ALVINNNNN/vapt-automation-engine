"""
Nmap Scanner Integration

Handles network reconnaissance and vulnerability scanning using Nmap.
"""

import subprocess
import logging
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any
import tempfile

from vapt.core.scanner import BaseScanner, ScannerType, ScanResult

logger = logging.getLogger(__name__)


class NmapScanner(BaseScanner):
    """Nmap integration for network scanning"""

    def __init__(self):
        super().__init__("nmap", ScannerType.NETWORK)
        self.nmap_path = "nmap"
        self.scripts = [
            "vuln",
            "default",
            "discovery",
        ]

    def configure(self, config: Dict[str, Any]) -> None:
        """Configure Nmap scanner"""
        self.config = config

        if "nmap_path" in config:
            self.nmap_path = config["nmap_path"]

        if "scripts" in config:
            self.scripts = config["scripts"]

        self.is_configured = self._verify_installation()

    def validate_configuration(self) -> bool:
        """Verify Nmap is installed and accessible"""
        return self.is_configured

    def _verify_installation(self) -> bool:
        """Check if Nmap is installed"""
        try:
            result = subprocess.run(
                [self.nmap_path, "--version"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except FileNotFoundError:
            logger.error("Nmap not found. Please install Nmap.")
            return False
        except Exception as e:
            logger.error(f"Error verifying Nmap installation: {e}")
            return False

    def execute(self, targets: List[str]) -> ScanResult:
        """Execute Nmap scan"""
        start_time = time.time()

        logger.info(f"Starting Nmap scan on {len(targets)} target(s)")

        # Create temporary file for XML output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp:
            xml_file = tmp.name

        try:
            # Build Nmap command
            cmd = [
                self.nmap_path,
                "-sV",  # Service/version detection
                "-sC",  # Default scripts
                "--script", ",".join(self.scripts),
                "-oX", xml_file,
                "-T4",  # Aggressive timing
            ]

            cmd.extend(targets)

            # Execute scan
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=3600,  # 1 hour timeout
            )

            if result.returncode != 0:
                logger.error(f"Nmap error: {result.stderr.decode()}")

            # Parse results
            vulnerabilities = self._parse_xml(xml_file)

            duration = time.time() - start_time

            return self._create_result(
                targets=targets,
                vulnerabilities=vulnerabilities,
                details={"xml_file": xml_file},
                duration=duration,
            )

        finally:
            # Cleanup
            Path(xml_file).unlink(missing_ok=True)

    def parse_results(self, raw_output: Any) -> List[Dict[str, Any]]:
        """Parse Nmap output"""
        vulnerabilities = []

        if isinstance(raw_output, str):
            vulnerabilities = self._parse_xml(raw_output)

        return vulnerabilities

    def _parse_xml(self, xml_file: str) -> List[Dict[str, Any]]:
        """Parse Nmap XML output"""
        vulnerabilities = []

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for host in root.findall("host"):
                status = host.find("status")
                if status is None or status.get("state") != "up":
                    continue

                hostnames = host.findall("hostnames/hostname")
                hostname = hostnames[0].get("name") if hostnames else "Unknown"

                for address in host.findall("address"):
                    if address.get("addrtype") == "ipv4":
                        ip = address.get("addr")
                        break
                else:
                    ip = "Unknown"

                # Extract ports and services
                for port in host.findall("ports/port"):
                    port_num = port.get("portid")
                    protocol = port.get("protocol")

                    service = port.find("service")
                    service_name = service.get("name") if service is not None else "unknown"
                    service_version = service.get("version") if service is not None else ""

                    # Check for script results (vulnerabilities)
                    scripts = port.findall("script")
                    for script in scripts:
                        script_id = script.get("id")
                        output = script.get("output", "")

                        if "VULNERABLE" in output or "vuln" in script_id.lower():
                            vulnerabilities.append({
                                "host": ip,
                                "hostname": hostname,
                                "port": port_num,
                                "protocol": protocol,
                                "service": service_name,
                                "version": service_version,
                                "vulnerability": script_id,
                                "description": output[:200],
                                "severity": self._assess_severity(script_id, output),
                                "cvss_score": 5.5,  # Default; would be enhanced with NVD lookup
                                "tool_source": "nmap",
                            })

        except ET.ParseError as e:
            logger.error(f"Error parsing Nmap XML: {e}")

        return vulnerabilities

    def _assess_severity(self, script_id: str, output: str) -> str:
        """Assess vulnerability severity"""
        script_id_lower = script_id.lower()
        output_lower = output.lower()

        critical_keywords = ["rce", "remote code execution", "critical"]
        high_keywords = ["injection", "authentication", "authorization", "ssrf"]
        medium_keywords = ["information", "crypto", "weak"]

        if any(keyword in script_id_lower or keyword in output_lower for keyword in critical_keywords):
            return "Critical"

        if any(keyword in script_id_lower or keyword in output_lower for keyword in high_keywords):
            return "High"

        if any(keyword in script_id_lower or keyword in output_lower for keyword in medium_keywords):
            return "Medium"

        return "Low"
