"""
CLI commands for AI-driven penetration testing
"""

import click
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from .ai_coordinator import AIAssessmentCoordinator

logger = logging.getLogger(__name__)


@click.group()
def ai_commands():
    """AI-driven penetration testing commands"""
    pass


@ai_commands.command()
@click.option("--client", required=True, help="Client name")
@click.option("--target", required=True, help="Target URL (e.g., https://app.example.com)")
@click.option("--output-dir", type=click.Path(), help="Output directory for results")
def interactive(client: str, target: str, output_dir: Optional[str]):
    """Run interactive AI-driven assessment with Claude reasoning

    This mode allows you to have a conversation with Claude about:
    - Reconnaissance strategy
    - Endpoint discovery and testing
    - JavaScript analysis techniques
    - Vulnerability hypotheses
    - Exploitation approaches

    Claude will guide you through the assessment step-by-step.
    """
    try:
        click.echo(f"\n{'='*60}")
        click.echo("AI-DRIVEN INTERACTIVE PENETRATION TEST")
        click.echo(f"{'='*60}")
        click.echo(f"Client: {client}")
        click.echo(f"Target: {target}")
        click.echo(f"\nInitializing Claude AI assessment coordinator...")

        coordinator = AIAssessmentCoordinator(client, target)

        click.echo("Starting interactive assessment...")
        click.echo("(Press Ctrl+C to exit at any time)\n")

        result = coordinator.run_interactive_assessment()

        click.echo(f"\n{'='*60}")
        click.echo("ASSESSMENT COMPLETE")
        click.echo(f"{'='*60}")
        click.echo(f"Assessment ID: {result['assessment_id']}")
        click.echo(f"Status: {result['status']}")
        click.echo(f"Findings: {result['findings_count']}")
        click.echo(f"Results saved to: {result['results_file']}")

    except KeyboardInterrupt:
        click.echo("\n\nAssessment interrupted by user")
    except Exception as e:
        click.echo(f"\n✗ Error: {e}", err=True)
        raise click.Abort()


@ai_commands.command()
@click.option("--client", required=True, help="Client name")
@click.option("--target", required=True, help="Target URL")
@click.option("--output-dir", type=click.Path(), help="Output directory")
def automated(client: str, target: str, output_dir: Optional[str]):
    """Run fully automated AI assessment

    This mode runs through all assessment phases automatically:
    1. Reconnaissance - Gather target information
    2. Analysis - Analyze findings for vulnerabilities
    3. Testing - Execute hypothesis-driven tests
    4. Exploitation - Exploit confirmed vulnerabilities
    5. Reporting - Generate comprehensive report

    Best for thorough, non-stop assessment.
    """
    try:
        click.echo(f"\n{'='*60}")
        click.echo("AI-DRIVEN AUTOMATED PENETRATION TEST")
        click.echo(f"{'='*60}")
        click.echo(f"Client: {client}")
        click.echo(f"Target: {target}")

        click.echo("\nPhases to execute:")
        click.echo("  1. Reconnaissance (information gathering)")
        click.echo("  2. Analysis (vulnerability hypothesis generation)")
        click.echo("  3. Testing (hypothesis-driven testing)")
        click.echo("  4. Exploitation (confirmed vulnerability exploitation)")
        click.echo("  5. Reporting (comprehensive report generation)")

        if not click.confirm("\nProceed with automated assessment?"):
            click.echo("Assessment cancelled")
            return

        coordinator = AIAssessmentCoordinator(client, target)

        click.echo("\nStarting assessment...")
        click.echo("This may take several minutes...\n")

        result = coordinator.run_assessment()

        click.echo(f"\n{'='*60}")
        click.echo("ASSESSMENT COMPLETE")
        click.echo(f"{'='*60}")
        click.echo(f"\nResults saved to: {coordinator.results_dir}")
        click.echo(f"Summary: {json.dumps(coordinator.get_summary(), indent=2)}")

    except Exception as e:
        click.echo(f"\n✗ Error: {e}", err=True)
        raise click.Abort()


