# Compliance Frameworks

This document outlines how VAPT Automation Engine maps vulnerabilities to various compliance frameworks for regulated environments.

## Supported Frameworks

### 1. OWASP Top 10 (2021)

The OWASP Top 10 is a ranking of the most critical web application security risks.

#### Mappings

| OWASP Category | VAPT Findings |
|---|---|
| A01:2021 - Broken Access Control | Missing access controls, privilege escalation, lateral movement |
| A02:2021 - Cryptographic Failures | Weak encryption, outdated algorithms, insecure protocols |
| A03:2021 - Injection | SQL injection, Command injection, NoSQL injection |
| A04:2021 - Insecure Design | Business logic flaws, workflow bypass |
| A05:2021 - Security Misconfiguration | Default credentials, exposed services, debug modes |
| A06:2021 - Vulnerable Components | Outdated libraries, unpatched software |
| A07:2021 - Identification Issues | Weak authentication, MFA bypass, session fixation |
| A08:2021 - Data Integrity Failures | Insecure deserialization, XXE |
| A09:2021 - Logging Failures | Insufficient logging, log tampering |
| A10:2021 - SSRF | Server-side request forgery, internal network access |

### 2. NIST Cybersecurity Framework

NIST CSF provides guidelines for managing cybersecurity risks and is required by many government agencies.

#### Risk Levels

| Level | Timeline | Description |
|---|---|---|
| Critical | Immediate | Must be remediated within 24 hours |
| High | 7 days | Must be remediated within 7 days |
| Medium | 30 days | Must be remediated within 30 days |
| Low | 90 days | Must be remediated within 90 days |

#### Core Functions

- **Identify**: Understanding organizational assets and vulnerabilities
- **Protect**: Implementing safeguards to prevent attacks
- **Detect**: Identifying security incidents in real-time
- **Respond**: Taking action when incidents are detected
- **Recover**: Restoring systems after incidents

### 3. PCI-DSS (Payment Card Industry Data Security Standard)

PCI-DSS is mandatory for organizations that handle payment card data.

#### Key Requirements

| Requirement | Focus |
|---|---|
| PCI-DSS 2.x | Default security parameters |
| PCI-DSS 3.x | Protection of stored data |
| PCI-DSS 4.x | Protection of data in transit |
| PCI-DSS 6.x | Secure development & vulnerability management |
| PCI-DSS 7.x | Restrict access to cardholder data |
| PCI-DSS 8.x | User identification and authentication |
| PCI-DSS 10.x | Logging and monitoring |
| PCI-DSS 11.x | Security testing and scanning |
| PCI-DSS 12.x | Information security policy |

### 4. ISO 27001 (Information Security Management)

ISO 27001 defines requirements for establishing and maintaining an information security management system (ISMS).

#### Control Categories (Annex A)

| Category | Controls |
|---|---|
| A.5 | Organizational controls |
| A.6 | People controls |
| A.7 | Physical controls |
| A.8 | Technological controls |

#### Key Technical Controls

- A.8.1: Cryptographic controls
- A.8.2: Endpoint controls
- A.8.3: Encryption controls
- A.8.4: Logging controls
- A.9: User access controls
- A.12: Technical operations controls

## Mapping Process

### Automatic Mapping

Each vulnerability finding is automatically mapped to applicable frameworks:

```python
finding = {
    "title": "SQL Injection Vulnerability",
    "severity": "High",
    "frameworks": {
        "owasp": ["A03:2021 - Injection"],
        "nist": ["High - Remediate within 30 days"],
        "pci_dss": ["PCI-DSS 6.5.1 - Injection flaws"],
        "iso_27001": ["A.12.6.1 - Technical vulnerability management"]
    }
}
```

### Manual Review

Security analysts can:
1. Verify automated mappings
2. Add additional framework references
3. Document framework-specific remediation steps

## Compliance Reporting

VAPT generates compliance reports including:

- **Framework Coverage**: Which requirements are affected
- **Findings Correlation**: How findings map to requirements
- **Remediation Tracking**: Progress toward compliance
- **Executive Summary**: Risk assessment by framework
- **Detailed Evidence**: Supporting documentation for auditors

## Example Reports

### OWASP Report Structure
```
OWASP Top 10 Coverage:
├── A01:2021 - Broken Access Control (3 findings)
├── A03:2021 - Injection (5 findings)
├── A07:2021 - Identification (2 findings)
└── ...
```

### NIST Report Structure
```
NIST CSF Status:
├── Identify: 85% Coverage
├── Protect: 72% Coverage
├── Detect: 60% Coverage
├── Respond: 50% Coverage
└── Recover: 40% Coverage
```

### PCI-DSS Report Structure
```
PCI-DSS Compliance:
├── Requirement 2: Findings (1) - Not In Scope
├── Requirement 4: Findings (3) - In Scope
├── Requirement 6: Findings (7) - In Scope
└── Requirement 7: Findings (2) - In Scope
```

## Framework Selection

When initiating an assessment, select applicable frameworks:

```bash
# Select specific frameworks
vapt init \
    --client "Acme Corp" \
    --frameworks "owasp,nist,pci_dss" \
    --pci-scope "payment-processing,customer-data"
```

## Remediation Guidance

Each framework provides specific remediation guidance:

```markdown
# Finding: Weak Encryption

## OWASP Remediation
- Implement AES-256 encryption for data at rest
- Use TLS 1.2+ for data in transit

## NIST Remediation
- Align with NIST SP 800-53 SC-7 (Cryptographic Protection)
- Document encryption key management

## PCI-DSS Remediation
- Follow PCI-DSS 3.2.1 Strong Cryptography requirements
- Use FIPS-approved algorithms
- Maintain encryption key inventory (Req 3.5)

## ISO 27001 Remediation
- Implement A.10.1.1 Cryptographic controls
- Document in ISMS documentation
- Include in annual internal audit
```

## Compliance Dashboard

VAPT provides a compliance dashboard showing:

- Compliance status by framework
- Trend analysis over time
- Risk heat map
- Required actions
- Audit trail

## Additional Resources

- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- NIST CSF: https://www.nist.gov/cyberframework
- PCI-DSS: https://www.pcisecuritystandards.org/
- ISO 27001: https://www.iso.org/isoiec-27001-information-security-management.html
