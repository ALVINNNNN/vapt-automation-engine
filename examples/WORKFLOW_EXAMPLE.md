# VAPT Automation Engine - Example Workflow

This document walks through a complete penetration testing assessment using VAPT.

## Scenario

**Client**: Acme Corporation  
**Date**: September 2026  
**Scope**: Internal network + web application  
**Frameworks**: OWASP, NIST, PCI-DSS, ISO 27001  
**Timeframe**: 5 business days

## Phase 1: Planning & Preparation

### 1.1 Create Assessment Directory

```bash
mkdir -p ~/vapt-assessments/acme-corp-sep2026
cd ~/vapt-assessments/acme-corp-sep2026
```

### 1.2 Prepare Target Lists

**Network targets** (`targets-network.txt`):
```
192.168.1.0/24
192.168.100.0/25
10.0.0.1-10
```

**Web targets** (`targets-web.txt`):
```
https://app.acme.com
https://api.acme.com
https://mail.acme.com
```

### 1.3 Review Authorization

```
✓ Signed penetration testing agreement
✓ Executive approval obtained
✓ Legal review completed
✓ Emergency contact list prepared
✓ ROE (Rules of Engagement) documented
```

## Phase 2: Assessment Initialization

### 2.1 Initialize Assessment

```bash
vapt init \
    --client "Acme Corporation" \
    --type hybrid \
    --output-dir ./assessment \
    --frameworks "owasp,nist,pci_dss,iso_27001"
```

**Output:**
```
✓ Assessment initialized: a5f8c2d1-e9b6-4c7a-9d1f-6e8h0j2k4l6m
  Client: Acme Corporation
  Type: hybrid
  Working Directory: ./assessment
  Frameworks: owasp, nist, pci_dss, iso_27001
```

### 2.2 Document Scope

Create `assessment/SCOPE.md`:

```markdown
# Assessment Scope - Acme Corporation

## In-Scope Systems

### Network
- 192.168.1.0/24 (Internal LAN)
- 192.168.100.0/25 (Management VLAN)
- 10.0.0.1-10 (DMZ servers)

### Web Applications
- https://app.acme.com (Main application)
- https://api.acme.com (REST API)
- https://mail.acme.com (Email system)

### Infrastructure
- Windows 2019 Servers
- Linux Ubuntu 20.04
- Cisco ASA Firewall
- Palo Alto Networks PAN-OS

## Out-of-Scope

- Production databases (read-only testing only)
- Third-party hosted services
- End-user workstations
- Development environment (separate assessment)

## Testing Windows

- Monday-Friday: 10 AM - 4 PM (EST)
- Avoid: 8-10 AM, 4-6 PM, 12-1 PM lunch
- No testing during: Payroll processing (Tuesdays 6-8 PM)

## Rules of Engagement

- No DoS/DDoS attacks
- No data exfiltration (only screenshots/evidence)
- No credential storage
- No permanent changes to systems
- Immediate notification of critical findings
```

## Phase 3: Reconnaissance

### 3.1 OSINT

```bash
# Document public information
cat > assessment/osint_findings.md << 'EOF'
## OSINT Findings

### Domain Information
- Domain: acme.com
- Registrar: Name.com
- Creation Date: 2015-03-15
- Nameservers: ns1.acme.com, ns2.acme.com
- MX Records: mail.acme.com

### DNS Enumeration
- app.acme.com - 203.0.113.50
- api.acme.com - 203.0.113.51
- mail.acme.com - 203.0.113.52

### Subdomains
- vpn.acme.com
- internal.acme.com (blocked)
- staging.acme.com
- dev.acme.com

### Technologies Identified
- Web Server: Apache 2.4.41
- PHP: 7.4.3
- Database: MySQL 8.0
- CMS: WordPress 5.9
EOF
```

### 3.2 Asset Discovery

```bash
# Quick network sweep
nmap -sn 192.168.1.0/24 > assessment/network-sweep.txt

# Service enumeration
nmap -sV -sC 192.168.1.0/24 -oX assessment/nmap-services.xml
```

## Phase 4: Network Assessment (nVAPT)

### 4.1 Execute Network Scan

```bash
vapt network-scan \
    --targets targets-network.txt \
    --profile aggressive \
    --output-dir ./assessment
```

