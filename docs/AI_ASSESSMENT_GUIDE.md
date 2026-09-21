# AI-Driven Penetration Testing Guide

## Overview

The VAPT Automation Engine now includes **Claude-powered intelligent penetration testing** for adaptive, reasoning-based black-box assessments. Instead of running hardcoded tool sequences, Claude AI analyzes findings and dynamically guides the assessment.

## Key Capabilities

### 1. Intelligent Reconnaissance
- **Technology Detection**: Claude identifies tech stack from clues
- **JavaScript Analysis**: Extract and analyze all JS files for vulnerabilities
- **Endpoint Discovery**: Intelligently enumerate API routes and endpoints
- **Architecture Analysis**: Understand data flows and trust boundaries
- **Pattern Recognition**: Identify security patterns and anti-patterns

### 2. Adaptive Analysis
- **Vulnerability Hypotheses**: Generate likely vulnerabilities based on findings
- **Threat Modeling**: Understand attacker motivations and attack paths
- **Risk Assessment**: Prioritize findings by exploitability and impact
- **Chaining Analysis**: Identify vulnerability chains and escalation paths

### 3. Hypothesis-Driven Testing
- **Test Planning**: Claude designs specific tests for each hypothesis
- **Exploitation Strategy**: Provides step-by-step exploitation guidance
- **Proof of Concept**: Generate reproducible evidence
- **Impact Demonstration**: Show business consequences

### 4. Dynamic Assessment
- **Adaptive Testing**: Adjust approach based on findings
- **Follow-up Analysis**: Identify secondary vulnerabilities
- **Lateral Movement**: Suggest privilege escalation paths
- **Chain Exploitation**: Combine vulnerabilities for greater impact

## Installation

### Prerequisites

```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-api-key"
```

### Setup

```bash
cd vapt-automation-engine
pip install -e .
```

## Usage

### 1. Interactive Assessment (Recommended for Learning)

Have a real-time conversation with Claude about your target:

```bash
vapt ai interactive \
    --client "Acme Corp" \
    --target "https://app.example.com"
```

**What Happens:**
1. Claude asks what to test first
2. You get reconnaissance strategy
3. Claude recommends endpoint testing approach
4. Claude guides through vulnerability hypotheses
5. Claude explains exploitation techniques

**Best For:**
- Learning penetration testing
- Custom/unusual applications
- Educational assessments
- Complex vulnerability chains

### 2. Automated Assessment

Run full assessment automatically with AI reasoning:

```bash
vapt ai automated \
    --client "Acme Corp" \
    --target "https://app.example.com"
```

**Phases:**
1. **Reconnaissance**: Information gathering (technology, endpoints, JS files)
2. **Analysis**: Claude analyzes findings for vulnerabilities
3. **Testing**: Executes hypothesis-driven tests
4. **Exploitation**: Attempts confirmed vulnerabilities
5. **Reporting**: Generates comprehensive report

**Best For:**
- Thorough assessments without interruption
- Compliance requirements
- Trending reports
- Quick turnaround needed

### 3. Component Commands

#### Reconnaissance Guidance
```bash
vapt ai reconnaissance --target "https://app.example.com"
```
Get Claude's specific recommendations for reconnaissance on your target.

#### Endpoint Discovery
```bash
vapt ai reconnaissance \
    --target "https://app.example.com" \
    --focus endpoints
```

#### JavaScript Analysis
```bash
vapt ai reconnaissance \
    --target "https://app.example.com" \
    --focus javascript
```

#### Technology Detection
```bash
vapt ai reconnaissance \
    --target "https://app.example.com" \
    --focus technology
```

#### Exploitation Strategy
```bash
vapt ai exploit-strategy \
    --target "https://app.example.com" \
    --findings ./my-findings.json
```

Based on findings you provide, Claude creates detailed exploitation strategy.

