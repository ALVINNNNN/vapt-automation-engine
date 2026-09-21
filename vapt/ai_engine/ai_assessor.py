"""
AI-Driven Intelligent Penetration Testing Engine

Uses Claude AI for adaptive, reasoning-based vulnerability assessment.
Performs black-box testing with intelligent reconnaissance and analysis.
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AssessmentPhase:
    """Represents a phase in the AI-driven assessment"""
    name: str
    description: str
    objectives: List[str]
    completed: bool = False
    findings: List[Dict[str, Any]] = None

    def __post_init__(self):
        if self.findings is None:
            self.findings = []


class AIAssessor:
    """
    AI-powered assessor that uses Claude for intelligent penetration testing.

    Performs:
    - Adaptive reconnaissance based on findings
    - JavaScript code analysis for vulnerabilities
    - Endpoint enumeration and pattern discovery
    - Design-based vulnerability hypothesis generation
    - Iterative testing with intelligent decision-making
    """

    def __init__(self, client_name: str, target_url: str, api_key: str):
        """Initialize AI assessor"""
        self.client_name = client_name
        self.target_url = target_url
        self.api_key = api_key

        self.assessment_id = f"ai-assess-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.assessment_dir = Path(f"assessments/{self.assessment_id}")
        self.assessment_dir.mkdir(parents=True, exist_ok=True)

        # Assessment state
        self.phases: Dict[str, AssessmentPhase] = self._init_phases()
        self.findings: List[Dict[str, Any]] = []
        self.endpoints: List[Dict[str, Any]] = []
        self.javascript_files: List[Dict[str, Any]] = []
        self.api_requests: List[Dict[str, Any]] = []
        self.reconnaissance_data: Dict[str, Any] = {}

        # AI client will be initialized separately with actual API
        self.claude_client = None
        self.conversation_history: List[Dict[str, str]] = []

    def _init_phases(self) -> Dict[str, AssessmentPhase]:
        """Initialize assessment phases"""
        return {
            "reconnaissance": AssessmentPhase(
                name="Reconnaissance",
                description="Intelligent gathering of target information",
                objectives=[
                    "Identify technology stack",
                    "Discover endpoints and API routes",
                    "Extract JavaScript files",
                    "Analyze application structure",
                    "Identify potential attack surfaces",
                ]
            ),
            "analysis": AssessmentPhase(
                name="Analysis",
                description="AI-driven analysis of gathered information",
                objectives=[
                    "Analyze JavaScript for vulnerabilities",
                    "Identify architectural weaknesses",
                    "Generate vulnerability hypotheses",
                    "Map data flows",
                    "Identify trust boundaries",
                ]
            ),
            "testing": AssessmentPhase(
                name="Testing",
                description="Intelligent hypothesis-driven testing",
                objectives=[
                    "Test identified hypotheses",
                    "Verify vulnerability assumptions",
                    "Exploit confirmed issues",
                    "Gather proof of concepts",
                    "Document evidence",
                ]
            ),
            "exploitation": AssessmentPhase(
                name="Exploitation",
                description="Attempted exploitation of discovered vulnerabilities",
                objectives=[
                    "Exploit confirmed vulnerabilities",
                    "Demonstrate business impact",
                    "Test privilege escalation",
                    "Evaluate lateral movement",
                    "Verify data access",
                ]
            ),
            "reporting": AssessmentPhase(
                name="Reporting",
                description="Generate findings and recommendations",
                objectives=[
                    "Compile all findings",
                    "Prioritize by severity",
                    "Create remediation guidance",
                    "Generate executive summary",
                    "Document proof of concepts",
                ]
            ),
        }

    def set_claude_client(self, client) -> None:
        """Set the Claude API client"""
        self.claude_client = client

    async def start_assessment(self) -> Dict[str, Any]:
        """Start the AI-driven assessment"""
        logger.info(f"Starting AI assessment: {self.assessment_id}")

        try:
            # Phase 1: Reconnaissance
            recon_findings = await self._phase_reconnaissance()

            # Phase 2: Analysis
            analysis_findings = await self._phase_analysis(recon_findings)

            # Phase 3: Testing
            test_findings = await self._phase_testing(analysis_findings)

            # Phase 4: Exploitation
            exploit_findings = await self._phase_exploitation(test_findings)

            # Phase 5: Reporting
            report_data = await self._phase_reporting(exploit_findings)

            return report_data

        except Exception as e:
            logger.error(f"Assessment error: {e}", exc_info=True)
            raise

    async def _phase_reconnaissance(self) -> Dict[str, Any]:
        """Phase 1: Intelligent Reconnaissance"""
        logger.info("Starting Reconnaissance Phase")

        phase = self.phases["reconnaissance"]
        phase.completed = True

        findings = {
            "technology_stack": await self._detect_technology_stack(),
            "javascript_files": await self._extract_javascript_files(),
            "endpoints": await self._enumerate_endpoints(),
            "api_patterns": await self._identify_api_patterns(),
            "security_headers": await self._check_security_headers(),
            "frontend_structure": await self._analyze_frontend_structure(),
        }

        self.reconnaissance_data = findings
        phase.findings = [{"type": k, "data": v} for k, v in findings.items()]

        logger.info(f"Reconnaissance complete: Found {len(findings)} data categories")
        return findings

    async def _detect_technology_stack(self) -> Dict[str, List[str]]:
        """Use AI to detect technology stack from target"""

        prompt = f"""
        Analyze the web application at {self.target_url} and identify:
        1. Frontend framework (React, Vue, Angular, etc.)
        2. Backend framework/language (Python, Node.js, Java, PHP, etc.)
        3. APIs and third-party services
        4. Databases (if identifiable)
        5. Infrastructure (CDN, hosting provider, etc.)

        For each technology, explain how you identified it and what attack vectors it might present.

        Response format:
        {{
            "frameworks": [...],
            "languages": [...],
            "databases": [...],
            "services": [...],
            "infrastructure": [...],
            "identified_by": {{...}},
            "potential_vulnerabilities": {{...}}
        }}
        """

        response = await self._ask_claude(prompt)
        return self._parse_json_response(response)

    async def _extract_javascript_files(self) -> List[Dict[str, Any]]:
        """Intelligently extract and analyze JavaScript files"""

        prompt = f"""
        Identify all JavaScript files loaded by {self.target_url}.

        For each JS file found:
        1. Extract the URL/path
        2. Identify purpose (framework, utility, business logic, etc.)
        3. Look for:
           - API endpoints in the code
           - Secret handling (API keys, tokens)
           - Authentication mechanisms
           - Data processing logic
           - Business logic vulnerabilities
           - CORS/CSRF patterns
           - Client-side validation
           - Hidden features or debug code

        Also perform static analysis looking for:
        - Hardcoded credentials
        - Exposed sensitive data
        - Weak cryptography
        - Potential injection points
        - Information disclosure

        Response format:
        {{
            "javascript_files": [
                {{
                    "url": "...",
                    "type": "framework|utility|business-logic",
                    "size": 0,
                    "minified": true/false,
                    "key_functions": [...],
                    "api_endpoints": [...],
                    "vulnerabilities": [...],
                    "interesting_patterns": [...]
                }}
            ],
            "global_objects": [...],
            "exposed_functions": [...],
            "configuration": {{...}}
        }}
        """

        response = await self._ask_claude(prompt)
        js_data = self._parse_json_response(response)

        self.javascript_files = js_data.get("javascript_files", [])
        return self.javascript_files

    async def _enumerate_endpoints(self) -> List[Dict[str, Any]]:
        """Intelligently enumerate API endpoints and routes"""

        # Combine sources for endpoint discovery
        prompt = f"""
        Enumerate all API endpoints and routes for {self.target_url}.

        Use multiple discovery methods:
        1. Extract from JavaScript files
        2. Network traffic analysis (API calls during normal usage)
        3. Common patterns (REST, GraphQL, RPC)
        4. Robots.txt and sitemap.xml
        5. Source map analysis (if available)
        6. Error messages and stack traces

        For each endpoint found, identify:
        - HTTP method (GET, POST, PUT, DELETE, etc.)
        - Path and query parameters
        - Required/optional headers
        - Request/response format (JSON, XML, etc.)
        - Authentication requirements
        - Purpose and functionality
        - Rate limiting (if observable)
        - Error responses

        Prioritize by:
        1. Sensitivity (user data, authentication, admin functions)
        2. Attack potential
        3. Unusual patterns

        Response format:
        {{
            "endpoints": [
                {{
                    "method": "GET|POST|PUT|DELETE",
                    "path": "/api/...",
                    "parameters": [...],
                    "required_auth": true/false,
                    "purpose": "...",
                    "sensitivity": "high|medium|low",
                    "potential_issues": [...]
                }}
            ],
            "patterns": [...],
            "authentication_types": [...]
        }}
        """

        response = await self._ask_claude(prompt)
        endpoint_data = self._parse_json_response(response)

        self.endpoints = endpoint_data.get("endpoints", [])
        return self.endpoints

    async def _identify_api_patterns(self) -> Dict[str, Any]:
        """Identify API patterns and security issues"""

        prompt = f"""
        Analyze the API patterns for {self.target_url}.

        Look for:
        1. Authentication mechanisms (JWT, sessions, API keys, OAuth, etc.)
        2. Authorization patterns (RBAC, ABAC, attribute-based)
        3. Input validation patterns (or lack thereof)
        4. Rate limiting and abuse protection
        5. CORS configuration
        6. API versioning
        7. Error handling and information disclosure
        8. Idempotency and transaction handling

        Identify potential vulnerabilities based on patterns:
        - Missing authentication on sensitive endpoints
        - Broken authorization (privilege escalation, IDOR)
        - Insufficient input validation
        - No rate limiting (brute force, DoS risks)
        - Overly permissive CORS
        - Information disclosure through errors
        - Race conditions in transactional operations

        Response format:
        {{
            "auth_mechanisms": [...],
            "authorization_models": [...],
            "security_patterns": {{...}},
            "anti_patterns": [...],
            "vulnerability_indicators": [...]
        }}
        """

        response = await self._ask_claude(prompt)
        return self._parse_json_response(response)

    async def _check_security_headers(self) -> Dict[str, List[str]]:
        """Analyze security headers"""

        prompt = f"""
        Analyze security headers for {self.target_url}.

        Check for:
        1. Content-Security-Policy (CSP)
        2. X-Frame-Options
        3. X-Content-Type-Options
        4. Strict-Transport-Security (HSTS)
        5. X-XSS-Protection
        6. Referrer-Policy
        7. Permissions-Policy
        8. Server header information

        For each header:
        - Note if present or missing
        - Evaluate configuration strength
        - Identify bypasses or weaknesses

        Response format:
        {{
            "headers": {{
                "present": [...],
                "missing": [...],
                "weak": [...]
            }},
            "vulnerabilities": [...],
            "recommendations": [...]
        }}
        """

        response = await self._ask_claude(prompt)
        return self._parse_json_response(response)

    async def _analyze_frontend_structure(self) -> Dict[str, Any]:
        """Analyze frontend code structure and architecture"""

        prompt = f"""
        Analyze the frontend architecture of {self.target_url}.

        Examine:
        1. Component structure and data flow
        2. State management (Redux, Vuex, React Context, etc.)
        3. API communication patterns
        4. Authentication token handling
        5. Session management
        6. Error handling and logging
        7. Client-side validation
        8. Feature flags and debug modes

        Identify architectural vulnerabilities:
        - Trusting client-side validation
        - Exposing sensitive data in state
        - Weak token/session handling
        - Unencrypted data storage
        - Debug features in production
        - Insecure logging

        Response format:
        {{
            "architecture": "...",
            "state_management": "...",
            "data_flows": [...],
            "security_issues": [...],
            "attack_scenarios": [...]
        }}
        """

        response = await self._ask_claude(prompt)
        return self._parse_json_response(response)

    async def _phase_analysis(self, recon_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: AI-driven Analysis of Reconnaissance Data"""
        logger.info("Starting Analysis Phase")

        phase = self.phases["analysis"]
        phase.completed = True

        prompt = f"""
        You are a world-class security researcher analyzing a penetration test.

        RECONNAISSANCE DATA:
        {json.dumps(recon_data, indent=2)}

        Perform deep analysis to:

        1. IDENTIFY VULNERABILITY HYPOTHESES
           - Based on technology stack, what are likely vulnerabilities?
           - What design patterns indicate specific risks?
           - Are there common misconfigurations?

        2. THREAT MODELING
           - Who are the threat actors?
           - What are their likely motivations?
           - What data would they target?
           - What attack paths are most likely?

        3. ARCHITECTURE ANALYSIS
           - What are the trust boundaries?
           - Where are the authentication gates?
           - How is data validated?
           - What assumptions are made about security?

        4. ENDPOINT RISK ASSESSMENT
           - Rank endpoints by risk
           - Identify IDOR candidates
           - Find broken authorization patterns
           - Spot missing authentication
           - Identify injection points

        5. JAVASCRIPT CODE REVIEW
           - Identify logic flaws
           - Find hardcoded credentials or secrets
           - Spot information disclosure
           - Analyze encryption/hashing implementations

        6. API SECURITY ANALYSIS
           - Evaluate authentication robustness
           - Assess authorization implementation
           - Identify input validation gaps
           - Check for race conditions
           - Analyze error handling

        GENERATE:
        - Prioritized list of vulnerability hypotheses (high to low probability)
        - Recommended testing approach for each
        - Expected evidence/proof of concept
        - Business impact assessment

        Format as JSON.
        """

        analysis = await self._ask_claude(prompt)
        analysis_data = self._parse_json_response(analysis)

        phase.findings = analysis_data.get("vulnerabilities", [])

        return analysis_data

    async def _phase_testing(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Intelligent Hypothesis-Driven Testing"""
        logger.info("Starting Testing Phase")

        phase = self.phases["testing"]
        phase.completed = True

        prompt = f"""
        Based on this vulnerability analysis:
        {json.dumps(analysis_data, indent=2)}

        Design a testing strategy for each vulnerability hypothesis.

        For each hypothesis, provide:
        1. TEST PLAN
           - Specific steps to test
           - Tools/methods to use
           - Expected behavior if vulnerable
           - Evidence to collect

        2. EXPLOITATION APPROACH
           - How to exploit if confirmed
           - Required payloads or techniques
           - Safety considerations
           - Impact demonstration

        3. VERIFICATION
           - How to confirm the vulnerability
           - False positive detection
           - Root cause analysis

        4. PRIORITY & EFFORT
           - Likelihood of vulnerability
           - Effort required to test
           - Business impact if real
           - Recommended testing order

        Create actionable test cases.
        """

        test_plan = await self._ask_claude(prompt)
        test_data = self._parse_json_response(test_plan)

        # Execute tests and collect results
        test_results = []
        for hypothesis in test_data.get("hypotheses", []):
            result = await self._execute_hypothesis_test(hypothesis)
            test_results.append(result)

        phase.findings = test_results
        return {"tests": test_results, "analysis": test_data}

    async def _execute_hypothesis_test(self, hypothesis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific vulnerability test"""

        prompt = f"""
        Execute this test and report results:

        Vulnerability: {hypothesis.get('name', 'Unknown')}
        Test Steps: {json.dumps(hypothesis.get('test_steps', []))}
        Expected Behavior: {hypothesis.get('expected_behavior', '')}
        Target: {self.target_url}

        Perform the test and report:
        1. OBSERVED BEHAVIOR
           - What actually happened
           - Step-by-step results
           - Differences from expected

        2. VULNERABILITY CONFIRMED?
           - Yes/No/Inconclusive
           - Confidence level (0-100%)
           - Evidence

        3. PROOF OF CONCEPT
           - If vulnerable, how to reproduce
           - Required payload/steps
           - Observable evidence

        4. BUSINESS IMPACT
           - What data/functionality is affected
           - What an attacker could do
           - Risk level

        Response as JSON.
        """

        result = await self._ask_claude(prompt)
        return self._parse_json_response(result)

    async def _phase_exploitation(self, test_findings: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Phase 4: Exploitation of Confirmed Vulnerabilities"""
        logger.info("Starting Exploitation Phase")

        phase = self.phases["exploitation"]
        phase.completed = True

        confirmed_vulns = [
            v for v in test_findings.get("tests", [])
            if v.get("confirmed", False)
        ]

        exploits = []
        for vuln in confirmed_vulns:
            exploit = await self._attempt_exploitation(vuln)
            exploits.append(exploit)

        phase.findings = exploits
        return exploits

    async def _attempt_exploitation(self, vulnerability: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt exploitation of a confirmed vulnerability"""

        prompt = f"""
        Exploit this confirmed vulnerability:

        {json.dumps(vulnerability, indent=2)}

        Provide:
        1. EXPLOITATION STEPS
           - Detailed steps to exploit
           - Any tools or payloads needed
           - Expected successful outcome

        2. PROOF OF CONCEPT
           - Code/command to demonstrate
           - Observable proof
           - Verification method

        3. IMPACT DEMONSTRATION
           - What access is gained
           - What data can be accessed
           - What actions can be performed
           - Business impact

        4. CHAINING OPPORTUNITIES
           - Can this lead to other vulnerabilities?
           - Privilege escalation paths?
           - Lateral movement possibilities?

        5. REMEDIATION
           - How to fix this vulnerability
           - Temporary workarounds
           - Long-term solutions

        Format as JSON.
        """

        result = await self._ask_claude(prompt)
        return self._parse_json_response(result)

    async def _phase_reporting(self, exploit_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Phase 5: Generate Assessment Report"""
        logger.info("Starting Reporting Phase")

        phase = self.phases["reporting"]
        phase.completed = True

        # Aggregate all findings
        all_findings = []
        for phase_name, phase_obj in self.phases.items():
            all_findings.extend(phase_obj.findings)

        prompt = f"""
        Generate a comprehensive penetration testing report.

        ASSESSMENT DATA:
        - Client: {self.client_name}
        - Target: {self.target_url}
        - Assessment Type: AI-Driven Black Box
        - Assessment ID: {self.assessment_id}

        FINDINGS:
        {json.dumps(all_findings, indent=2)}

        Create a report with:

        1. EXECUTIVE SUMMARY
           - Overview of vulnerabilities found
           - Risk ratings
           - Business impact
           - Key recommendations

        2. DETAILED FINDINGS
           - For each vulnerability:
             * Description
             * CVSS score and severity
             * Proof of concept
             * Business impact
             * Remediation steps
             * References

        3. RISK ASSESSMENT
           - Prioritized by severity
           - Business impact analysis
           - Remediation timeline

        4. REMEDIATION ROADMAP
           - Priority fixes
           - Effort estimates
           - Verification steps

        5. COMPLIANCE MAPPING
           - OWASP Top 10 2021
           - NIST Framework
           - CWE/CVE references

        Format as JSON with all data.
        """

        report_data = await self._ask_claude(prompt)
        final_report = self._parse_json_response(report_data)

        # Save report
        self._save_report(final_report)

        phase.findings = final_report.get("findings", [])

        return final_report

    async def _ask_claude(self, prompt: str) -> str:
        """Send prompt to Claude and get response"""
        if not self.claude_client:
            raise RuntimeError("Claude client not initialized")

        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })

        try:
            response = self.claude_client.messages.create(
                model="claude-opus-5",
                max_tokens=4096,
                system="""You are an expert security researcher and penetration tester.
                Provide thorough, accurate security analysis. When identifying vulnerabilities,
                be specific about exploitation paths and business impact. Always format technical
                responses as valid JSON where requested.""",
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text

            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Extract and parse JSON from Claude response"""
        try:
            # Try direct JSON parsing
            return json.loads(response)
        except json.JSONDecodeError:
            # Try extracting JSON from markdown code block
            match = re.search(r"```(?:json)?\n?(.*?)\n?```", response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass

            # Try extracting JSON object
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass

            logger.warning("Could not parse JSON from response")
            return {}

    def _save_report(self, report_data: Dict[str, Any]) -> None:
        """Save assessment report to file"""
        report_file = self.assessment_dir / "assessment_report.json"

        with open(report_file, "w") as f:
            json.dump({
                "assessment_id": self.assessment_id,
                "client": self.client_name,
                "target": self.target_url,
                "timestamp": datetime.now().isoformat(),
                "report": report_data,
                "phases": {
                    name: {
                        "completed": phase.completed,
                        "findings_count": len(phase.findings)
                    }
                    for name, phase in self.phases.items()
                }
            }, f, indent=2)

        logger.info(f"Report saved to {report_file}")

    def get_assessment_summary(self) -> Dict[str, Any]:
        """Get summary of assessment"""
        return {
            "assessment_id": self.assessment_id,
            "client": self.client_name,
            "target": self.target_url,
            "phases": {
                name: {
                    "completed": phase.completed,
                    "findings": len(phase.findings)
                }
                for name, phase in self.phases.items()
            },
            "total_findings": len(self.findings),
            "javascript_files_analyzed": len(self.javascript_files),
            "endpoints_discovered": len(self.endpoints),
            "report_location": str(self.assessment_dir / "assessment_report.json")
        }