**Scan Progress:**
```
[████████░░░░░░░░░░░░░░░░░░░░░░░░] 35% - Scanning 192.168.1.0/24
Hosts up: 15
Services found: 47
Potential vulnerabilities: 12

[██████████████████░░░░░░░░░░░░░░] 65% - Scanning 192.168.100.0/25
Hosts up: 8
Services found: 18
Potential vulnerabilities: 5

[██████████████████████████████████] 100% - Complete
```

### 4.2 Key Findings from Network Scan

```
CRITICAL (1):
  - SSL/TLS: Heartbleed vulnerable (CVE-2014-0160) on 192.168.1.15:443

HIGH (3):
  - Service: Telnet exposed (192.168.1.5:23)
  - Weak SSH: RSA 1024-bit key (192.168.100.10:22)
  - SNMP: Default community string (192.168.1.20:161)

MEDIUM (7):
  - Services with default credentials
  - Weak encryption protocols
  - Information disclosure

LOW (5):
  - Outdated service versions
  - Unnecessary services running
```

## Phase 5: Application Assessment (AVAPT)

### 5.1 Setup Burp Suite

```bash
# Start Burp Suite with API
java -Xmx4g -jar burpsuite_pro_2026.jar \
    --project-file=acme.burp \
    --config-file=headless.config
```

### 5.2 Configure VAPT for Burp

Create `config/burp_config.json`:
```json
{
    "api_url": "http://localhost:1337",
    "api_key": "YOUR_API_KEY",
    "timeout": 3600,
    "scan_scope": {
        "include": [
            "^https://app\\.acme\\.com/.*",
            "^https://api\\.acme\\.com/.*"
        ]
    }
}
```

### 5.3 Execute Web Scan

```bash
vapt app-scan \
    --url "https://app.acme.com" \
    --burp-config config/burp_config.json \
    --output-dir ./assessment
```

### 5.4 Manual Testing

```bash
# 1. Authentication Testing
   ✓ SQL injection in login form
   ✓ Weak password policy
   ✓ Account lockout bypass

# 2. Session Management
   ✓ Session fixation possible
   ✓ Insecure cookie attributes (no HttpOnly)

# 3. API Testing
   ✓ IDOR in /api/users/{id}
   ✓ Missing rate limiting
   ✓ No CSRF token on state-changing operations

# 4. Input Validation
   ✓ Stored XSS in comment field
   ✓ Command injection in file upload
   ✓ Path traversal in download endpoint
```

## Phase 6: Exploitation & Verification

### 6.1 Proof of Concept

```bash
# SQL Injection PoC
curl -X POST "https://app.acme.com/login" \
  -d "username=admin' OR '1'='1&password=anything"

# Response: 200 OK - Logged in as admin
```

### 6.2 Post-Exploitation

```bash
# After gaining access to app.acme.com
# 1. Retrieve database credentials from config
# 2. Access sensitive data (customer records)
# 3. Enumerate internal systems
# 4. Lateral movement to admin panel
# 5. Document evidence (screenshots)

# DO NOT:
# - Exfiltrate actual customer data
# - Make permanent changes
# - Use credentials after assessment
# - Delete or modify evidence
```

## Phase 7: Analysis & Mapping

### 7.1 Aggregate Findings

```bash
# All findings from network and app scans
assessment/findings.json contains:
  - 24 total findings
  - 1 Critical
  - 4 High
  - 9 Medium
  - 10 Low
```

### 7.2 Compliance Mapping

Automatically mapped to:
- **OWASP**: A07:2021 (Auth), A03:2021 (Injection), A05:2021 (XXE)
- **NIST**: CSF Categories: Detect, Protect, Recover
- **PCI-DSS**: Req 2, 4, 6, 7, 8, 11
- **ISO 27001**: A.8 (Technical), A.9 (User access), A.12 (Operations)

## Phase 8: Report Generation

### 8.1 Generate All Reports

```bash
vapt report \
    --assessment-id a5f8c2d1-e9b6-4c7a-9d1f-6e8h0j2k4l6m \
    --format executive technical html pdf json \
    --output-dir ./assessment/reports
```

### 8.2 Executive Summary (Sample)

