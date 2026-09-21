# VAPT Automation Engine - Directory Structure

## Project Layout

```
vapt-automation-engine/
│
├── README.md                                 # Project overview and quick start
├── LICENSE                                   # MIT License
├── CHANGELOG.md                              # Version history
├── CONTRIBUTING.md                           # Contribution guidelines
├── DIRECTORY_STRUCTURE.md                    # This file
├── requirements.txt                          # Python dependencies
├── setup.py                                  # Package installation script
├── setup.cfg                                 # Setup configuration
├── pyproject.toml                            # Modern Python packaging config
├── .env.example                              # Environment variables template
├── .gitignore                                # Git ignore rules
├── .dockerignore                             # Docker ignore rules
├── .editorconfig                             # Editor configuration
├── .pre-commit-config.yaml                   # Pre-commit hooks
│
├── src/                                      # Core application source code
│   ├── __init__.py
│   ├── main.py                               # Application entry point
│   ├── config.py                             # Configuration management
│   ├── logger.py                             # Logging configuration
│   ├── constants.py                          # Global constants
│   ├── exceptions.py                         # Custom exceptions
│   │
│   ├── core/                                 # Core orchestration engine
│   │   ├── __init__.py
│   │   ├── engine.py                         # Main orchestration engine
│   │   ├── scan_manager.py                   # Scan lifecycle management
│   │   ├── state_machine.py                  # Scan state management
│   │   ├── scheduler.py                      # Task scheduling
│   │   └── progress_tracker.py               # Progress monitoring
│   │
│   ├── frameworks/                           # Compliance framework implementations
│   │   ├── __init__.py
│   │   ├── base_framework.py                 # Abstract base framework
│   │   ├── owasp/                            # OWASP compliance
│   │   │   ├── __init__.py
│   │   │   ├── owasp_top_10.py               # OWASP Top 10
│   │   │   ├── owasp_asvs.py                 # ASVS framework
│   │   │   └── mappings.json                 # Vulnerability mappings
│   │   ├── nist/                             # NIST compliance
│   │   │   ├── __init__.py
│   │   │   ├── nist_csf.py                   # NIST Cybersecurity Framework
│   │   │   ├── nist_800_53.py                # NIST 800-53 controls
│   │   │   └── mappings.json                 # Control mappings
│   │   ├── pci_dss/                          # PCI-DSS compliance
│   │   │   ├── __init__.py
│   │   │   ├── pci_dss_requirements.py       # PCI-DSS requirements
│   │   │   └── mappings.json                 # Requirement mappings
│   │   ├── iso27001/                         # ISO 27001 compliance
│   │   │   ├── __init__.py
│   │   │   ├── iso27001_controls.py          # ISO 27001 controls
│   │   │   └── mappings.json                 # Control mappings
│   │   └── hipaa/                            # HIPAA compliance (bonus)
│   │       ├── __init__.py
│   │       ├── hipaa_requirements.py
│   │       └── mappings.json
│   │
│   ├── scanners/                             # Network and application scanners
│   │   ├── __init__.py
│   │   ├── base_scanner.py                   # Abstract scanner base class
│   │   ├── nvapt/                            # Network VAPT scanners
│   │   │   ├── __init__.py
│   │   │   ├── nmap_scanner.py               # Nmap integration
│   │   │   ├── metasploit_scanner.py         # Metasploit integration
│   │   │   ├── nessus_scanner.py             # Nessus integration
│   │   │   ├── openvas_scanner.py            # OpenVAS integration
│   │   │   ├── shodan_scanner.py             # Shodan integration
│   │   │   └── network_utils.py              # Network utilities
│   │   └── avapt/                            # Application VAPT scanners
│   │       ├── __init__.py
│   │       ├── burp_scanner.py               # Burp Suite Professional
│   │       ├── owasp_zap_scanner.py          # OWASP ZAP integration
│   │       ├── sslyze_scanner.py             # SSL/TLS scanning
│   │       ├── nikto_scanner.py              # Web server scanning
│   │       ├── sqlmap_scanner.py             # SQL injection testing
│   │       └── app_utils.py                  # Application utilities
│   │
│   ├── integrations/                         # Third-party tool integrations
│   │   ├── __init__.py
│   │   ├── burp/
│   │   │   ├── __init__.py
│   │   │   ├── burp_api_client.py            # Burp REST API client
│   │   │   ├── scan_config.py                # Scan configurations
│   │   │   └── result_parser.py              # Result parsing
│   │   ├── metasploit/
│   │   │   ├── __init__.py
│   │   │   ├── msf_rpc_client.py             # Metasploit RPC client
│   │   │   ├── exploit_loader.py             # Exploit management
│   │   │   └── result_parser.py              # Result parsing
│   │   ├── nmap/
│   │   │   ├── __init__.py
│   │   │   ├── nmap_wrapper.py               # Nmap Python wrapper
│   │   │   ├── port_analysis.py              # Port analysis
│   │   │   └── result_parser.py              # Result parsing
│   │   ├── sslyze/
│   │   │   ├── __init__.py
│   │   │   ├── ssl_analyzer.py               # SSL/TLS analyzer
│   │   │   └── result_parser.py              # Result parsing
│   │   └── common/
│   │       ├── __init__.py
│   │       ├── tool_detector.py              # Detect installed tools
│   │       ├── environment_checker.py        # Environment validation
│   │       └── version_manager.py            # Tool version tracking
│   │
│   ├── data/                                 # Data models and processing
│   │   ├── __init__.py
│   │   ├── models.py                         # Data models (Pydantic)
│   │   ├── schemas.py                        # Data schemas
│   │   ├── database.py                       # Database abstraction layer
│   │   └── cache.py                          # Caching layer
│   │
│   ├── processors/                           # Result processing and analysis
│   │   ├── __init__.py
│   │   ├── result_aggregator.py              # Aggregate multi-tool results
│   │   ├── vulnerability_classifier.py       # Classify vulnerabilities
│   │   ├── risk_calculator.py                # Risk scoring (CVSS)
│   │   ├── deduplication.py                  # Remove duplicate findings
│   │   └── enrichment.py                     # Enrich findings with metadata
│   │
│   ├── reports/                              # Report generation
│   │   ├── __init__.py
│   │   ├── report_builder.py                 # Main report builder
│   │   ├── report_generator.py               # Report orchestration
│   │   ├── formats/
│   │   │   ├── __init__.py
│   │   │   ├── base_formatter.py             # Abstract formatter
│   │   │   ├── json_formatter.py             # JSON output
│   │   │   ├── csv_formatter.py              # CSV output
│   │   │   ├── xml_formatter.py              # XML output (OWASP ZAP)
│   │   │   ├── html_formatter.py             # HTML output
│   │   │   ├── pdf_formatter.py              # PDF output
│   │   │   ├── markdown_formatter.py         # Markdown output
│   │   │   └── sarif_formatter.py            # SARIF format
│   │   ├── templates/
│   │   │   ├── __init__.py
│   │   │   ├── executive_summary.py          # Executive report template
│   │   │   ├── technical_report.py           # Technical report template
│   │   │   ├── compliance_report.py          # Compliance report template
│   │   │   └── custom_report.py              # Custom report builder
│   │   └── renderers/
│   │       ├── __init__.py
│   │       ├── html_renderer.py              # HTML rendering
│   │       ├── pdf_renderer.py               # PDF rendering
│   │       ├── markdown_renderer.py          # Markdown rendering
│   │       └── styling.py                    # Styling and theming
│   │
│   ├── api/                                  # REST API
│   │   ├── __init__.py
│   │   ├── app.py                            # FastAPI application
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── scans.py                      # Scan endpoints
│   │   │   ├── results.py                    # Result endpoints
│   │   │   ├── reports.py                    # Report endpoints
│   │   │   ├── compliance.py                 # Compliance endpoints
│   │   │   ├── tools.py                      # Tool management endpoints
│   │   │   ├── settings.py                   # Settings endpoints
│   │   │   └── health.py                     # Health check endpoints
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                       # Authentication
│   │   │   ├── logging.py                    # Request logging
│   │   │   └── error_handler.py              # Error handling
│   │   └── websocket.py                      # WebSocket for real-time updates
│   │
│   ├── cli/                                  # Command-line interface
│   │   ├── __init__.py
│   │   ├── cli.py                            # Main CLI entry point
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── scan.py                       # Scan commands
│   │   │   ├── report.py                     # Report commands
│   │   │   ├── compliance.py                 # Compliance commands
│   │   │   ├── tool.py                       # Tool management commands
│   │   │   ├── config.py                     # Configuration commands
│   │   │   └── database.py                   # Database commands
│   │   └── formatters.py                     # CLI output formatters
│   │
│   └── utils/                                # Utility modules
│       ├── __init__.py
│       ├── validators.py                     # Input validation
│       ├── converters.py                     # Data conversion
│       ├── encryption.py                     # Encryption utilities
│       ├── file_utils.py                     # File operations
│       ├── network_utils.py                  # Network utilities
│       ├── time_utils.py                     # Time/date utilities
│       └── version.py                        # Version information
│
├── config/                                   # Configuration files and templates
│   ├── default_config.yaml                   # Default configuration
│   ├── default_config.json                   # JSON alternative
│   ├── profiles/                             # Scan profiles
│   │   ├── quick_scan.yaml                   # Quick scan profile
│   │   ├── standard_scan.yaml                # Standard scan profile
│   │   ├── comprehensive_scan.yaml           # Comprehensive scan profile
│   │   ├── compliance_scan.yaml              # Compliance-focused scan
│   │   ├── custom_scan.template              # Custom scan template
│   │   ├── nvapt/
│   │   │   ├── network_basic.yaml
│   │   │   ├── network_advanced.yaml
│   │   │   └── network_compliance.yaml
│   │   └── avapt/
│   │       ├── web_basic.yaml
│   │       ├── web_advanced.yaml
│   │       ├── api_testing.yaml
│   │       └── mobile_testing.yaml
│   ├── tools/                                # Tool configurations
│   │   ├── burp_config.yaml
│   │   ├── metasploit_config.yaml
│   │   ├── nmap_config.yaml
│   │   ├── sslyze_config.yaml
│   │   └── zap_config.yaml
│   ├── frameworks/                           # Compliance framework configs
│   │   ├── owasp_top10_v2021.yaml
│   │   ├── owasp_asvs_4.0.yaml
│   │   ├── nist_csf_2024.yaml
│   │   ├── nist_800_53_rev5.yaml
│   │   ├── pci_dss_3.2.1.yaml
│   │   ├── iso27001_2022.yaml
│   │   └── hipaa_config.yaml
│   ├── report_templates/                     # Report template configs
│   │   ├── executive_config.yaml
│   │   ├── technical_config.yaml
│   │   └── compliance_config.yaml
│   └── environments/                         # Environment-specific configs
│       ├── development.yaml
│       ├── staging.yaml
│       ├── production.yaml
│       ├── linux.yaml
│       └── windows.yaml
│
├── templates/                                # Report and output templates
│   ├── html/
│   │   ├── base.html
│   │   ├── executive_report.html
│   │   ├── technical_report.html
│   │   ├── compliance_report.html
│   │   ├── vulnerability_detail.html
│   │   ├── assets/
│   │   │   ├── style.css
│   │   │   ├── responsive.css
│   │   │   ├── print.css
│   │   │   ├── script.js
│   │   │   ├── chart.js
│   │   │   └── images/
│   │   │       ├── logo.png
│   │   │       ├── icons/
│   │   │       └── backgrounds/
│   │   └── layouts/
│   │       ├── single_column.html
│   │       ├── two_column.html
│   │       └── dashboard.html
│   ├── pdf/
│   │   ├── base_template.html
│   │   ├── executive_template.html
│   │   ├── technical_template.html
│   │   ├── compliance_template.html
│   │   └── styles.css
│   ├── markdown/
│   │   ├── base_template.md
│   │   ├── executive_template.md
│   │   └── technical_template.md
│   ├── email/
│   │   ├── scan_started.html
│   │   ├── scan_completed.html
│   │   └── scan_failed.html
│   └── custom/
│       └── README.md
│
├── data/                                     # Data storage and examples
│   ├── sample_scans/                         # Sample scan configurations
│   │   ├── sample_nvapt.json
│   │   ├── sample_avapt.json
│   │   └── sample_compliance.json
│   ├── sample_results/                       # Sample result files
│   │   ├── nmap_sample.xml
│   │   ├── burp_sample.json
│   │   ├── metasploit_sample.json
│   │   └── zap_sample.xml
│   ├── compliance_mappings/                  # Compliance framework mappings
│   │   ├── owasp_cwe_mapping.json
│   │   ├── nist_mapping.json
│   │   ├── pci_mapping.json
│   │   ├── iso27001_mapping.json
│   │   └── cve_reference.json
│   └── databases/
│       ├── vulnerability_db.sql
│       ├── compliance_db.sql
│       └── tool_db.sql
│
├── tests/                                    # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── pytest.ini
│   ├── coverage.ini
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_config.py
│   │   ├── test_core/
│   │   ├── test_frameworks/
│   │   ├── test_scanners/
│   │   ├── test_processors/
│   │   ├── test_reports/
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_scanner_integration.py
│   │   ├── test_report_generation.py
│   │   └── test_api.py
│   ├── fixtures/
│   │   ├── sample_data.json
│   │   ├── mock_tools.py
│   │   └── mock_results.py
│   └── e2e/
│       ├── test_full_workflow.py
│       └── test_compliance_scan.py
│
├── scripts/                                  # Utility scripts
│   ├── install_dependencies.sh               # Install script (Linux)
│   ├── install_dependencies.ps1              # Install script (Windows)
│   ├── setup_environment.sh                  # Setup environment
│   ├── verify_tools.sh                       # Verify tool installation
│   ├── generate_sample_report.sh             # Generate sample reports
│   ├── update_compliance_db.py               # Update compliance database
│   ├── migrate_database.py                   # Database migration
│   ├── backup_results.py                     # Backup utility
│   └── cleanup_old_scans.py                  # Cleanup utility
│
├── docker/                                   # Docker configuration
│   ├── Dockerfile
│   ├── Dockerfile.windows
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod.yml
│   ├── .dockerignore
│   └── entrypoint.sh
│
├── kubernetes/                               # Kubernetes configuration
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── pvc.yaml
│   ├── hpa.yaml
│   └── kustomization.yaml
│
├── ansible/                                  # Ansible playbooks
│   ├── site.yml
│   ├── requirements.yml
│   ├── inventory/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   │       ├── vapt_servers.yml
│   │       └── all.yml
│   ├── roles/
│   │   ├── common/
│   │   ├── dependencies/
│   │   ├── vapt_engine/
│   │   ├── tools/
│   │   └── database/
│   └── plays/
│       ├── install.yml
│       ├── configure.yml
│       └── update.yml
│
├── examples/                                 # Usage examples
│   ├── README.md
│   ├── basic_usage/
│   │   ├── quick_scan.py
│   │   ├── quick_scan_cli.sh
│   │   └── generate_report.py
│   ├── advanced_usage/
│   │   ├── custom_scan_profile.py
│   │   ├── api_integration.py
│   │   ├── webhook_integration.py
│   │   └── multi_target_scan.py
│   ├── compliance/
│   │   ├── owasp_scan.py
│   │   ├── nist_scan.py
│   │   ├── pci_dss_scan.py
│   │   └── iso27001_scan.py
│   ├── tool_integration/
│   │   ├── burp_integration.py
│   │   ├── metasploit_example.py
│   │   ├── nmap_example.py
│   │   └── sslyze_example.py
│   ├── report_generation/
│   │   ├── html_report.py
│   │   ├── pdf_report.py
│   │   ├── executive_report.py
│   │   └── compliance_report.py
│   ├── scheduled_scans/
│   │   ├── scheduled_scan.py
│   │   └── cron_setup.sh
│   └── configs/
│       ├── sample_config.yaml
│       ├── sample_nvapt_profile.yaml
│       ├── sample_avapt_profile.yaml
│       └── custom_framework_config.yaml
│
├── deployment/                               # Deployment guides and scripts
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── linux/
│   │   ├── ubuntu_install.md
│   │   ├── centos_install.md
│   │   ├── kali_install.md
│   │   └── install.sh
│   ├── windows/
│   │   ├── windows_install.md
│   │   ├── powershell_install.ps1
│   │   ├── wsl_install.md
│   │   └── docker_windows.md
│   ├── cloud/
│   │   ├── aws_deployment.md
│   │   ├── azure_deployment.md
│   │   ├── gcp_deployment.md
│   │   ├── cloudformation.yaml
│   │   └── terraform/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── outputs.tf
│   ├── standalone/
│   │   ├── standalone_setup.md
│   │   └── configuration_wizard.py
│   └── upgrade/
│       ├── migration_guide.md
│       └── upgrade_script.sh
│
├── docs/                                     # Documentation
│   ├── index.md
│   ├── README.md
│   ├── getting_started/
│   │   ├── INSTALLATION.md
│   │   ├── QUICK_START.md
│   │   ├── CONFIGURATION.md
│   │   └── FIRST_SCAN.md
│   ├── user_guide/
│   │   ├── overview.md
│   │   ├── cli_usage.md
│   │   ├── web_ui.md
│   │   ├── api_reference.md
│   │   ├── scan_profiles.md
│   │   ├── report_generation.md
│   │   ├── compliance_mapping.md
│   │   └── advanced_usage.md
│   ├── compliance/
│   │   ├── owasp_guide.md
│   │   ├── nist_guide.md
│   │   ├── pci_dss_guide.md
│   │   ├── iso27001_guide.md
│   │   ├── hipaa_guide.md
│   │   └── framework_mapping.md
│   ├── architecture/
│   │   ├── ARCHITECTURE.md
│   │   ├── component_design.md
│   │   ├── data_flow.md
│   │   ├── integration_points.md
│   │   └── scalability.md
│   ├── tool_integration/
│   │   ├── burp_suite.md
│   │   ├── metasploit.md
│   │   ├── nmap.md
│   │   ├── sslyze.md
│   │   ├── owasp_zap.md
│   │   ├── custom_tools.md
│   │   └── tool_requirements.md
│   ├── api/
│   │   ├── api_overview.md
│   │   ├── authentication.md
│   │   ├── endpoints.md
│   │   ├── examples.md
│   │   ├── webhooks.md
│   │   └── websocket.md
│   ├── database/
│   │   ├── schema.md
│   │   ├── migrations.md
│   │   ├── backup_restore.md
│   │   └── optimization.md
│   ├── security/
│   │   ├── authentication.md
│   │   ├── authorization.md
│   │   ├── encryption.md
│   │   ├── secrets_management.md
│   │   ├── audit_logging.md
│   │   └── security_best_practices.md
│   ├── deployment/
│   │   ├── linux_deployment.md
│   │   ├── windows_deployment.md
│   │   ├── docker_deployment.md
│   │   ├── kubernetes_deployment.md
│   │   ├── cloud_deployment.md
│   │   └── high_availability.md
│   ├── troubleshooting/
│   │   ├── common_issues.md
│   │   ├── tool_integration_issues.md
│   │   ├── report_generation_issues.md
│   │   ├── performance_tuning.md
│   │   └── logging_debugging.md
│   ├── development/
│   │   ├── development_setup.md
│   │   ├── contributing.md
│   │   ├── code_style.md
│   │   ├── testing.md
│   │   ├── plugin_development.md
│   │   └── custom_scanner.md
│   ├── release_notes/
│   │   ├── v1.0.0.md
│   │   ├── v1.1.0.md
│   │   └── changelog.md
│   └── faq/
│       ├── general_faq.md
│       ├── technical_faq.md
│       ├── compliance_faq.md
│       └── troubleshooting_faq.md
│
└── .github/                                  # GitHub configuration
    ├── workflows/
    │   ├── ci.yml
    │   ├── tests.yml
    │   ├── security_scan.yml
    │   ├── release.yml
    │   └── docs_deploy.yml
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   ├── feature_request.md
    │   └── compliance_issue.md
    ├── PULL_REQUEST_TEMPLATE/
    │   └── pull_request_template.md
    └── dependabot.yml
```

