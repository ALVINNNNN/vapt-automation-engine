"""
Bug Bounty Hunting CLI

Commands for bug bounty hunting with YesWeHack integration.
"""

import click
import json
import logging
from pathlib import Path
from typing import Optional
import asyncio

from .yeswehack_integration import YesWeHackIntegration
from .bug_hunter import BugHunter

logger = logging.getLogger(__name__)


@click.group()
def bug_bounty_commands():
    """Bug bounty hunting and vulnerability research commands"""
    pass


@bug_bounty_commands.command()
@click.option("--client", required=True, help="Client/target name")
@click.option("--target", required=True, help="Target URL")
@click.option("--output-dir", type=click.Path(), help="Output directory")
def hunt(client: str, target: str, output_dir: Optional[str]):
    """Hunt for bug bounty vulnerabilities using YesWeHack data

    This command:
    1. Analyzes target technology stack
    2. Uses Claude + YesWeHack data to identify high-value bugs
    3. Prioritizes by bounty potential (ROI)
    4. Hunts for vulnerabilities systematically
    5. Generates hunting report with findings

    Focus: Medium-High impact ($1000-$5000+ bounties)
    """
    try:
        click.echo(f"\n{'='*60}")
        click.echo("BUG BOUNTY HUNTING MODE")
        click.echo(f"{'='*60}")
        click.echo(f"Target: {target}")
        click.echo(f"Client: {client}")

        # Initialize YesWeHack integration
        click.echo("\nLoading bug bounty data from YesWeHack...")
        yeswehack = YesWeHackIntegration()
        reports = yeswehack.fetch_recent_reports(limit=50)
        patterns = yeswehack.extract_patterns()

        click.echo(f"✓ Loaded {len(reports)} bug reports")
        click.echo(f"✓ Extracted {len(patterns['vulnerability_types'])} vulnerability patterns")

        # Show summary
        summary = yeswehack.generate_summary()
        click.echo(f"\nBug Bounty Data Summary:")
        click.echo(f"  Total Potential Bounty: ${summary['total_potential_bounty']:,}")
        click.echo(f"  Average Bounty: ${summary['average_bounty']:.0f}")
        click.echo(f"  High-Impact Findings: {summary['high_impact_findings']}")

        # Initialize Claude client
        click.echo("\nInitializing Claude AI bug hunter...")
        try:
            import anthropic
            import os
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")
            claude_client = anthropic.Anthropic(api_key=api_key)
        except Exception as e:
            click.echo(f"✗ Error initializing Claude: {e}", err=True)
            raise click.Abort()

        # Start hunting
        click.echo(f"\nStarting bug hunt on {target}...")
        click.echo("(This may take several minutes as Claude analyzes the target)\n")

        hunter = BugHunter(client, target, claude_client, yeswehack)

        # Run async hunting
        result = asyncio.run(hunter.start_hunting())

        # Display results
        click.echo(f"\n{'='*60}")
        click.echo("HUNTING COMPLETE")
        click.echo(f"{'='*60}")

        summary = result.get("summary", {})
        click.echo(f"\nFindings Summary:")
        click.echo(f"  Vulnerabilities Hunted: {summary.get('total_hunted', 0)}")
        click.echo(f"  Confirmed Findings: {summary.get('confirmed_findings', 0)}")
        click.echo(f"  Potential Bounty: ${summary.get('potential_bounty', 0):,}")
        click.echo(f"  Hunting Efficiency: {summary.get('hunting_efficiency', 0):.1%}")

        if result.get("findings"):
            click.echo(f"\nTop Findings:")
            for finding in result.get("findings", [])[:5]:
                click.echo(f"  • {finding.get('vulnerability', 'Unknown')}")
                click.echo(f"    Bounty: ${finding.get('bounty_estimate', 0)}")
                click.echo(f"    Impact: {finding.get('type', 'Unknown')}")

        click.echo(f"\nFull report: {hunter.results_dir / 'hunting_report.json'}")

    except Exception as e:
        click.echo(f"\n✗ Error: {e}", err=True)
        raise click.Abort()