#### Report Generation
```bash
vapt ai generate-report \
    --findings-file ./findings.json \
    --output ./comprehensive-report.json
```

Claude generates professional report from findings.

## How AI Assessment Works

### Assessment Workflow

```
┌─────────────────────────────────────────┐
│ 1. RECONNAISSANCE                       │
│ - Claude identifies tech stack          │
│ - Extracts JavaScript files             │
│ - Enumerates endpoints                  │
│ - Analyzes architecture                 │
│ - Documents patterns                    │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│ 2. ANALYSIS                             │
│ - Claude generates hypotheses            │
│ - Threat modeling                       │
│ - Risk assessment                       │
│ - Attack path identification            │
│ - Prioritizes by exploitability         │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│ 3. TESTING                              │
│ - Claude designs test cases              │
│ - Tests hypotheses                      │
│ - Verifies findings                     │
│ - Gathers evidence                      │
│ - Adjusts based on results              │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│ 4. EXPLOITATION                         │
│ - Claude provides exploit guidance       │
│ - Attempts confirmed vulnerabilities   │
│ - Demonstrates business impact         │
│ - Explores escalation paths            │
│ - Documents proof of concept           │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│ 5. REPORTING                            │
│ - Compiles all findings                 │
│ - Prioritizes by severity               │
│ - Creates remediation guidance          │
│ - Maps to compliance frameworks         │
│ - Generates executive summary           │
└─────────────────────────────────────────┘
```

### Claude's Reasoning Process

**At each step, Claude:**

1. **Analyzes** - Reviews all data collected so far
2. **Reasons** - Explains what patterns indicate
3. **Hypothesizes** - Generates likely vulnerabilities
4. **Prioritizes** - Ranks by probability and impact
5. **Recommends** - Suggests specific testing approach
6. **Adapts** - Adjusts strategy based on findings

## Real-World Example

### Scenario: Black-Box Web App Assessment

```bash
# Start interactive assessment
$ vapt ai interactive --client "Acme Corp" --target "https://app.acme.com"

============================================================
PHASE 1: Interactive Reconnaissance
============================================================
Claude: Based on the application at app.acme.com, here's my reconnaissance strategy...

[Claude provides detailed reconnaissance strategy]

============================================================
PHASE 2: Endpoint Analysis
============================================================
Claude: I've identified these key endpoints based on JavaScript analysis:
- GET /api/users/{id}           <- IDOR candidate
- POST /api/auth/login          <- Brute force target
- GET /api/admin/settings       <- Admin panel discovery
- POST /api/files/upload        <- File upload vulnerability

For each endpoint, here are the recommended testing approaches:

[Claude explains how to test each endpoint]

============================================================
PHASE 3: JavaScript Analysis
============================================================
Claude: In the main JavaScript bundle, I found:
- API key embedded in code
- Weak password validation on client
- Session token handling vulnerabilities
- Admin detection logic

Here's how to exploit each:

[Detailed exploitation guidance]

============================================================
PHASE 4: Vulnerability Hypotheses
============================================================
Claude: Based on all findings, my top 5 hypotheses:

1. IDOR in /api/users/{id}
   - Probability: 95%
   - Testing: Try accessing user 2,3,4 while logged in as user 1
   - Impact: Access to customer data

2. Weak Session Management
   - Probability: 85%
   - Testing: Check JWT, cookie attributes, token rotation
   - Impact: Session fixation, account takeover

3. Client-Side Authorization
   - Probability: 90%
   - Testing: Modify role in localStorage, access admin endpoints
   - Impact: Complete privilege escalation

[All hypotheses with testing steps]

============================================================
PHASE 5: Exploitation Guidance
============================================================
Claude: Here's how to exploit the most likely vulnerabilities:

Exploit #1: IDOR
1. Login with user account
2. Intercept /api/users/1 request
3. Change ID to 2, 3, 4... 
4. Retrieve customer data

Proof: Save responses showing different user data

Impact: Customer PII exposure, GDPR violation

[Complete exploitation walkthrough]
```