```
PENETRATION TESTING ASSESSMENT - EXECUTIVE SUMMARY
===================================================

Client:           Acme Corporation
Assessment Date:  September 2026
Testing Duration: 5 business days
Scope:           Internal Network + Web Applications

FINDINGS OVERVIEW
-----------------
Total Vulnerabilities: 24

By Severity:
  Critical:  1  (4%)
  High:      4  (17%)
  Medium:    9  (38%)
  Low:      10  (41%)

BUSINESS IMPACT
---------------
• Critical issue allows complete system compromise
• High-risk findings enable unauthorized data access
• Medium-risk issues provide lateral movement paths

IMMEDIATE ACTIONS REQUIRED
--------------------------
1. Patch Heartbleed vulnerability (CVE-2014-0160)
2. Disable Telnet protocol
3. Remediate SQL injection in login form
4. Implement multi-factor authentication

RECOMMENDED TIMELINE
--------------------
• Critical:  Remediate within 24 hours
• High:      Remediate within 7 days
• Medium:    Remediate within 30 days
• Low:       Remediate within 90 days
```

### 8.3 Technical Report Excerpt

```
TECHNICAL FINDINGS REPORT
==========================

[1/24] SQL Injection in Login Form
--------
Severity:    High
CVSS Score:  8.9
CWE:         CWE-89 (SQL Injection)
OWASP:       A03:2021 - Injection
PCI-DSS:     Req 6.5.1
ISO 27001:   A.12.6.1

Description:
The login form on https://app.acme.com/login.php is vulnerable to SQL
injection. User-supplied input is not properly sanitized before being
used in SQL queries.

Proof of Concept:
  Input:  admin' OR '1'='1 --
  Result: Successful login as admin user

Business Impact:
• Complete authentication bypass
• Unauthorized access to sensitive data
• Potential privilege escalation
• Compliance violation (PCI-DSS, ISO 27001)

Remediation:
1. Use parameterized queries / prepared statements
2. Implement input validation and sanitization
3. Use ORM frameworks (e.g., Doctrine, Eloquent)
4. Enable query logging and monitoring
5. Conduct code review of all database interactions

References:
  - OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
  - CWE-89: https://cwe.mitre.org/data/definitions/89.html
  - NIST SP 800-53 SI-10: Information System Monitoring
```

## Phase 9: Client Presentation

### 9.1 Presentation Outline

```
1. Executive Summary (C-level) - 10 minutes
   - Risk overview
   - Critical findings
   - Business impact
   - Roadmap

2. Technical Deep Dive (IT/Security) - 30 minutes
   - Detailed findings
   - Proof of concepts
   - Remediation steps
   - Questions & Answers

3. Remediation Planning - 20 minutes
   - Timeline negotiation
   - Resource allocation
   - Testing procedures
   - Follow-up assessment
```

### 9.2 Deliverables Package

```
assessment/deliverables/
├── Acme-Corp-Executive-Summary.pdf
├── Acme-Corp-Technical-Report.pdf
├── Acme-Corp-Evidence-Screenshots/
│   ├── sql-injection-poc.png
│   ├── heartbleed-verification.png
│   └── ...
├── Acme-Corp-Compliance-Mapping.xlsx
├── Acme-Corp-Remediation-Guide.pdf
├── Acme-Corp-Assessment-Data.json
└── README.txt
```

## Phase 10: Follow-up

### 10.1 Remediation Tracking

```bash
# Re-scan after 30 days
vapt network-scan \
    --targets targets-network.txt \
    --output-dir ./assessment-followup-30day

# Compare results
vapt compare-assessments \
    --baseline assessment/assessment_state.json \
    --followup assessment-followup-30day/assessment_state.json
```

### 10.2 Documentation

Archive assessment data:
```bash
tar -czf acme-corp-sep2026-assessment.tar.gz assessment/
gpg --encrypt --recipient "client@acme.com" acme-corp-sep2026-assessment.tar.gz

# Maintain records for:
# - Compliance audit trail
# - Future assessments
# - Legal documentation
```

## Lessons Learned

```markdown
# Acme Corp Assessment - Post-Assessment Review

## What Went Well
✓ Clear scope definition
✓ Cooperative client contact
✓ Well-documented infrastructure
✓ Comprehensive tool integration

## Challenges
✗ Burp API occasionally slow during peak traffic
✗ Some systems had monitoring that triggered alerts
✗ Legacy systems lacked modern logging

## Improvements for Next Assessment
- Coordinate testing windows better
- Test on staging environment first
- Provide more training to client's security team
- Implement continuous security monitoring
```

---

**Assessment ID:** a5f8c2d1-e9b6-4c7a-9d1f-6e8h0j2k4l6m  
**Completed:** September 2026  
**Tester:** [Your Name]  
**Reviewed:** [Security Lead]
