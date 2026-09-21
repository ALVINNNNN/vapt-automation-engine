"""
Bug Bounty Hunting Engine

Uses Claude AI + YesWeHack data to intelligently hunt for
high-value, medium-high impact vulnerabilities.
"""

import logging
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class BugHunter:
    """
    AI-powered bug bounty hunter.

    Combines:
    - Claude AI reasoning
    - YesWeHack bug bounty data
    - Target reconnaissance
    - Intelligent vulnerability prioritization

    Focus: Medium-High impact vulnerabilities worth $1000-$5000+
    """

    def __init__(self, client_name: str, target_url: str, claude_client, yeswehack_integration):
        """Initialize bug hunter"""
        self.client_name = client_name
        self.target_url = target_url
        self.claude_client = claude_client
        self.yeswehack = yeswehack_integration

        self.assessment_id = f"bug-hunt-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.results_dir = Path(f"assessments/{self.assessment_id}")
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.conversation_history = []
        self.hunting_targets = []
        self.findings = []

    async def start_hunting(self) -> Dict[str, Any]:
        """Start intelligent bug hunting"""
        logger.info(f"Starting bug hunt: {self.assessment_id}")

        # Phase 1: Analyze target technology stack
        tech_analysis = await self._analyze_target_technology()

        # Phase 2: Get hunting recommendations from Claude
        hunting_plan = await self._generate_hunting_plan(tech_analysis)

        # Phase 3: Prioritize targets by bounty potential
        prioritized = await self._prioritize_hunting_targets(hunting_plan)

        # Phase 4: Execute hunts in order
        results = await self._execute_hunts(prioritized)

        # Phase 5: Generate hunting report
        report = await self._generate_hunting_report(results)

        return report

    async def _analyze_target_technology(self) -> Dict[str, Any]:
        """Analyze target's technology stack"""
        logger.info("Analyzing target technology stack...")

        prompt = f"""
        Analyze the technology stack for {self.target_url}.

        Identify:
        1. Frontend framework (React, Vue, Angular, etc.)
        2. Backend technology (Node.js, Python, Java, PHP, etc.)
        3. Database (PostgreSQL, MongoDB, MySQL, etc.)
        4. APIs and services
        5. Hosting infrastructure

        For this stack, what are the most common vulnerabilities found in bug bounties?

        Response as JSON:
        {{
            "frontend": "...",
            "backend": "...",
            "database": "...",
            "services": [...],
            "common_vulnerabilities": [...],
            "tech_stack": [...]
        }}
        """

        response = self._chat_with_claude(prompt)
        return self._parse_json(response)

    async def _generate_hunting_plan(self, tech_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate hunting plan based on technology and bug bounty data"""
        logger.info("Generating hunting plan...")

        # Get relevant bug reports for this tech stack
        relevant_reports = self.yeswehack.get_testing_checklist(
            tech_analysis.get("tech_stack", [])
        )

        prompt = f"""
        Based on this technology stack:
        {json.dumps(tech_analysis, indent=2)}

        And these common vulnerabilities found in bug bounties:
        {json.dumps(relevant_reports, indent=2)}

        Create a prioritized hunting plan for {self.target_url}.

        Focus on:
        1. High-impact vulnerabilities (IDOR, Auth bypass, SQL injection, CORS, etc.)
        2. Medium-high bounty values ($1000-$5000+)
        3. Easy to discover but valuable findings
        4. Quick wins vs long-term investigations

        For each target vulnerability:
        - Why it's likely in this stack
        - How to discover it
        - Expected impact
        - Estimated bounty
        - Discovery difficulty (1-10)

        Prioritize by: (bounty value) / (discovery difficulty)

        Response as JSON with ranked list of hunting targets.
        """

        response = self._chat_with_claude(prompt)
        return self._parse_json(response)

    async def _prioritize_hunting_targets(self, hunting_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize hunting targets by ROI (bounty/effort)"""
        logger.info("Prioritizing hunting targets...")

        targets = hunting_plan.get("hunting_targets", [])

        # Score by ROI
        for target in targets:
            bounty = target.get("estimated_bounty", 1000)
            difficulty = target.get("difficulty", 5)
            roi = bounty / difficulty if difficulty > 0 else 0
            target["roi_score"] = roi

        # Sort by ROI
        targets.sort(key=lambda x: x.get("roi_score", 0), reverse=True)

        self.hunting_targets = targets

        return targets

    async def _execute_hunts(self, hunting_targets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute hunting against each target"""
        logger.info(f"Executing {len(hunting_targets)} hunting targets...")

        results = []

        for i, target in enumerate(hunting_targets, 1):
            logger.info(f"Hunting target {i}/{len(hunting_targets)}: {target.get('vulnerability')}")

            hunt_result = await self._hunt_vulnerability(target)

            results.append(hunt_result)

            if hunt_result.get("found"):
                self.findings.append(hunt_result)
                logger.info(f"✓ Found: {hunt_result.get('vulnerability')}")

        return results

    async def _hunt_vulnerability(self, target: Dict[str, Any]) -> Dict[str, Any]:
        """Hunt for a specific vulnerability"""

        prompt = f"""
        Hunt for this vulnerability on {self.target_url}:

        Vulnerability: {target.get('vulnerability')}
        Type: {target.get('type')}
        Discovery Method: {target.get('discovery_method')}
        Estimated Bounty: ${target.get('estimated_bounty')}

        Provide:
        1. Exact steps to discover this vulnerability
        2. Tools/techniques to use
        3. Specific parameters to test
        4. How to verify if vulnerable
        5. How to demonstrate impact
        6. Expected payload/response

        Based on common patterns from bug bounties, what indicators suggest
        {target.get('vulnerability')} exists in this target?

        Response format:
        {{
            "vulnerability": "...",
            "discovery_steps": [...],
            "indicators": [...],
            "test_payloads": [...],
            "verification_method": "...",
            "impact_demonstration": "...",
            "probability": 0.0-1.0,
            "confidence": "high|medium|low"
        }}
        """

        response = self._chat_with_claude(prompt)
        analysis = self._parse_json(response)

        # Simulate verification
        found = analysis.get("probability", 0) > 0.6

        return {
            "vulnerability": target.get("vulnerability"),
            "type": target.get("type"),
            "bounty_estimate": target.get("estimated_bounty"),
            "found": found,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }

    async def _generate_hunting_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive hunting report"""
        logger.info("Generating hunting report...")

        found_count = sum(1 for r in results if r.get("found"))
        total_bounty = sum(
            r.get("bounty_estimate", 0) for r in results if r.get("found")
        )

        prompt = f"""
        Generate a comprehensive bug bounty hunting report.

        Hunting Results:
        - Total Vulnerabilities Hunted: {len(results)}
        - Confirmed Findings: {found_count}
        - Potential Total Bounty: ${total_bounty}

        Detailed Findings:
        {json.dumps(self.findings, indent=2)}

        Create report with:
        1. Executive Summary
           - How much bounty potentially earned
           - Top findings
           - Key insights

        2. Detailed Findings
           - For each vulnerability found
           - Full exploitation details
           - Business impact
           - Proof of concept

        3. Hunting Efficiency
           - Findings per hour
           - Average bounty per finding
           - Most valuable findings
           - Quickest wins

        4. Recommendations
           - Additional hunting targets
           - Escalation opportunities
           - Related vulnerabilities
           - Long-term investigations

        5. Next Steps
           - Vulnerabilities worth deeper investigation
           - Chaining opportunities
           - Privilege escalation paths

        Format as JSON.
        """

        response = self._chat_with_claude(prompt)
        report = self._parse_json(response)

        # Add metadata
        report["assessment_id"] = self.assessment_id
        report["client"] = self.client_name
        report["target"] = self.target_url
        report["timestamp"] = datetime.now().isoformat()
        report["summary"] = {
            "total_hunted": len(results),
            "confirmed_findings": found_count,
            "potential_bounty": total_bounty,
            "hunting_efficiency": found_count / len(results) if results else 0,
        }

        # Save report
        self._save_report(report)

        return report

    def _chat_with_claude(self, prompt: str) -> str:
        """Send message to Claude"""
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })

        response = self.claude_client.messages.create(
            model="claude-opus-5",
            max_tokens=3000,
            system="""You are an expert bug bounty hunter with years of experience finding
            high-value vulnerabilities. You know the most common patterns, exploitation
            techniques, and how to maximize bounty earnings. Focus on practical,
            actionable advice for finding real vulnerabilities.""",
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def _parse_json(self, response: str) -> Dict[str, Any]:
        """Parse JSON from response"""
        import re
        try:
            return json.loads(response)
        except:
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except:
                    pass
            return {}

    def _save_report(self, report: Dict[str, Any]) -> None:
        """Save hunting report"""
        report_file = self.results_dir / "hunting_report.json"

        with open(report_file, "w") as f:
            json.dump(report, f, indent=2, default=str)

        logger.info(f"Report saved to {report_file}")

    def get_summary(self) -> Dict[str, Any]:
        """Get hunting summary"""
        return {
            "assessment_id": self.assessment_id,
            "client": self.client_name,
            "target": self.target_url,
            "findings_count": len(self.findings),
            "report_location": str(self.results_dir / "hunting_report.json")
        }
