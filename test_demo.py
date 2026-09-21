#!/usr/bin/env python3
"""
Demo script showing VAPT engine self-learning pattern system in action.
Shows what happens during a hunt without requiring actual API calls.
"""

import json
from pathlib import Path
from vapt.bug_bounty.vulnerability_pattern_learner import VulnerabilityPatternLearner

def demo_pattern_learning():
    """Demonstrate the pattern learning system"""

    print("\n" + "="*70)
    print("VAPT ENGINE - SELF-LEARNING PATTERN SYSTEM DEMO")
    print("="*70)

    # Load learned patterns
    print("\n[1] Loading Learned Vulnerability Patterns...")
    learner = VulnerabilityPatternLearner()

    if not learner.patterns:
        print("  ✗ No patterns trained yet. Run: python -m vapt.bug_bounty.bug_bounty_cli train")
        return

    print(f"  ✓ Loaded {len(learner.patterns)} vulnerability patterns")

    # Show pattern summary
    summary = learner.get_pattern_summary()
    print(f"\n[2] Pattern Knowledge Base Summary:")
    print(f"  - Patterns Learned: {summary['patterns_learned']}")
    print(f"  - Total Bounty Covered: ${summary['total_bounty_covered']:,.0f}")
    print(f"  - Avg Confidence: {summary['avg_pattern_confidence']:.0%}")
    print(f"  - Total Training Examples: {summary['total_examples']}")

    # Show specific pattern details
    print(f"\n[3] Example Pattern - IDOR (Insecure Direct Object References):")

    for vuln_type, pattern in learner.patterns.items():
        if "idor" in vuln_type.lower():
            print(f"\n  Pattern: {pattern.vulnerability_type}")
            print(f"  Description: {pattern.description[:150]}...")

            print(f"\n  Indicators (signs this exists):")
            for ind in pattern.indicators[:3]:
                print(f"    • {ind}")

            print(f"\n  Discovery Methods:")
            for method in pattern.discovery_methods[:2]:
                print(f"    • {method}")

            print(f"\n  Common Endpoints:")
            for ep in pattern.affected_endpoints[:3]:
                print(f"    • {ep}")

            print(f"\n  Test Payloads:")
            for payload in pattern.payload_examples[:3]:
                print(f"    • {payload}")

            print(f"\n  Expected Bounty: ${pattern.average_bounty:,.0f}")
            print(f"  Confidence: {pattern.confidence_score:.0%}")
            print(f"  Learned From: {pattern.examples_count} real reports")
            break

    # Simulate target analysis
    print(f"\n[4] Simulated Target Analysis - epayment.ocbc.com:")
    target_tech = ["React", "Node.js", "MongoDB", "Express"]
    print(f"  Technology Stack Detected: {', '.join(target_tech)}")

    # Find relevant vulnerabilities for this stack
    print(f"\n[5] Identifying Relevant Vulnerabilities for Target Tech Stack:")
    relevant = learner.identify_similar_vulnerabilities(target_tech, [])

    for vuln_type, score in relevant[:5]:
        print(f"  • {vuln_type}")
        print(f"    Relevance Score: {score:.2f}")

        if vuln_type in learner.patterns:
            pattern = learner.patterns[vuln_type]
            print(f"    Est. Bounty: ${pattern.average_bounty:,.0f}")
            print(f"    Confidence: {pattern.confidence_score:.0%}")
            print()

    # Show test plans
    print(f"\n[6] Example Test Plan Generated:")
    test_plan = learner.generate_test_plan_for_vulnerability("Insecure Direct Object References (IDOR)")

    if test_plan:
        print(f"  Vulnerability: {test_plan['vulnerability']}")
        print(f"  Expected Bounty: ${test_plan['expected_bounty']:,.0f}")
        print(f"  Confidence: {test_plan['confidence']:.0%}")

        print(f"\n  Test Steps:")
        for i, step in enumerate(test_plan['discovery_steps'][:3], 1):
            print(f"    {i}. {step}")

        print(f"\n  Test Payloads:")
        for payload in test_plan['test_payloads'][:3]:
            print(f"    • {payload}")

        print(f"\n  Remediation:")
        for rem in test_plan['remediation'][:2]:
            print(f"    • {rem}")

    # Show hunting workflow
    print(f"\n[7] Hunting Workflow (what would happen with real API key):")
    print("""
  Step 1: Analyze target technology stack
    → Detect: React + Node.js + MongoDB

  Step 2: Identify likely vulnerabilities using learned patterns
    → IDOR in API endpoints
    → Authentication/Authorization issues
    → NoSQL Injection in database
    → CORS misconfigurations

  Step 3: Prioritize by ROI (Bounty / Difficulty)
    1. IDOR [$2,000 bounty, easy] = $4,000/hr ROI
    2. Auth Bypass [$3,000, medium] = $3,000/hr ROI
    3. NoSQL Injection [$5,000, hard] = $1,666/hr ROI

  Step 4: Hunt systematically
    → Test /api/users/{id} for IDOR
    → Test JWT token manipulation
    → Test database query injection
    → Verify each finding with payloads

  Step 5: Generate report
    → Confirmed findings
    → Estimated bounties
    → Exploitation steps
    → Remediation guidance
    """)

    print(f"\n[8] Key Benefits of Self-Learning System:")
    print("""
  ✓ No External Queries: Uses cached patterns (fast)
  ✓ AI Reasoning: Claude reasons from learned knowledge
  ✓ Offline Capable: Works without internet after training
  ✓ Generalizable: Applies patterns to new targets
  ✓ Continuous Learning: Improves from each hunt
  ✓ Privacy: No data sent to external APIs during hunting
    """)

    print(f"\n[9] To Run Actual Hunt on epayment.ocbc.com:")
    print("""
  1. Set API key:
     export ANTHROPIC_API_KEY="sk-ant-..."

  2. Run hunt command:
     python -m vapt.bug_bounty.bug_bounty_cli hunt \\
         --client "OCBC Bank" \\
         --target "https://epayment.ocbc.com"

  3. Claude will:
     • Analyze the target
     • Use learned patterns to identify vulnerabilities
     • Prioritize by ROI
     • Generate exploitation steps
     • Create detailed report

  All using cached patterns - NO external API calls during hunt!
    """)

    print("="*70)
    print("Demo complete! System is ready for hunting.")
    print("="*70 + "\n")

if __name__ == "__main__":
    demo_pattern_learning()