## Advanced Features

### 1. Conversation Memory

The AI assessor maintains conversation history, allowing Claude to:
- Reference previous findings
- Build on prior hypotheses
- Connect disparate vulnerabilities
- Provide contextual guidance

### 2. Evidence Collection

Automatically documents:
- Reconnaissance data
- Test results
- Exploitation evidence
- Timeline of activities

### 3. Compliance Mapping

Claude automatically maps findings to:
- OWASP Top 10
- NIST Cybersecurity Framework
- PCI-DSS requirements
- ISO 27001 controls
- CWE/CVE references

### 4. Report Generation

Creates comprehensive reports with:
- Executive summary
- Technical findings
- Risk assessment
- Remediation roadmap
- Business impact analysis

## Assessment Phases Explained

### Phase 1: Reconnaissance

**Claude analyzes:**
- Technology stack clues
- JavaScript files (frameworks, libraries, business logic)
- API patterns and endpoints
- Security headers and configurations
- Frontend architecture and data flows
- Hidden features or debug code

**Output:**
- Technology stack inventory
- JavaScript file analysis
- Endpoint enumeration
- API pattern documentation
- Security header assessment
- Frontend architecture map

### Phase 2: Analysis

**Claude reasons about:**
- What technologies indicate about likely vulnerabilities
- Common misconfigurations for detected stack
- Architectural weaknesses
- Trust boundary violations
- Data flow security implications
- Attack surface enumeration

**Output:**
- Vulnerability hypothesis list (ranked by probability)
- Threat models
- Risk assessment
- Attack path identification
- Exploitation prioritization

### Phase 3: Testing

**Claude designs and executes:**
- Specific test cases for each hypothesis
- Parameter fuzzing and manipulation
- Authentication/authorization testing
- Input validation verification
- Race condition checking
- Business logic flaw exploitation

**Output:**
- Test results for each hypothesis
- Confirmed vs. inconclusive findings
- Evidence gathered
- Exploitation proof of concept

### Phase 4: Exploitation

**Claude performs:**
- Exploitation of confirmed vulnerabilities
- Business impact demonstration
- Privilege escalation attempts
- Lateral movement exploration
- Data access verification
- Persistence exploration (if authorized)

**Output:**
- Successful exploitation proof
- Data access demonstration
- Privilege escalation results
- Business impact assessment

### Phase 5: Reporting

**Claude compiles:**
- All findings with severity ratings
- CVSS scores and risk assessment
- Remediation guidance for each
- Compliance framework mapping
- Executive summary
- Detailed technical report
- Proof of concept documentation

**Output:**
- JSON findings database
- HTML interactive report
- PDF executive summary
- Compliance mapping
- Remediation timeline

## Best Practices

### 1. Prepare the Target

```bash
# Ensure target is accessible
curl -I https://app.example.com

# Note any authentication requirements
# Document any testing windows or restrictions
```

### 2. Use Interactive Mode for Complex Apps

Interactive mode is better for:
- Custom applications
- Unusual architectures
- Educational assessments
- When you need real-time guidance

```bash
vapt ai interactive --client "Client" --target "https://app.example.com"
```

### 3. Use Automated Mode for Standard Apps

Automated mode is better for:
- Standard web applications
- Time-sensitive assessments
- Compliance requirements
- When maximum efficiency is needed

```bash
vapt ai automated --client "Client" --target "https://app.example.com"
```

### 4. Verify Claude's Findings

Always verify:
- Test all recommendations
- Confirm Claude's assumptions
- Don't blindly trust hypotheses
- Manual verification of edge cases

### 5. Document Everything

Save:
- Conversation history (auto-saved)
- Screenshots of findings
- Request/response examples
- Proof of concept code
- Timeline of activities

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY not set"

