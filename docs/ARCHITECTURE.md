# VAPT Automation Engine - System Architecture

## Overview

The VAPT Automation Engine is a professional-grade penetration testing automation framework designed to support both Network VAPT (nVAPT) and Application VAPT (AVAPT). It integrates multiple security tools, maps findings to compliance frameworks, and generates comprehensive reports in multiple formats.

## Architecture Layers

```
┌─────────────────────────────────────────────┐
│         User Interfaces                      │
│  (CLI, REST API, Web UI, Webhooks)          │
├─────────────────────────────────────────────┤
│         Core Orchestration                   │
│  (Scan Manager, State Machine, Scheduler)   │
├─────────────────────────────────────────────┤
│         Scanner Implementations              │
│  (nVAPT & AVAPT Scanners)                   │
├─────────────────────────────────────────────┤
│         Tool Integrations                    │
│  (Nmap, Burp, Metasploit, etc.)             │
├─────────────────────────────────────────────┤
│         Processing & Analysis                │
│  (Aggregation, Classification, Enrichment)  │
├─────────────────────────────────────────────┤
│         Compliance Frameworks                │
│  (OWASP, NIST, PCI-DSS, ISO 27001)          │
├─────────────────────────────────────────────┤
│         Report Generation                    │
│  (HTML, PDF, JSON, CSV, Markdown)           │
├─────────────────────────────────────────────┤
│         Data & Persistence                   │
│  (Database, Cache, File Storage)            │
└─────────────────────────────────────────────┘
```

## Core Components

### 1. Core Engine (src/core/)
- **engine.py**: Main orchestration engine that coordinates the entire scanning workflow
- **scan_manager.py**: Manages scan lifecycle (creation, execution, cleanup)
- **state_machine.py**: Manages scan states and transitions
- **scheduler.py**: Handles task scheduling and parallel execution
- **progress_tracker.py**: Monitors and reports scan progress in real-time

### 2. Frameworks (src/frameworks/)
Maps vulnerabilities and findings to compliance frameworks:
- **OWASP**: Top 10, ASVS
- **NIST**: Cybersecurity Framework, 800-53
- **PCI-DSS**: Payment Card Industry requirements
- **ISO 27001**: Information security controls
- **HIPAA**: Healthcare data protection

### 3. Scanners (src/scanners/)

#### Network VAPT (nVAPT)
- Nmap: Port scanning and OS detection
- Metasploit: Exploit framework integration
- OpenVAS: Comprehensive vulnerability scanning
- Shodan: Internet search integration

#### Application VAPT (AVAPT)
- Burp Suite Professional: Web application testing
- OWASP ZAP: Open-source web scanner
- sslyze: SSL/TLS security assessment
- Nikto: Web server scanning
- SQLMap: SQL injection testing

### 4. Tool Integrations (src/integrations/)
Each tool has dedicated integration code:
- API clients for remote communication
- Result parsers for output normalization
- Configuration management
- Authentication handling

### 5. Data Processing (src/processors/)
- **result_aggregator.py**: Combines results from multiple tools
- **vulnerability_classifier.py**: Categorizes findings by type and severity
- **risk_calculator.py**: Computes CVSS scores and risk ratings
- **deduplication.py**: Removes duplicate findings
- **enrichment.py**: Adds CVE/CWE metadata

### 6. Report Generation (src/reports/)
- **report_builder.py**: Constructs reports with findings
- **Formats**: JSON, CSV, XML, HTML, PDF, Markdown, SARIF
- **Templates**: Executive, Technical, Compliance
- **Renderers**: HTML, PDF with interactive features and styling

### 7. REST API (src/api/)
- FastAPI-based REST API
- WebSocket support for real-time updates
- Authentication and authorization middleware
- CORS and rate limiting

### 8. CLI (src/cli/)
- Command-line interface for all operations
- Scan management
- Report generation
- Configuration management

## Data Flow

### Scan Execution Flow

```
1. User initiates scan
   ↓
2. Scan Manager creates scan job
   ↓
3. State Machine transitions to RUNNING
   ↓
4. Scheduler dispatches to appropriate scanner
   ↓
5. Scanner invokes tool integrations
   ↓
6. Tools execute (Nmap, Burp, etc.)
   ↓
7. Results collected and normalized
   ↓
8. Result Processor handles:
   - Aggregation of multi-tool results
   - Classification by severity
   - Risk scoring
   - Deduplication
   - Enrichment
   ↓
9. Compliance Framework Mapper correlates findings
   ↓
10. Report Generator creates output
    ↓
11. Reports saved and indexed
    ↓
12. State Machine transitions to COMPLETED
    ↓
13. Scan completed (user notified)
```

## Tool Integration Pattern

Each tool integration follows this pattern:

```
Tool-Specific Wrapper
    ↓
Tool Configuration
    ↓
Tool API Client
    ↓
Tool Execution
    ↓
Raw Result Output
    ↓
Result Parser
    ↓
Normalized Finding Schema
    ↓
Common Processing Pipeline
```

## Compliance Framework Mapping

```
Raw Finding
    ↓
Finding Classifier
    (Type: SQL Injection, OS Detection, etc.)
    ↓
Framework Mapper
    (OWASP Top 10 #1, NIST AC-6, PCI-DSS 6.5.1)
    ↓
Compliance Report
    (Organized by framework control/requirement)
```

## Database Schema Overview

### Core Tables
- **scans**: Scan jobs and metadata
- **findings**: Individual vulnerabilities discovered
- **compliance_mappings**: Framework control associations
- **tools**: Tool configurations and versions
- **reports**: Generated report metadata
- **scan_results**: Aggregated scan results

## Deployment Architecture

### Standalone
- Single machine installation
- SQLite database
- Direct tool access

### Containerized (Docker)
- Multi-container application
- PostgreSQL database
- Microservice-ready architecture

### Kubernetes
- Distributed deployment
- Horizontal scaling
- High availability
- Persistent volume storage

## Security Considerations

1. **Secrets Management**
   - Environment variables for credentials
   - Vault integration for production
   - Encrypted storage of sensitive data

2. **Authentication**
   - JWT-based API authentication
   - Role-based access control (RBAC)
   - Audit logging of all operations

3. **Data Protection**
   - Encryption of sensitive findings
   - Audit trails for compliance
   - Secure result storage

## Extensibility Points

1. **Custom Scanners**: Implement base_scanner.py interface
2. **Custom Frameworks**: Add compliance framework mappings
3. **Custom Report Formats**: Implement formatter interface
4. **Tool Integrations**: Add new tool wrappers
5. **Processors**: Add custom result processing logic

## Performance Considerations

1. **Caching**: Redis for frequently accessed data
2. **Database Optimization**: Indexes on scan ID, severity, framework
3. **Parallel Execution**: Concurrent scanner execution
4. **Lazy Loading**: Load findings on-demand
5. **Result Streaming**: Stream large reports

## Scalability

- **Horizontal Scaling**: Kubernetes for scan distribution
- **Vertical Scaling**: Database optimization and caching
- **Tool Distribution**: Distribute tool execution across nodes
- **Result Aggregation**: Efficient multi-scan correlation

## Monitoring & Logging

- Centralized logging (ELK stack or similar)
- Performance metrics (Prometheus/Grafana)
- Alert system for critical findings
- Audit logs for compliance
