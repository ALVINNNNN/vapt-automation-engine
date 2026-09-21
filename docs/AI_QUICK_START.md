# AI Penetration Testing - Quick Start

Get started with Claude-powered intelligent penetration testing in 5 minutes.

## Setup (1 minute)

### 1. Get Claude API Key

Visit https://console.anthropic.com/account/keys and create an API key.

### 2. Set Environment Variable

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### 3. Verify Installation

```bash
pip install anthropic
python -c "import anthropic; print('✓ Ready')"
```

## Run Your First Assessment (4 minutes)

### Option A: Interactive Mode (Recommended)

Have a conversation with Claude about your target:

```bash
vapt ai interactive \
    --client "Acme Corp" \
    --target "https://app.example.com"
```

**You'll get:**
- Reconnaissance strategy
- Endpoint testing approach
- JavaScript analysis guidance
- Vulnerability hypotheses
- Exploitation techniques

### Option B: Automated Mode

Run full assessment automatically:

```bash
vapt ai automated \
    --client "Acme Corp" \
    --target "https://app.example.com"
```

**Runs automatically:**
1. Reconnaissance (gathering information)
2. Analysis (generating hypotheses)
3. Testing (executing tests)
4. Exploitation (exploiting vulnerabilities)
5. Reporting (generating report)

## What Happens Next

### Results Location

```
assessments/ai-pentest-YYYYMMDD-HHMMSS/
├── assessment_state.json
├── assessment_report.json (findings)
└── interactive_assessment.json (conversation history)
```

### View Results

```bash
# See assessment summary
vapt ai analyze-results --assessment-id ai-pentest-YYYYMMDD-HHMMSS

# Review findings
cat assessments/ai-pentest-YYYYMMDD-HHMMSS/assessment_report.json
```

## Common Tasks

### Get Reconnaissance Guidance

Ask Claude what to test:

```bash
vapt ai reconnaissance --target "https://app.example.com"
```

### Get Exploitation Strategy

Upload findings and get exploitation plan:

```bash
vapt ai exploit-strategy \
    --target "https://app.example.com" \
    --findings ./my-findings.json
```

### Generate Professional Report

```bash
vapt ai generate-report \
    --findings-file ./findings.json \
    --output ./report.json
```

## Example Workflow

```bash
# 1. Start interactive assessment
vapt ai interactive --client "Acme" --target "https://app.acme.com"

# Claude guides you through:
# - What to look for
# - How to test endpoints
# - How to analyze JavaScript
# - What vulnerabilities are likely
# - How to exploit them

# 2. During assessment, Claude asks clarifying questions:
# "What was the response from the API? Did it leak user data?"

# 3. Based on your findings, Claude suggests next steps:
# "That IDOR vulnerability can lead to privilege escalation. Try accessing admin endpoints..."

# 4. After gathering all findings, Claude helps generate report:
# "Based on what we found, here's the comprehensive report..."

# 5. Results saved automatically to:
assessments/ai-pentest-20260921-143022/
```

## What Claude Can Do

### Discovery & Reconnaissance
✓ Identify technology stack  
✓ Find JavaScript files and analyze them  
✓ Enumerate API endpoints  
✓ Detect security patterns  
✓ Identify attack surfaces  

### Analysis & Reasoning
✓ Generate vulnerability hypotheses  
✓ Threat modeling  
✓ Risk prioritization  
✓ Attack path identification  
✓ Vulnerability chaining  

### Testing Guidance
✓ Design test cases  
✓ Provide exploitation steps  
✓ Suggest payloads  
✓ Explain how to verify  
✓ Show business impact  

### Reporting
✓ Compile findings  
✓ Prioritize by severity  
✓ Create remediation guidance  
✓ Map to compliance frameworks  
✓ Generate executive summary  

## Tips & Tricks

### 1. Be Specific

❌ Bad: "Find vulnerabilities"  
✓ Good: "I found a parameter 'user_id' that accepts any integer. Can I access other users' data?"

### 2. Provide Context

❌ Bad: "Is this vulnerable?"  
✓ Good: "The API endpoint /api/users/{id} returns all user data. When I change the ID, I can see other users' information."

### 3. Ask Follow-ups

❌ Bad: "What's next?"  
✓ Good: "Now that I have the IDOR, can I escalate to admin access?"

### 4. Request Specific Formats

```bash
# Get JSON output for integration
vapt ai exploit-strategy \
    --target "https://app.example.com" \
    --findings findings.json \
    --format json
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### "Connection timeout"
- Check internet connection
- Verify API key is valid
- Try again (API may be busy)

### "Invalid JSON in response"
- Claude tried but failed to format JSON
- Ask it to reformatted: "Format this as valid JSON"
- Manually extract the data

### "Assessment taking too long"
- Reconnaissance can take several minutes
- This is normal - Claude is performing deep analysis
- Large targets take longer than small ones

## Next Steps

1. ✓ Set up API key
2. ✓ Run first interactive assessment
3. ✓ Review results in `assessments/` directory
4. ✓ Read [AI_ASSESSMENT_GUIDE.md](AI_ASSESSMENT_GUIDE.md) for advanced usage
5. ✓ Integrate into your workflow

## Advanced Usage

### Python Integration

```python
from vapt.ai_engine import AIAssessmentCoordinator

coordinator = AIAssessmentCoordinator(
    client_name="Acme Corp",
    target_url="https://app.acme.com"
)

# Run assessment
result = coordinator.run_interactive_assessment()

# Access results
summary = coordinator.get_summary()
print(f"Assessment ID: {summary['assessment_id']}")
print(f"Results saved to: {summary['results_directory']}")
```

### Custom Assessment Script

```python
from vapt.ai_engine import quick_ai_assessment

# Quick interactive assessment
result = quick_ai_assessment(
    client_name="Acme Corp",
    target_url="https://app.acme.com"
)
```

## Security Note

⚠️ **IMPORTANT**: Only test systems you own or have written authorization to test.

Keep in mind:
- Save all authorization documents
- Document all activities
- Get written client agreement
- Understand your liability
- Follow all applicable laws

## Support & Documentation

- **Full Guide**: [AI_ASSESSMENT_GUIDE.md](AI_ASSESSMENT_GUIDE.md)
- **Main Docs**: [README.md](../README.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Usage**: [USAGE_GUIDE.md](USAGE_GUIDE.md)

---

**Ready to start?** Run your first assessment:

```bash
vapt ai interactive --client "Test" --target "https://your-app.com"
```

Claude will guide you through the entire process! 🚀
