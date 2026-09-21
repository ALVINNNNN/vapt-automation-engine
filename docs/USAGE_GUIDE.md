# VAPT Automation Engine - Usage Guide

## Table of Contents
1. [Basic Workflow](#basic-workflow)
2. [Network Assessment (nVAPT)](#network-assessment-nvapт)
3. [Application Assessment (AVAPT)](#application-assessment-avapt)
4. [Report Generation](#report-generation)
5. [Advanced Usage](#advanced-usage)
6. [Best Practices](#best-practices)

## Basic Workflow

```
┌─────────────┐
│  Planning   │  Define scope, objectives, frameworks
└──────┬──────┘
       │
┌──────▼───────────┐
│ Reconnaissance   │  OSINT, asset discovery
└──────┬───────────┘
       │
┌──────▼──────────┐
│ Network Scan    │  nVAPT - Nmap, SSL/TLS
└──────┬──────────┘
       │
┌──────▼──────────────┐
│ Application Scan    │  AVAPT - Burp Suite
└──────┬──────────────┘
       │
┌──────▼────────────┐
│ Exploitation      │  Metasploit, manual testing
└──────┬────────────┘
       │
┌──────▼──────────────┐
│ Analysis & Review   │  Risk assessment, mapping
└──────┬──────────────┘
       │
┌──────▼────────────┐
│ Report Generation │  Executive, Technical, HTML
└─────────────────┘
```

## Network Assessment (nVAPT)

### Step 1: Prepare Target List

Create a file with network targets:

```bash
cat > targets.txt << 'EOF'
192.168.1.0/24
10.0.0.1-50
example.com
mail.example.com
EOF
```

### Step 2: Initialize Assessment

```bash
vapt init \
    --client "Acme Corporation" \
    --type nvapт \
    --output-dir ./assessments/acme-nov-2024
```

Output:
```
✓ Assessment initialized: a1b2c3d4-e5f6-7890
  Client: Acme Corporation
  Type: nvapт
  Working Directory: ./assessments/acme-nov-2024
```

### Step 3: Execute Network Scan

```bash
vapt network-scan \
    --targets targets.txt \
    --profile aggressive \
    --output-dir ./assessments/acme-nov-2024
```

#### Scan Profiles

| Profile | Speed | Coverage | Best For |
|---------|-------|----------|----------|
| quick | Fast | 60% | Preliminary assessment |
| normal | Medium | 80% | Standard assessment |
| aggressive | Slow | 95%+ | Thorough testing |

### Step 4: Review Results

```bash
vapt summarize \
    --assessment-id a1b2c3d4-e5f6-7890 \
    --output-dir ./assessments/acme-nov-2024
```

Output:
```
============================================================
ASSESSMENT SUMMARY
============================================================
Assessment ID: a1b2c3d4-e5f6-7890
Client: Acme Corporation
Type: nvapт
Status: completed
Total Findings: 42

Findings by Severity:
  Critical: 3
  High: 8
  Medium: 15
  Low: 16

Scanners Used: nmap, sslyze
Exploitations Attempted: 5
============================================================
```

## Application Assessment (AVAPT)

### Step 1: Setup Burp Suite

Ensure Burp Suite Professional is running with REST API enabled:

```bash
# Create Burp configuration
cat > config/burp_config.json << 'EOF'
{
    "api_url": "http://localhost:1337",
    "api_key": "YOUR_API_KEY",
    "timeout": 3600,
    "session_timeout": 300
}
EOF
```

### Step 2: Initialize Assessment

```bash
vapt init \
    --client "Acme Corporation" \
    --type avapt \
    --output-dir ./assessments/acme-app-scan
```

### Step 3: Execute Application Scan

```bash
vapt app-scan \
    --url "https://app.example.com" \
    --burp-config config/burp_config.json \
    --output-dir ./assessments/acme-app-scan
```

### Step 4: Manual Testing

For complex applications, conduct manual testing:

```bash
# Within Burp Suite
1. Configure browser proxy (127.0.0.1:8080)
2. Browse application to build site map
3. Run Scanner (Burp Scanner)
4. Perform manual testing on interesting features
5. Review findings
```

## Report Generation

### Generate All Reports

```bash
vapt report \
    --assessment-id a1b2c3d4-e5f6-7890 \
    --format executive technical html pdf json \
    --output-dir ./reports/
```

### Report Types

#### 1. Executive Summary
- C-level audience
- Risk overview
- Business impact
- Remediation priority

```bash
vapt report \
    --assessment-id a1b2c3d4-e5f6-7890 \
    --format executive \
    --output-dir ./reports/
```

#### 2. Technical Report
- Detailed findings
- CVSS scores
- Proof of concept
- Remediation steps

```bash
vapt report \
    --assessment-id a1b2c3d4-e5f6-7890 \
    --format technical \
    --output-dir ./reports/
```

#### 3. HTML Report
- Interactive web view
- Evidence gallery
- Timeline
- Compliance mapping

```bash
vapt report \
    --assessment-id a1b2c3d4-e5f6-7890 \
    --format html \
    --output-dir ./reports/
```

#### 4. PDF Report
- Print-ready format
- Audit trail
- Compliance documentation
- Legal evidence

```bash
vapt report \
    --assessment-id a1b2c3d4-e5f6-7890 \
    --format pdf \
    --output-dir ./reports/
```

#### 5. JSON Export
- Machine-readable format
- API integration
- Automation friendly

```bash
vapt report \
    --assessment-id a1b2c3d4-e5f6-7890 \
    --format json \
    --output-dir ./reports/
```

## Advanced Usage

### Custom Scanning Configuration

Create advanced configuration:

```yaml
# config/advanced_scan.yaml
assessment:
  client: Acme Corporation
  scope: "All internal systems"
  frameworks: [owasp, nist, pci_dss, iso_27001]

network_scan:
  profiles:
    aggressive:
      timing: T4
      scripts:
        - vuln
        - default
        - discovery
        - ssl-enum-ciphers
        - ssl-date
      nse_script_args: "unsafe=1"

web_scan:
  burp:
    crawl_strategy: deep
    scan_speed: fast
    extensions:
      - active-extensions
      - passive-extensions
  
  manual_testing:
    - authentication_bypass
    - business_logic_flaws
    - api_testing

reporting:
  formats: [executive, technical, html, pdf]
  include_evidence: true
  include_remediation: true
  compliance_mapping: true
```

### Scheduled Assessments

Run periodic assessments:

```bash
#!/bin/bash
# weekly-assessment.sh

TIMESTAMP=$(date +"%Y-%m-%d")
CLIENT="Acme Corp"
ASSESSMENT_DIR="assessments/${CLIENT}-${TIMESTAMP}"

mkdir -p ${ASSESSMENT_DIR}

# Initialize
vapt init \
    --client "${CLIENT}" \
    --type hybrid \
    --output-dir ${ASSESSMENT_DIR}

# Run scans
vapt network-scan \
    --targets targets.txt \
    --profile normal \
    --output-dir ${ASSESSMENT_DIR}

vapt app-scan \
    --url "https://app.example.com" \
    --output-dir ${ASSESSMENT_DIR}

# Generate reports
vapt report \
    --assessment-id ${ASSESSMENT_DIR} \
    --format all \
    --output-dir ${ASSESSMENT_DIR}/reports

# Archive
tar -czf ${ASSESSMENT_DIR}.tar.gz ${ASSESSMENT_DIR}
```

### Integration with CI/CD

```yaml
# .github/workflows/security-scan.yml
name: Security Assessment

on: [push, pull_request]

jobs:
  vapt-scan:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup VAPT
        run: |
          pip install -r requirements.txt
          pip install -e .
      
      - name: Network Scan
        run: |
          vapt network-scan \
              --targets targets.txt \
              --profile normal \
              --output-dir ./scan-results
      
      - name: Generate Report
        run: |
          vapt report \
              --assessment-id $(date +%s) \
              --format json \
              --output-dir ./scan-results
      
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: security-scan
          path: scan-results/
```

## Best Practices

### 1. Scope Definition

Always clearly define:
- In-scope systems
- Testing timeframe
- Authorized personnel
- Prohibited actions
- Escalation procedures

### 2. Pre-Assessment

- Obtain written authorization
- Identify critical systems
- Plan testing windows
- Prepare remediation plan
- Establish communication channels

### 3. During Assessment

- Document all activities
- Take screenshots/evidence
- Maintain audit log
- Report critical findings immediately
- Coordinate with client stakeholders

### 4. Post-Assessment

- Compile findings
- Verify accuracy of results
- Generate compliance reports
- Present to client
- Plan remediation tracking

### 5. Tool Configuration

```bash
# Always use configuration files
vapt init \
    --client "Acme Corp" \
    --config config/assessment.yaml

# Verify tool versions before assessment
nmap --version
msfconsole --version
burp --version
```

### 6. Evidence Collection

```bash
# Capture comprehensive evidence
1. Screenshots of findings
2. Network traffic captures
3. Log excerpts
4. Command output
5. System responses
6. Timeline of activities
```

### 7. Compliance Verification

```bash
# Always validate compliance mappings
vapt compliance-check \
    --frameworks owasp,nist,pci_dss,iso_27001 \
    --assessment-id a1b2c3d4-e5f6-7890
```

## Troubleshooting

### Common Issues

**Issue: Nmap timeout**
```bash
# Increase timeout
vapt network-scan \
    --targets targets.txt \
    --profile normal \
    --timeout 7200
```

**Issue: Burp API connection failed**
```bash
# Check Burp is running
curl -X GET http://localhost:1337/v2/project/status

# Enable REST API in Burp UI
# User Options → Misc → REST API → Enable
```

**Issue: Permission denied (Linux)**
```bash
# Run with appropriate privileges
sudo vapt network-scan --targets targets.txt

# Or add user to sudoers
sudo visudo
# Add: username ALL=(ALL) NOPASSWD: /usr/bin/nmap
```

## Performance Optimization

```bash
# Parallel scanning (if hardware supports)
vapt network-scan \
    --targets targets.txt \
    --parallel 4 \
    --profile quick

# Reduce scan depth for large networks
vapt network-scan \
    --targets 192.168.1.0/24 \
    --skip-os-detection \
    --skip-version-detection
```

## Next Steps

- Review [FRAMEWORKS.md](FRAMEWORKS.md) for compliance details
- Check examples in [examples/](../examples/)
- Contact support for tool integration questions
