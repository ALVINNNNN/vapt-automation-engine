"""
AI Assessment Coordinator

Orchestrates AI-driven penetration testing with Claude integration.
Manages assessment workflow and coordinates between modules.
"""

import logging
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class AIAssessmentCoordinator:
    """
    Coordinates AI-driven penetration testing assessments.

    Features:
    - Manages Claude AI client
    - Orchestrates assessment workflow
    - Handles tool integration
    - Manages findings and evidence
    - Generates reports
    """

    def __init__(self, client_name: str, target_url: str, api_key: Optional[str] = None):
        """Initialize coordinator"""
        self.client_name = client_name
        self.target_url = target_url
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.assessment_id = f"ai-pentest-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.results_dir = Path(f"assessments/{self.assessment_id}")
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Claude client
        self.claude_client = self._init_claude_client()

        # Assessment state
        self.assessment_state = {
            "status": "initialized",
            "start_time": datetime.now().isoformat(),
            "phases": {},
            "findings": [],
            "evidence": [],
        }

    def _init_claude_client(self):
        """Initialize Claude API client"""
        try:
            import anthropic
            return anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package required: pip install anthropic")

    def run_assessment(self) -> Dict[str, Any]:
        """Run complete AI-driven assessment"""
        logger.info(f"Starting AI assessment: {self.assessment_id}")
        logger.info(f"Target: {self.target_url}")
        logger.info(f"Client: {self.client_name}")

        # Run async assessment in event loop
        try:
            result = asyncio.run(self._run_async_assessment())
            return result
        except Exception as e:
            logger.error(f"Assessment failed: {e}", exc_info=True)
            self.assessment_state["status"] = "failed"
            self.assessment_state["error"] = str(e)
            self._save_state()
            raise

    async def _run_async_assessment(self) -> Dict[str, Any]:
        """Run assessment asynchronously"""
        from .ai_assessor import AIAssessor

        assessor = AIAssessor(self.client_name, self.target_url, self.api_key)
        assessor.set_claude_client(self.claude_client)

        # Run assessment phases
        result = await assessor.start_assessment()

        # Save results
        self.assessment_state["status"] = "completed"
        self.assessment_state["result"] = result
        self.assessment_state["summary"] = assessor.get_assessment_summary()
        self._save_state()

        logger.info("Assessment completed successfully")
        return result

    def run_interactive_assessment(self) -> Dict[str, Any]:
        """Run interactive assessment with Claude reasoning"""
        logger.info("Starting interactive AI assessment")

        conversation_history = []
        findings = []

        # Phase 1: Initial reconnaissance with Claude
        print("\n" + "="*60)
        print("PHASE 1: Interactive Reconnaissance")
        print("="*60)

        recon_prompt = f"""
        I need to perform a black-box penetration test on {self.target_url}.

        Please help me with reconnaissance by:
        1. Identifying what to test first
        2. Suggesting discovery methods
        3. Analyzing technology stack clues
        4. Recommending endpoint enumeration approach
        5. Suggesting JavaScript analysis techniques

        Be specific and tactical.
        """

        recon_response = self._chat_with_claude(conversation_history, recon_prompt)
        print("\nReconnaissance Strategy:")
        print(recon_response)

        # Phase 2: API endpoint analysis
        print("\n" + "="*60)
        print("PHASE 2: Endpoint Analysis")
        print("="*60)

        endpoint_prompt = """
        Based on your reconnaissance strategy, what specific API endpoints
        should I test first? For each endpoint, provide:
        1. Expected endpoint path/URL
        2. HTTP method to try
        3. Likely parameters
        4. Vulnerability indicators to look for
        5. Testing approach
        """

        endpoint_response = self._chat_with_claude(conversation_history, endpoint_prompt)
        print("\nEndpoint Testing Strategy:")
        print(endpoint_response)

        # Phase 3: JavaScript analysis
        print("\n" + "="*60)
        print("PHASE 3: JavaScript Analysis")
        print("="*60)

        js_prompt = """
        What JavaScript patterns should I look for that might indicate vulnerabilities?
        1. Common security anti-patterns
        2. Where to find hardcoded secrets
        3. API keys/tokens in code
        4. Logic flaws to identify
        5. Client-side validation bypasses
        """

        js_response = self._chat_with_claude(conversation_history, js_prompt)
        print("\nJavaScript Analysis Guidance:")
        print(js_response)

        # Phase 4: Vulnerability hypotheses
        print("\n" + "="*60)
        print("PHASE 4: Vulnerability Hypotheses")
        print("="*60)

        hypothesis_prompt = """
        Based on what we've discussed, what are the top 5 vulnerability hypotheses
        for this application? For each, provide:
        1. Vulnerability type (IDOR, SQL Injection, Auth bypass, etc.)
        2. Why it's likely based on what we found
        3. Exact testing steps
        4. Expected evidence if vulnerable
        5. Business impact if true
        """

        hypothesis_response = self._chat_with_claude(
            conversation_history,
            hypothesis_prompt
        )
        print("\nTop Vulnerability Hypotheses:")
        print(hypothesis_response)
        findings.append({
            "phase": "hypotheses",
            "content": hypothesis_response,
            "timestamp": datetime.now().isoformat()
        })

        # Phase 5: Exploitation strategy
        print("\n" + "="*60)
        print("PHASE 5: Exploitation Strategy")
        print("="*60)

        exploit_prompt = """
        For the most likely vulnerabilities, provide detailed exploitation steps:
        1. Exact payloads or requests to send
        2. Where to intercept/modify requests
        3. How to chain vulnerabilities
        4. How to demonstrate business impact
        5. How to gather proof of concept
        """

        exploit_response = self._chat_with_claude(
            conversation_history,
            exploit_prompt
        )
        print("\nExploitation Guidance:")
        print(exploit_response)
        findings.append({
            "phase": "exploitation",
            "content": exploit_response,
            "timestamp": datetime.now().isoformat()
        })

        # Save conversation and findings
        self._save_interactive_results(conversation_history, findings)

        return {
            "assessment_id": self.assessment_id,
            "status": "interactive_completed",
            "findings_count": len(findings),
            "results_file": str(self.results_dir / "interactive_assessment.json")
        }

    def _chat_with_claude(self, conversation_history: List[Dict], prompt: str) -> str:
        """Send message to Claude and get response"""
        conversation_history.append({
            "role": "user",
            "content": prompt
        })

        response = self.claude_client.messages.create(
            model="claude-opus-5",
            max_tokens=2048,
            system="""You are an expert penetration tester and security researcher.
            Provide specific, actionable advice for black-box testing.
            Focus on practical testing techniques, endpoint discovery, and vulnerability patterns.
            Always explain your reasoning and the indicators you're looking for.""",
            messages=conversation_history
        )

        assistant_message = response.content[0].text
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def _save_interactive_results(self, history: List[Dict], findings: List[Dict]) -> None:
        """Save interactive assessment results"""
        results_file = self.results_dir / "interactive_assessment.json"

        with open(results_file, "w") as f:
            json.dump({
                "assessment_id": self.assessment_id,
                "client": self.client_name,
                "target": self.target_url,
                "mode": "interactive",
                "timestamp": datetime.now().isoformat(),
                "conversation_turns": len(history) // 2,
                "conversation_history": history,
                "findings": findings,
            }, f, indent=2)

        logger.info(f"Results saved to {results_file}")

    def _save_state(self) -> None:
        """Save assessment state"""
        state_file = self.results_dir / "assessment_state.json"

        with open(state_file, "w") as f:
            # Convert datetime objects to strings
            state_copy = json.loads(json.dumps(self.assessment_state, default=str))
            json.dump(state_copy, f, indent=2)

    def get_summary(self) -> Dict[str, Any]:
        """Get assessment summary"""
        return {
            "assessment_id": self.assessment_id,
            "client": self.client_name,
            "target": self.target_url,
            "status": self.assessment_state["status"],
            "start_time": self.assessment_state["start_time"],
            "results_directory": str(self.results_dir),
            "findings_count": len(self.assessment_state.get("findings", [])),
        }


# Convenience function for quick interactive assessment
def quick_ai_assessment(client_name: str, target_url: str) -> Dict[str, Any]:
    """Quick interactive AI assessment"""
    coordinator = AIAssessmentCoordinator(client_name, target_url)
    return coordinator.run_interactive_assessment()


# Convenience function for full automated assessment
def automated_ai_assessment(client_name: str, target_url: str) -> Dict[str, Any]:
    """Automated AI-driven assessment"""
    coordinator = AIAssessmentCoordinator(client_name, target_url)
    return coordinator.run_assessment()
