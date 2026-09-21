"""
Assessment Orchestration Engine

Coordinates the complete penetration testing workflow including
reconnaissance, scanning, exploitation, and reporting.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class AssessmentType(Enum):
    """Assessment type enumeration"""
    NVAPТ = "nvapт"  # Network VAPT
    AVAPT = "avapt"   # Application VAPT
    HYBRID = "hybrid"  # Combined assessment


class AssessmentStatus(Enum):
    """Assessment status tracking"""
    PLANNING = "planning"
    RECONNAISSANCE = "reconnaissance"
    SCANNING = "scanning"
    EXPLOITATION = "exploitation"
    ANALYSIS = "analysis"
    REPORTING = "reporting"
    COMPLETED = "completed"
    FAILED = "failed"


class Assessment:
    """Main assessment orchestration class"""

    def __init__(
        self,
        client_name: str,
        assessment_type: AssessmentType = AssessmentType.HYBRID,
        assessment_id: Optional[str] = None,
        working_dir: Optional[Path] = None,
    ):
        """Initialize assessment"""
        self.assessment_id = assessment_id or str(uuid.uuid4())
        self.client_name = client_name
        self.assessment_type = assessment_type
        self.working_dir = Path(working_dir) if working_dir else Path.cwd() / "assessments" / self.assessment_id
        self.working_dir.mkdir(parents=True, exist_ok=True)

        self.status = AssessmentStatus.PLANNING
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None

        self.metadata: Dict[str, Any] = {
            "assessment_id": self.assessment_id,
            "client": client_name,
            "type": assessment_type.value,
            "created": self.start_time.isoformat(),
            "frameworks": ["OWASP", "NIST", "PCI-DSS", "ISO27001"],
        }

        self.findings: List[Dict[str, Any]] = []
        self.scan_results: Dict[str, Any] = {}
        self.exploitation_results: List[Dict[str, Any]] = []

        self._setup_logging()
        logger.info(f"Assessment {self.assessment_id} initialized for {client_name}")

    def _setup_logging(self) -> None:
        """Setup logging for this assessment"""
        log_dir = self.working_dir / "logs"
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(log_dir / f"assessment_{self.assessment_id}.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def set_status(self, status: AssessmentStatus) -> None:
        """Update assessment status"""
        self.status = status
        logger.info(f"Assessment status: {status.value}")

    def add_finding(
        self,
        title: str,
        severity: str,
        cvss_score: float,
        description: str,
        impact: str,
        remediation: str,
        evidence: Optional[List[str]] = None,
        frameworks: Optional[Dict[str, List[str]]] = None,
        tool_source: Optional[str] = None,
    ) -> None:
        """Add a security finding"""
        finding = {
            "finding_id": str(uuid.uuid4()),
            "title": title,
            "severity": severity,
            "cvss_score": cvss_score,
            "description": description,
            "impact": impact,
            "remediation": remediation,
            "evidence": evidence or [],
            "frameworks": frameworks or {},
            "tool_source": tool_source,
            "timestamp": datetime.now().isoformat(),
        }
        self.findings.append(finding)
        logger.info(f"Finding added: {title} ({severity})")

    def add_scan_result(self, scanner_name: str, results: Dict[str, Any]) -> None:
        """Store scan results from a tool"""
        self.scan_results[scanner_name] = {
            "timestamp": datetime.now().isoformat(),
            "data": results,
        }
        logger.info(f"Scan results added from {scanner_name}")

    def add_exploitation_result(
        self,
        vulnerability_id: str,
        exploit_name: str,
        success: bool,
        details: Dict[str, Any],
    ) -> None:
        """Record exploitation attempt"""
        result = {
            "vulnerability_id": vulnerability_id,
            "exploit": exploit_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
        }
        self.exploitation_results.append(result)
        logger.info(f"Exploitation result: {exploit_name} - {'SUCCESS' if success else 'FAILED'}")

    def get_findings_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Get findings filtered by severity"""
        return [f for f in self.findings if f["severity"].lower() == severity.lower()]

    def get_summary(self) -> Dict[str, Any]:
        """Get assessment summary"""
        severities = {}
        for finding in self.findings:
            severity = finding["severity"]
            severities[severity] = severities.get(severity, 0) + 1

        return {
            "assessment_id": self.assessment_id,
            "client": self.client_name,
            "type": self.assessment_type.value,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_findings": len(self.findings),
            "findings_by_severity": severities,
            "scanners_used": list(self.scan_results.keys()),
            "exploitations_attempted": len(self.exploitation_results),
        }

    def save_state(self) -> None:
        """Save assessment state to disk"""
        state_file = self.working_dir / "assessment_state.json"
        state = {
            "metadata": self.metadata,
            "status": self.status.value,
            "findings": self.findings,
            "scan_results": self.scan_results,
            "exploitation_results": self.exploitation_results,
            "summary": self.get_summary(),
        }

        with open(state_file, "w") as f:
            json.dump(state, f, indent=2, default=str)

        logger.info(f"Assessment state saved to {state_file}")

    def finalize(self) -> None:
        """Finalize assessment"""
        self.end_time = datetime.now()
        self.status = AssessmentStatus.COMPLETED
        self.save_state()
        logger.info(f"Assessment {self.assessment_id} completed")

    def __repr__(self) -> str:
        return f"Assessment(id={self.assessment_id}, client={self.client_name}, type={self.assessment_type.value})"