## Key Directories Explained

### `/src/` - Core Application
Houses all Python source code organized by functionality:
- **core/**: Orchestration engine and scan management
- **frameworks/**: Compliance framework implementations
- **scanners/**: nVAPT and AVAPT scanner implementations
- **integrations/**: Tool-specific API clients and parsers
- **reports/**: Multi-format report generation
- **api/**: FastAPI REST API implementation
- **cli/**: Command-line interface

### `/config/` - Configuration Files
- **profiles/**: Pre-defined scan profiles
- **tools/**: Tool-specific configurations
- **frameworks/**: Framework-specific configurations
- **environments/**: Environment-specific settings

### `/templates/` - Report Templates
- **html/**: HTML report templates and assets
- **pdf/**: PDF report templates
- **markdown/**: Markdown report templates
- **email/**: Email notification templates

### `/tests/` - Test Suite
- **unit/**: Unit tests for individual components
- **integration/**: Integration tests for component interactions
- **e2e/**: End-to-end workflow tests
- **fixtures/**: Test data and fixtures

### `/docs/` - Documentation
Comprehensive documentation organized by topic:
- **getting_started/**: Installation and quick start
- **user_guide/**: User documentation
- **compliance/**: Compliance framework guides
- **architecture/**: System design documentation
- **api/**: API documentation
- **deployment/**: Deployment guides

### `/deployment/` - Deployment Resources
- **linux/**: Linux-specific deployment guides
- **windows/**: Windows deployment guides
- **cloud/**: Cloud provider deployment (AWS, Azure, GCP)
- **kubernetes/**: Kubernetes manifests

### `/examples/` - Usage Examples
- **basic_usage/**: Simple examples
- **advanced_usage/**: Complex scenarios
- **compliance/**: Compliance-specific examples
- **tool_integration/**: Tool-specific examples

## File Organization Principles

1. **Modularity**: Each component is self-contained
2. **Scalability**: Directory structure supports growth
3. **Clarity**: Names clearly indicate purpose
4. **Separation**: Code, config, and data are separate
5. **Documentation**: Every section has documentation
6. **Testing**: Parallel test structure to src/

## Getting Started

1. Read `/docs/getting_started/INSTALLATION.md`
2. Review `/docs/getting_started/QUICK_START.md`
3. Check `/examples/` for usage patterns
4. Explore `/docs/ARCHITECTURE.md` for system design

## Next Steps

- Configure tools in `/config/tools/`
- Customize scan profiles in `/config/profiles/`
- Review compliance frameworks in `/src/frameworks/`
- Check deployment guides in `/deployment/`
