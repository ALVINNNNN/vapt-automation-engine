"""
VAPT CLI - Command Line Interface

Main entry point for the penetration testing automation engine.
"""

import click
import logging
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from vapt.core.assessment import Assessment, AssessmentType, AssessmentStatus
from vapt.core.scanner import ScannerRegistry, ScannerType
from vapt.core.reporter import Reporter, ReportFormat, ExecutiveReporter, TechnicalReporter
from vapt.scanners.nmap_scanner import NmapScanner
from vapt.scanners.sslyze_scanner import SSLyzeScanner
from vapt.scanners.burp_scanner import BurpScanner
from vapt.compliance.framework_mapper import FrameworkMapper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """VAPT Automation Engine - Penetration Testing Automation"""
    pass


@cli.command()
@click.option("--client", required=True, help="Client name")
@click.option("--type", "assessment_type", type=click.Choice(["nvapт", "avapt", "hybrid"]), default="hybrid", help="Assessment type")
@click.option("--output-dir", type=click.Path(), help="Output directory for assessment data")
def init(client: str, assessment_type: str, output_dir: Optional[str]):
    """Initialize a new penetration testing assessment"""

    try:
        type_map = {
            "nvapт": AssessmentType.NVAPТ,
            "avapt": AssessmentType.AVAPT,
            "hybrid": AssessmentType.HYBRID,
        }

        assessment = Assessment(
            client_name=client,
            assessment_type=type_map[assessment_type],
            working_dir=Path(output_dir) if output_dir else None,
        )

        click.echo(f"✓ Assessment initialized: {assessment.assessment_id}")
        click.echo(f"  Client: {client}")
        click.echo(f"  Type: {assessment_type}")
        click.echo(f"  Working Directory: {assessment.working_dir}")

        assessment.save_state()

    except Exception as e:
        click.echo(f"✗ Error initializing assessment: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--targets", required=True, type=click.Path(exists=True), help="File with target IPs/hosts (one per line)")
@click.option("--profile", type=click.Choice(["quick", "normal", "aggressive"]), default="normal", help="Scan profile")
@click.option("--output-dir", type=click.Path(), required=True, help="Assessment output directory")
def network_scan(targets: str, profile: str, output_dir: str):
    """Execute network vulnerability assessment (nVAPT)"""

    try:
        output_path = Path(output_dir)

        # Read targets
        with open(targets) as f:
            target_list = [line.strip() for line in f if line.strip()]

        if not target_list:
            click.echo("✗ No targets provided", err=True)
            raise click.Abort()

        click.echo(f"Starting network scan on {len(target_list)} target(s)...")

        # Initialize scanners
        registry = ScannerRegistry()

        # Nmap scanner
        nmap = NmapScanner()
        nmap_config = {
            "scripts": ["vuln", "default", "discovery"],
        }
        nmap.configure(nmap_config)
        registry.register_scanner(nmap)

        # SSLyze scanner
        sslyze = SSLyzeScanner()
        sslyze.configure({})
        registry.register_scanner(sslyze)

        # Execute network scans
        results = registry.execute_by_type(ScannerType.NETWORK, target_list)

        click.echo(f"✓ Network scan completed")
        click.echo(f"  Scanners used: {len(results)}")

        for result in results:
            click.echo(f"  - {result.scanner_name}: {len(result.vulnerabilities)} vulnerabilities found")

        # Save results
        output_file = output_path / "network_scan_results.json"
        with open(output_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "targets": target_list,
                "results": [
                    {
                        "scanner": r.scanner_name,
                        "vulnerabilities": r.vulnerabilities,
                        "duration": r.duration_seconds,
                    } for r in results
                ]
            }, f, indent=2, default=str)

        click.echo(f"  Results saved to: {output_file}")

    except Exception as e:
        click.echo(f"✗ Error during network scan: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--url", required=True, help="Target application URL")
