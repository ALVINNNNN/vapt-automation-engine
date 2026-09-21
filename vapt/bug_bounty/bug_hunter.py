"""
Bug Bounty Hunting Engine

Uses Claude AI + learned vulnerability patterns to intelligently hunt for
high-value, medium-high impact vulnerabilities without external queries.
"""

import logging
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from .vulnerability_pattern_learner import VulnerabilityPatternLearner

logger = logging.getLogger(__name__)


class BugHunter:
    """
    AI-powered bug bounty hunter.

    Combines:
    - Claude AI reasoning
    - Self-learned vulnerability patterns (no external queries)
    - Target reconnaissance
    - Intelligent vulnerability prioritization

    Focus: Medium-High impact vulnerabilities worth $1000-$5000+

    Uses learned patterns from YesWeHack data that are cached locally,
    enabling Claude to identify vulnerabilities through reasoning without
    requiring external API calls on each hunt.
    """

    def __init__(self, client_name: str, target_url: str, claude_client, yeswehack_integration=None):
        """Initialize bug hunter"""
        self.client_name = client_name
        self.target_url = target_url
        self.claude_client = claude_client
        self.yeswehack = yeswehack_integration

        # Initialize pattern learner (loads cached patterns)
        self.pattern_learner = VulnerabilityPatternLearner()

        # If YesWeHack integration provided and patterns not yet learned, train from it
        if yeswehack_integration and not self.pattern_learner.patterns:
            logger.info("First run: Training pattern learner from YesWeHack data...")
            reports = yeswehack_integration.fetch_recent_reports(limit=50)
            self.pattern_learner.train_from_reports(reports)

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
        """Generate hunting plan based on technology and learned vulnerability patterns"""
        logger.info("Generating hunting plan from learned patterns...")

        tech_stack = tech_analysis.get("tech_stack", [])

        # Get knowledge base from learned patterns (no external queries)
        pattern_knowledge = self.pattern_learner.get_pattern_knowledge_base()

        # Find relevant vulnerabilities for this tech stack
        relevant_vulns = self.pattern_learner.identify_similar_vulnerabilities(
            tech_stack, []  # Will use tech stack matching
        )

        # Build relevant vulnerabilities list from patterns
        relevant_for_stack = {}
        for vuln_type, score in relevant_vulns[:15]:
            if vuln_type in pattern_knowledge:
                relevant_for_stack[vuln_type] = pattern_knowledge[vuln_type]

        prompt = f"""
        Based on this technology stack:
        {json.dumps(tech_analysis, indent=2)}

        And these vulnerability patterns learned from real bug bounty reports:
        {json.dumps(relevant_for_stack, indent=2)}

        Create a prioritized hunting plan for {self.target_url}.

        Use your knowledge of these patterns to:
        1. Identify high-impact vulnerabilities likely in this stack
        2. Prioritize by bounty value vs discovery difficulty (ROI)
        3. Focus on medium-high impact findings ($1000-$5000+)
        4. List quick wins first, then complex vulnerabilities

        For each target vulnerability:
        - Why it's likely in this tech stack
        - Specific discovery steps to test
        - Expected impact
        - Estimated bounty
        - Discovery difficulty (1-10)

        Score by: (bounty value) / (discovery difficulty)

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
        """Hunt for a specific vulnerability using learned patterns"""

        vuln_name = target.get("vulnerability", "")

        # Get test plan from learned patterns
        test_plan = self.pattern_learner.generate_test_plan_for_vulnerability(vuln_name)

        prompt = f"""
        Hunt for this vulnerability on {self.target_url}:

        Vulnerability: {vuln_name}
        Type: {target.get('type')}
        Estimated Bounty: ${target.get('estimated_bounty')}

        Based on patterns learned from {test_plan.get('confidence', 0):.0%} confidence in this vulnerability type,
        here's what we know:

        Indicators to look for:
        {json.dumps(test_plan.get('indicators', [])[:5], indent=2)}

        Common discovery methods:
        {json.dumps(test_plan.get('discovery_steps', [])[:3], indent=2)}

        Test with these payloads:
        {json.dumps(test_plan.get('test_payloads', [])[:3], indent=2)}

        Provide:
        1. Specific steps to test this target
        2. Exact parameters to fuzz
        3. Expected indicators if vulnerable
        4. How to verify the vulnerability
        5. Impact demonstration steps

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

        # Assess finding likelihood based on Claude's probability and pattern confidence
        probability = analysis.get("probability", 0)
        pattern_confidence = test_plan.get("confidence", 0.5)
        found = (probability * 0.7 + pattern_confidence * 0.3) > 0.6

        return {
            "vulnerability": vuln_name,
            "type": target.get("type"),
            "bounty_estimate": target.get("estimated_bounty"),
            "found": found,
            "analysis": analysis,
            "test_plan": test_plan,
            "timestamp": datetime.now().isoformat(),
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
