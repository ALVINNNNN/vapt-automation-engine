"""
Report Generation Engine

Generates comprehensive reports in multiple formats for client delivery
and compliance documentation.
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class ReportFormat(Enum):
    """Available report formats"""
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    HTML = "html"
    PDF = "pdf"
    JSON = "json"
    EXCEL = "excel"


class BaseReporter(ABC):
    """Abstract base class for report generators"""

    def __init__(self, format_type: ReportFormat):
        """Initialize reporter"""
        self.format_type = format_type

    @abstractmethod
    def generate(
        self,
        assessment_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        output_path: Path,
    ) -> Path:
        """Generate report and return path"""
        pass

    @abstractmethod
    def validate_data(self, assessment_data: Dict[str, Any]) -> bool:
        """Validate input data"""
        pass


class Reporter:
    """Main report orchestration class"""

    def __init__(self, output_dir: Optional[Path] = None):
        """Initialize reporter"""
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.reporters: Dict[ReportFormat, BaseReporter] = {}
        self.generated_reports: List[Path] = []

    def register_reporter(self, format_type: ReportFormat, reporter: BaseReporter) -> None:
        """Register a report generator"""
        self.reporters[format_type] = reporter
        logger.info(f"Reporter registered: {format_type.value}")

    def generate_report(
        self,
        format_type: ReportFormat,
        assessment_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        output_filename: Optional[str] = None,
    ) -> Optional[Path]:
        """Generate a single report"""
        reporter = self.reporters.get(format_type)
        if not reporter:
            logger.error(f"No reporter configured for format: {format_type.value}")
            return None

        if not reporter.validate_data(assessment_data):
            logger.error(f"Invalid data for report format: {format_type.value}")
            return None

        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{assessment_data.get('assessment_id', 'report')}_{format_type.value}_{timestamp}"

        output_path = self.output_dir / output_filename

        try:
            report_path = reporter.generate(assessment_data, findings, output_path)
            self.generated_reports.append(report_path)
            logger.info(f"Report generated: {report_path}")
            return report_path
        except Exception as e:
            logger.error(f"Failed to generate {format_type.value} report: {str(e)}")
            return None

    def generate_all_reports(
        self,
        assessment_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        formats: Optional[List[ReportFormat]] = None,
    ) -> Dict[ReportFormat, Optional[Path]]:
        """Generate all configured reports"""
        if formats is None:
            formats = list(self.reporters.keys())

        results = {}
        for format_type in formats:
            report_path = self.generate_report(format_type, assessment_data, findings)
            results[format_type] = report_path

        return results

    def get_generated_reports(self) -> List[Path]:
        """Get all generated report paths"""
        return self.generated_reports

    def package_reports(self, archive_path: Optional[Path] = None) -> Path:
        """Package all reports into a single archive"""
        import shutil

        if archive_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = self.output_dir / f"reports_archive_{timestamp}"

        archive_file = shutil.make_archive(
            str(archive_path),
            "zip",
            self.output_dir,
        )

        logger.info(f"Reports packaged: {archive_file}")
        return Path(archive_file)


class ExecutiveReporter(BaseReporter):
    """Executive summary report generator"""

    def __init__(self):
        super().__init__(ReportFormat.EXECUTIVE)

    def generate(
        self,
        assessment_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        output_path: Path,
    ) -> Path:
        """Generate executive summary"""
        output_path = Path(str(output_path) + ".txt")

        content = self._generate_content(assessment_data, findings)

        with open(output_path, "w") as f:
            f.write(content)

        return output_path

    def validate_data(self, assessment_data: Dict[str, Any]) -> bool:
        """Validate data for executive report"""
        required_fields = ["client", "assessment_id"]
        return all(field in assessment_data for field in required_fields)

    def _generate_content(
        self,
        assessment_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
    ) -> str:
        """Generate executive summary content"""
        severity_counts = {}
        for finding in findings:
            severity = finding.get("severity", "Unknown")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        content = f"""
EXECUTIVE SUMMARY
=================

Client: {assessment_data.get('client', 'N/A')}
Assessment ID: {assessment_data.get('assessment_id', 'N/A')}
Type: {assessment_data.get('type', 'N/A')}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

FINDINGS OVERVIEW
-----------------

Total Findings: {len(findings)}

By Severity:
"""
        for severity, count in severity_counts.items():
            content += f"  {severity}: {count}\n"

        content += f"""
KEY RISKS
---------

"""
        critical_findings = [f for f in findings if f.get("severity", "").lower() == "critical"]
        high_findings = [f for f in findings if f.get("severity", "").lower() == "high"]

        if critical_findings:
            content += "CRITICAL:\n"
            for finding in critical_findings[:3]:
                content += f"  - {finding.get('title', 'Unknown')}\n"
            content += "\n"

        if high_findings:
            content += "HIGH:\n"
            for finding in high_findings[:3]:
                content += f"  - {finding.get('title', 'Unknown')}\n"

        content += """
RECOMMENDATIONS
---------------

1. Address all CRITICAL findings immediately
2. Implement fixes for HIGH severity findings within 30 days
3. Review medium severity findings within 90 days
4. Conduct periodic security assessments

"""
        return content


class TechnicalReporter(BaseReporter):
    """Technical detailed report generator"""

    def __init__(self):
        super().__init__(ReportFormat.TECHNICAL)

    def generate(
        self,
        assessment_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        output_path: Path,
    ) -> Path:
        """Generate technical report"""
        output_path = Path(str(output_path) + ".txt")

        content = self._generate_content(assessment_data, findings)

        with open(output_path, "w") as f:
            f.write(content)

        return output_path

    def validate_data(self, assessment_data: Dict[str, Any]) -> bool:
        """Validate data for technical report"""
        required_fields = ["client", "assessment_id"]
        return all(field in assessment_data for field in required_fields)

    def _generate_content(
        self,
        assessment_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
    ) -> str:
        """Generate technical report content"""
        content = f"""
TECHNICAL ASSESSMENT REPORT
============================

Client: {assessment_data.get('client', 'N/A')}
Assessment ID: {assessment_data.get('assessment_id', 'N/A')}
Type: {assessment_data.get('type', 'N/A')}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DETAILED FINDINGS
-----------------

"""
        # Sort by severity
        severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        sorted_findings = sorted(
            findings,
            key=lambda x: severity_order.get(x.get("severity", "Unknown"), 4)
        )

        for finding in sorted_findings:
            content += f"""
Finding: {finding.get('title', 'Unknown')}
Severity: {finding.get('severity', 'Unknown')}
CVSS Score: {finding.get('cvss_score', 'N/A')}

Description:
{finding.get('description', 'N/A')}

Impact:
{finding.get('impact', 'N/A')}

Remediation:
{finding.get('remediation', 'N/A')}

Evidence:
"""
            for evidence in finding.get('evidence', []):
                content += f"  - {evidence}\n"

            content += "\n" + "-" * 80 + "\n"

        return content