@ai_commands.command()
@click.option("--assessment-id", required=True, help="Assessment ID")
@click.option("--results-dir", type=click.Path(), default="assessments", help="Results directory")
def analyze_results(assessment_id: str, results_dir: str):
    """Analyze and display assessment results"""
    try:
        results_path = Path(results_dir) / assessment_id / "assessment_state.json"

        if not results_path.exists():
            click.echo(f"✗ Results not found: {results_path}", err=True)
            raise click.Abort()

        with open(results_path) as f:
            results = json.load(f)

        click.echo(f"\n{'='*60}")
        click.echo("ASSESSMENT RESULTS")
        click.echo(f"{'='*60}")
        click.echo(f"Assessment ID: {assessment_id}")
        click.echo(f"Status: {results['status']}")
        click.echo(f"Start Time: {results['start_time']}")

        if "result" in results and "findings" in results["result"]:
            findings = results["result"]["findings"]
            click.echo(f"\nFindings by Severity:")

            severity_counts = {}
            for finding in findings:
                severity = finding.get("severity", "Unknown")
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

            for severity, count in sorted(severity_counts.items()):
                click.echo(f"  {severity}: {count}")

        click.echo(f"\nFull results: {results_path}")

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@ai_commands.command()
@click.option("--target", required=True, help="Target URL")
@click.option("--quick", is_flag=True, help="Quick analysis (reduced depth)")
def reconnaissance(target: str, quick: bool):
    """AI-guided reconnaissance

    Get Claude's recommendations on reconnaissance techniques
    for your specific target.
    """
    try:
        coordinator = AIAssessmentCoordinator("Reconnaissance Only", target)

        prompt = f"""
        I need to perform reconnaissance on {target}.

        Please provide:
        1. Information gathering techniques
        2. Technology identification methods
        3. API endpoint discovery approaches
        4. JavaScript file extraction methods
        5. Security header analysis

        Be specific and tactical.
        """

        response = coordinator._chat_with_claude([], prompt)

        click.echo(f"\n{'='*60}")
        click.echo("RECONNAISSANCE GUIDANCE")
        click.echo(f"{'='*60}")
        click.echo(f"Target: {target}\n")
        click.echo(response)

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@ai_commands.command()
@click.option("--target", required=True, help="Target URL")
@click.option("--findings", type=click.Path(exists=True), required=True, help="JSON file with findings")
def exploit_strategy(target: str, findings: str):
    """Get AI-guided exploitation strategy

    Provide your reconnaissance findings and get Claude's
    exploitation strategy.
    """
    try:
        with open(findings) as f:
            findings_data = json.load(f)

        coordinator = AIAssessmentCoordinator("Exploitation Strategy", target)

        prompt = f"""
        Based on these findings from {target}:

        {json.dumps(findings_data, indent=2)}

        Provide a detailed exploitation strategy:
        1. Prioritize findings by exploitability
        2. Identify chaining opportunities
        3. Provide step-by-step exploitation for each
        4. Explain how to gather proof of concept
        5. Suggest business impact demonstration
        """

        response = coordinator._chat_with_claude([], prompt)

        click.echo(f"\n{'='*60}")
        click.echo("EXPLOITATION STRATEGY")
        click.echo(f"{'='*60}")
        click.echo(f"Target: {target}\n")
        click.echo(response)

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@ai_commands.command()
@click.option("--findings-file", type=click.Path(exists=True), required=True, help="JSON findings file")
@click.option("--output", type=click.Path(), help="Output file for report")
def generate_report(findings_file: str, output: Optional[str]):
    """Generate comprehensive report from findings"""
    try:
        with open(findings_file) as f:
            findings = json.load(f)

        coordinator = AIAssessmentCoordinator("Report Generation", "N/A")

        prompt = f"""
        Generate a professional penetration testing report for these findings:

        {json.dumps(findings, indent=2)}

        Include:
        1. Executive Summary
        2. Detailed Findings (by severity)
        3. Risk Assessment
        4. Remediation Roadmap
        5. Compliance Mapping (OWASP, NIST, PCI-DSS)

        Format as JSON with all sections.
        """

        response = coordinator._chat_with_claude([], prompt)
        report = json.loads(response)

        output_file = Path(output) if output else Path("generated_report.json")

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        click.echo(f"✓ Report generated: {output_file}")

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    ai_commands()