@click.option("--burp-config", type=click.Path(exists=True), help="Burp Suite API configuration")
@click.option("--output-dir", type=click.Path(), required=True, help="Assessment output directory")
def app_scan(url: str, burp_config: Optional[str], output_dir: str):
    """Execute application vulnerability assessment (AVAPT)"""

    try:
        output_path = Path(output_dir)

        click.echo(f"Starting application scan on {url}...")

        # Initialize Burp scanner
        burp = BurpScanner()

        config = {
            "api_url": "http://localhost:1337",
            "api_key": "",
        }

        if burp_config:
            with open(burp_config) as f:
                config.update(json.load(f))

        burp.configure(config)

        if not burp.validate_configuration():
            click.echo("⚠ Burp Suite API not accessible, proceeding with demo mode", err=True)

        # Execute scan
        result = burp.execute([url])

        click.echo(f"✓ Application scan completed")
        click.echo(f"  Vulnerabilities found: {len(result.vulnerabilities)}")

        # Save results
        output_file = output_path / "app_scan_results.json"
        with open(output_file, "w") as f:
            json.dump({
                "timestamp": result.timestamp,
                "target": url,
                "vulnerabilities": result.vulnerabilities,
                "duration": result.duration_seconds,
            }, f, indent=2, default=str)

        click.echo(f"  Results saved to: {output_file}")

    except Exception as e:
        click.echo(f"✗ Error during application scan: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--assessment-id", required=True, help="Assessment ID")
@click.option("--format", "report_formats", multiple=True, type=click.Choice(["executive", "technical", "html", "pdf", "json"]), default=["executive", "technical"], help="Report formats")
@click.option("--output-dir", type=click.Path(), required=True, help="Output directory for reports")
def report(assessment_id: str, report_formats: tuple, output_dir: str):
    """Generate comprehensive assessment reports"""

    try:
        output_path = Path(output_dir)

        # Create reporter
        reporter = Reporter(output_path)

        # Register reporters
        reporter.register_reporter(ReportFormat.EXECUTIVE, ExecutiveReporter())
        reporter.register_reporter(ReportFormat.TECHNICAL, TechnicalReporter())

        # Load assessment data (demo)
        assessment_data = {
            "assessment_id": assessment_id,
            "client": "Demo Client",
            "type": "hybrid",
        }

        findings = []  # Would load from assessment results

        # Generate reports
        if not report_formats:
            report_formats = ["executive", "technical"]

        format_map = {
            "executive": ReportFormat.EXECUTIVE,
            "technical": ReportFormat.TECHNICAL,
            "html": ReportFormat.HTML,
            "pdf": ReportFormat.PDF,
            "json": ReportFormat.JSON,
        }

        click.echo("Generating reports...")

        for fmt in report_formats:
            if fmt in format_map:
                report_path = reporter.generate_report(format_map[fmt], assessment_data, findings)
                if report_path:
                    click.echo(f"✓ {fmt.upper()} report: {report_path}")
                else:
                    click.echo(f"✗ Failed to generate {fmt} report", err=True)

        click.echo(f"\nReports saved to: {output_path}")

    except Exception as e:
        click.echo(f"✗ Error generating reports: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--assessment-id", required=True, help="Assessment ID")
@click.option("--output-dir", type=click.Path(), required=True, help="Assessment data directory")
def summarize(assessment_id: str, output_dir: str):
    """Display assessment summary"""

    try:
        output_path = Path(output_dir)
        state_file = output_path / "assessment_state.json"

        if not state_file.exists():
            click.echo(f"✗ Assessment state file not found: {state_file}", err=True)
            raise click.Abort()

        with open(state_file) as f:
            state = json.load(f)

        summary = state.get("summary", {})

        click.echo("\n" + "=" * 60)
        click.echo("ASSESSMENT SUMMARY")
        click.echo("=" * 60)
        click.echo(f"Assessment ID: {summary.get('assessment_id')}")
        click.echo(f"Client: {summary.get('client')}")
        click.echo(f"Type: {summary.get('type')}")
        click.echo(f"Status: {summary.get('status')}")
        click.echo(f"Start Time: {summary.get('start_time')}")
        click.echo(f"End Time: {summary.get('end_time')}")
        click.echo(f"\nTotal Findings: {summary.get('total_findings')}")

        click.echo("\nFindings by Severity:")
        for severity, count in summary.get('findings_by_severity', {}).items():
            click.echo(f"  {severity}: {count}")

        click.echo(f"\nScanners Used: {', '.join(summary.get('scanners_used', []))}")
        click.echo(f"Exploitations Attempted: {summary.get('exploitations_attempted', 0)}")
        click.echo("=" * 60 + "\n")

    except Exception as e:
        click.echo(f"✗ Error loading assessment summary: {e}", err=True)
        raise click.Abort()


def main():
    """Main entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