@bug_bounty_commands.command()
@click.option("--min-bounty", type=int, default=1000, help="Minimum bounty to show")
@click.option("--sort-by", type=click.Choice(["bounty", "impact", "frequency"]), default="bounty")
def top_findings(min_bounty: int, sort_by: str):
    """Show top bug bounty findings from YesWeHack

    Displays high-impact vulnerabilities worth hunting for.
    """
    try:
        click.echo(f"\n{'='*60}")
        click.echo("TOP BUG BOUNTY FINDINGS")
        click.echo(f"{'='*60}\n")

        yeswehack = YesWeHackIntegration()
        reports = yeswehack.fetch_recent_reports()
        high_impact = yeswehack.get_high_impact_findings(min_bounty=min_bounty)

        if sort_by == "bounty":
            high_impact.sort(key=lambda x: x.bounty_amount or 0, reverse=True)
        elif sort_by == "impact":
            high_impact.sort(key=lambda x: x.cvss_score or 0, reverse=True)

        for i, report in enumerate(high_impact[:10], 1):
            click.echo(f"{i}. {report.title}")
            click.echo(f"   Type: {report.vulnerability_type}")
            click.echo(f"   Bounty: ${report.bounty_amount}")
            click.echo(f"   Severity: {report.severity}")
            click.echo(f"   Discovery: {report.discovery_method}")
            click.echo(f"   Impact: {report.impact[:80]}...")
            click.echo()

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@bug_bounty_commands.command()
@click.option("--tech-stack", multiple=True, required=True, help="Technology (e.g., React, Node.js, Django)")
def tech_checklist(tech_stack: tuple):
    """Generate testing checklist for technology stack

    Shows vulnerabilities commonly found in this tech stack
    based on bug bounty data.
    """
    try:
        click.echo(f"\n{'='*60}")
        click.echo("TECH STACK VULNERABILITY CHECKLIST")
        click.echo(f"{'='*60}\n")
        click.echo(f"Technologies: {', '.join(tech_stack)}\n")

        yeswehack = YesWeHackIntegration()
        yeswehack.fetch_recent_reports()

        checklist = yeswehack.get_testing_checklist(list(tech_stack))

        for priority, items in checklist.items():
            priority_display = priority.replace("_", " ").upper()
            click.echo(f"\n{priority_display} PRIORITY:")
            click.echo("=" * 50)

            for item in items[:5]:
                click.echo(f"\n✓ {item['vulnerability']}")
                click.echo(f"  Type: {item['type']}")
                click.echo(f"  Bounty: ${item['expected_bounty']}")
                click.echo(f"  Discovery: {item['discovery_method']}")
                click.echo(f"  Quick Test:")
                for step in item['steps'][:2]:
                    click.echo(f"    - {step}")

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@bug_bounty_commands.command()
@click.option("--type", "vuln_type", required=True, help="Vulnerability type")
def exploitation_guide(vuln_type: str):
    """Get detailed exploitation guide for vulnerability type

    Shows step-by-step exploitation from bug bounty reports.
    """
    try:
        click.echo(f"\n{'='*60}")
        click.echo("EXPLOITATION GUIDE")
        click.echo(f"{'='*60}\n")

        yeswehack = YesWeHackIntegration()
        yeswehack.fetch_recent_reports()

        guide = yeswehack.get_exploitation_guide(vuln_type)

        if not guide:
            click.echo(f"✗ No guide found for: {vuln_type}", err=True)
            raise click.Abort()

        click.echo(f"Vulnerability: {guide['title']}\n")
        click.echo(f"Description:")
        click.echo(f"{guide['description']}\n")

        click.echo(f"Business Impact:")
        click.echo(f"{guide['impact']}\n")

        click.echo(f"Exploitation Steps:")
        for i, step in enumerate(guide['steps'], 1):
            click.echo(f"{i}. {step}")

        click.echo(f"\nRemediation:")
        click.echo(f"{guide['remediation']}\n")

        if guide['similar_findings']:
            click.echo(f"Similar Findings in Bug Bounties:")
            for finding in guide['similar_findings'][:3]:
                click.echo(f"  • {finding}")

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@bug_bounty_commands.command()
def vulnerability_patterns():
    """Show common vulnerability patterns from bug bounties

    Displays the most frequently reported vulnerabilities
    and their average bounty values.
    """
    try:
        click.echo(f"\n{'='*60}")
        click.echo("COMMON VULNERABILITY PATTERNS")
        click.echo(f"{'='*60}\n")

        yeswehack = YesWeHackIntegration()
        yeswehack.fetch_recent_reports()
        patterns = yeswehack.extract_patterns()

        vuln_types = patterns.get('vulnerability_types', {})
        sorted_types = sorted(vuln_types.items(), key=lambda x: x[1]['count'], reverse=True)

        click.echo("Most Common Vulnerability Types:\n")

        for vuln_type, data in sorted_types[:10]:
            examples = data.get('examples', [])
            avg_bounty = sum(e.get('bounty', 0) for e in examples) / len(examples) if examples else 0

            click.echo(f"• {vuln_type}")
            click.echo(f"  Found: {data['count']} times")
            click.echo(f"  Avg Bounty: ${avg_bounty:.0f}")
            click.echo(f"  Examples:")
            for example in examples[:2]:
                click.echo(f"    - {example['title'][:60]}...")
            click.echo()

        click.echo("\nDiscovery Methods:")
        discovery_methods = patterns.get('discovery_methods', {})
        for method, data in sorted(discovery_methods.items(), key=lambda x: x[1]['count'], reverse=True)[:5]:
            click.echo(f"  • {method}: {data['count']} findings")

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    bug_bounty_commands()
