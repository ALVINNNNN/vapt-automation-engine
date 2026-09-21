# VAPT Automation Engine

A comprehensive penetration testing automation platform for conducting Network and Application Vulnerability Assessment Penetration Testing (nVAPT & AVAPT) in highly regulated environments.

## Overview

This engine automates the full end-to-end workflow for professional penetration testing assessments, supporting multiple compliance frameworks and generating detailed, client-ready reports.

### Key Features

- **Dual Assessment Capability**
  - nVAPT: Network Vulnerability Assessment & Penetration Testing
  - AVAPT: Application Vulnerability Assessment & Penetration Testing

- **Compliance Framework Support**
  - OWASP Top 10 & Testing Guide
  - NIST Cybersecurity Framework
  - PCI-DSS Requirements
  - ISO 27001/27002

- **Integrated Security Tools**
  - Burp Suite Professional (API-driven)
  - Metasploit Framework (RPC)
  - Nmap & Advanced Scanning
  - sslyze (SSL/TLS Analysis)
  - Custom Exploitation Modules

- **Multi-Format Reporting**
  - Executive Summary (C-Suite Ready)
  - Technical Detailed Report (Remediation Focused)
  - HTML Interactive Report (Web-based)
  - PDF Compliance Report (Audit Trail)
  - Risk Assessment Matrix
  - Evidence Repository

- **Cross-Platform Support**
  - Kali Linux (Native)
  - Windows (WSL/Native Integration)
  - Docker Containerized Deployment

## Quick Start

### Prerequisites

- Python 3.8+
- Burp Suite Professional (license key)
- Metasploit Framework
- Nmap
- Git

### Installation

```bash
git clone https://github.com/alvinnnnn/vapt-automation-engine.git
cd vapt-automation-engine
pip install -r requirements.txt
python setup.py install
```

### Basic Usage

```bash
# Initialize a new assessment
vapt init --client "Acme Corp" --scope-file scope.txt

# Run network assessment
vapt network-assess --target-file targets.txt --profile aggressive

# Run application assessment
vapt app-assess --target-url https://app.acme.com --burp-profile corporate

# Generate reports
vapt report --format all --output ./reports/
```

## Project Structure

```
vapt-automation-engine/
├── docs/                          # Comprehensive documentation
│   ├── INSTALLATION.md           # Setup instructions
│   ├── FRAMEWORKS.md             # Compliance framework mappings
│   ├── ARCHITECTURE.md           # System design
│   └── USAGE_GUIDE.md            # Detailed user guide
├── vapt/                         # Main package
│   ├── __init__.py
│   ├── core/                     # Core functionality
│   │   ├── assessment.py         # Assessment orchestration
│   │   ├── scanner.py            # Scanner abstraction
│   │   └── reporter.py           # Report generation
│   ├── scanners/                 # Tool integrations
│   │   ├── burp.py               # Burp Suite integration
│   │   ├── metasploit.py         # Metasploit integration
│   │   ├── nmap_scanner.py       # Nmap integration
│   │   └── sslyze_scanner.py     # SSL/TLS analysis
│   ├── assessments/              # Assessment types
│   │   ├── nvapт/                # Network assessment
│   │   └── avapt/                # Application assessment
│   ├── exploits/                 # Exploitation modules
│   ├── reporters/                # Report generators
│   │   ├── executive.py          # Executive summary
│   │   ├── technical.py          # Technical report
│   │   ├── html_reporter.py      # HTML report
│   │   └── pdf_reporter.py       # PDF report
│   ├── compliance/               # Compliance frameworks
│   │   ├── owasp.py              # OWASP mappings
│   │   ├── nist.py               # NIST mappings
│   │   ├── pci_dss.py            # PCI-DSS mappings
│   │   └── iso27001.py           # ISO 27001 mappings
│   ├── config/                   # Configuration management
│   ├── utils/                    # Utility functions
│   └── cli.py                    # CLI interface
├── tests/                        # Unit & integration tests
├── templates/                    # Report templates
├── examples/                     # Example assessments
├── config/                       # Configuration files
│   ├── frameworks.yaml           # Compliance framework config
│   └── tools.yaml                # Tool configuration
├── requirements.txt              # Python dependencies
├── setup.py                      # Installation script
└── .github/                      # GitHub specific files
    └── workflows/               # CI/CD pipelines
```

## Compliance Mapping

Each vulnerability finding is automatically mapped to:

- **OWASP**: Top 10, Testing Guide, Risk Rating
- **NIST**: CSF Categories, Risk Levels, Controls
- **PCI-DSS**: Requirement IDs, Remediation Priority
- **ISO 27001**: Control Objectives, Implementation Status

## Security Considerations

- All credentials encrypted at rest
- API keys stored securely (environment variables)
- Sensitive data redacted in export reports
- Audit logging of all operations
- Role-based access control (RBAC)

## License

Proprietary - For authorized penetration testing only

## Support

For issues, documentation, or tool integration requests, refer to `docs/SUPPORT.md`

---

**Version**: 1.0.0  
**Last Updated**: 2026-09-21  
**Status**: Active Development