**Solution:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Or pass it in code:
coordinator = AIAssessmentCoordinator(
    "Client",
    "https://target.com",
    api_key="sk-ant-..."
)
```

### Issue: "Claude responding with non-JSON"

Claude is trained to return JSON when requested, but if parsing fails:
- Check the prompt wording
- Review the full response
- Manually extract the JSON portion
- Report to anthropic support if persistent

### Issue: "Assessment taking too long"

Claude API responses can vary:
- Network latency: Usually 1-5 seconds per request
- Complex analysis: May take 10-20 seconds
- Large responses: May take longer

**Tips:**
- Use `--quick` flag for faster but less thorough assessment
- Split assessment into smaller phases
- Run during off-peak times
- Check API status page

### Issue: "Target giving 403 Forbidden"

**Solutions:**
- Ensure you have authorization to test
- Check if target blocks automated testing
- Try with different user agent
- Verify credentials if required
- Contact client to whitelist testing IP

## Integration with Traditional Tools

AI assessment works alongside traditional tools:

```bash
# Run traditional network scan
vapt network-scan --targets targets.txt

# Then get Claude's analysis
vapt ai exploit-strategy \
    --target "https://web-app.example.com" \
    --findings ./scan-results.json

# Manual testing informed by Claude
# Then get Claude to generate report
vapt ai generate-report --findings-file findings.json
```

## Security Considerations

### Authorization

⚠️ **CRITICAL**: Only test systems you own or have written authorization to test.

```bash
# Require explicit authorization
AUTHORIZATION_REQUIRED=true vapt ai automated \
    --client "Client" \
    --target "https://app.example.com" \
    --auth-file ./pentest-agreement.pdf
```

### Data Handling

- Findings saved locally in `assessments/` directory
- Conversation history saved with assessment
- No sensitive data sent to Anthropic except what you include in prompts
- All results are encrypted at rest

### Liability

- AI assessment is a tool, not a substitute for human expertise
- Always verify Claude's findings independently
- Understand the reasoning before acting on recommendations
- Document all activities for compliance

## Example Assessment Report

Results are saved to:
```
assessments/ai-pentest-YYYYMMDD-HHMMSS/
├── assessment_state.json          # Assessment metadata
├── assessment_report.json         # Findings and analysis
├── interactive_assessment.json    # Conversation history
└── findings/
    ├── javascript-analysis.json
    ├── endpoints.json
    ├── vulnerabilities.json
    └── recommendations.json
```

## Advanced Usage

### Custom Assessment Script

```python
from vapt.ai_engine import AIAssessmentCoordinator

# Initialize
coordinator = AIAssessmentCoordinator(
    client_name="Acme Corp",
    target_url="https://app.acme.com"
)

# Run interactive assessment
result = coordinator.run_interactive_assessment()

# Access results
print(coordinator.get_summary())
```

### Integrating with CI/CD

```yaml
# .github/workflows/security-test.yml
name: AI Pentest

on: [push]

jobs:
  ai-assess:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: AI Security Assessment
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          pip install -e .
          vapt ai interactive \
            --client "CI Pipeline" \
            --target "https://staging.example.com" \
            --output-dir "./reports"
      
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: security-report
          path: reports/
```

## Summary

The AI-driven assessment mode provides:

✓ **Intelligent reconnaissance** with Claude reasoning  
✓ **Dynamic hypothesis generation** based on findings  
✓ **Adaptive testing** that adjusts based on results  
✓ **Expert guidance** on exploitation techniques  
✓ **Comprehensive reporting** with compliance mapping  

Perfect for teams that want AI-assisted pentesting combined with human expertise.

---

**Next Steps:**
1. Set up ANTHROPIC_API_KEY
2. Run: `vapt ai interactive --client "Test" --target "https://your-app.com"`
3. Follow Claude's guidance through the assessment
4. Review generated findings and recommendations
5. Perform manual verification and exploitation
6. Generate final report with Claude's help
