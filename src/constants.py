"""
Global constants for VAPT Automation Engine
"""

# Application
APP_NAME = "VAPT Automation Engine"
APP_VERSION = "1.0.0"

# Scan Types
SCAN_TYPE_NVAPT = "nVAPT"  # Network VAPT
SCAN_TYPE_AVAPT = "AVAPT"  # Application VAPT

# Scan States
SCAN_STATE_PENDING = "pending"
SCAN_STATE_RUNNING = "running"
SCAN_STATE_PAUSED = "paused"
SCAN_STATE_COMPLETED = "completed"
SCAN_STATE_FAILED = "failed"
SCAN_STATE_CANCELLED = "cancelled"

# Severity Levels
SEVERITY_CRITICAL = "critical"
SEVERITY_HIGH = "high"
SEVERITY_MEDIUM = "medium"
SEVERITY_LOW = "low"
SEVERITY_INFO = "info"

SEVERITY_LEVELS = {
    SEVERITY_CRITICAL: 5,
    SEVERITY_HIGH: 4,
    SEVERITY_MEDIUM: 3,
    SEVERITY_LOW: 2,
    SEVERITY_INFO: 1,
}

# Compliance Frameworks
FRAMEWORK_OWASP_TOP10 = "OWASP Top 10"
FRAMEWORK_OWASP_ASVS = "OWASP ASVS"
FRAMEWORK_NIST_CSF = "NIST Cybersecurity Framework"
FRAMEWORK_NIST_800_53 = "NIST 800-53"
FRAMEWORK_PCI_DSS = "PCI-DSS"
FRAMEWORK_ISO27001 = "ISO 27001"
FRAMEWORK_HIPAA = "HIPAA"

# Report Formats
REPORT_FORMAT_JSON = "json"
REPORT_FORMAT_CSV = "csv"
REPORT_FORMAT_XML = "xml"
REPORT_FORMAT_HTML = "html"
REPORT_FORMAT_PDF = "pdf"
REPORT_FORMAT_MARKDOWN = "markdown"
REPORT_FORMAT_SARIF = "sarif"

# Report Templates
REPORT_TEMPLATE_EXECUTIVE = "executive"
REPORT_TEMPLATE_TECHNICAL = "technical"
REPORT_TEMPLATE_COMPLIANCE = "compliance"
REPORT_TEMPLATE_CUSTOM = "custom"

# Tools
TOOL_NMAP = "nmap"
TOOL_METASPLOIT = "metasploit"
TOOL_BURP = "burp"
TOOL_SSLYZE = "sslyze"
TOOL_OWASP_ZAP = "owasp_zap"
TOOL_NIKTO = "nikto"
TOOL_SQLMAP = "sqlmap"
TOOL_OPENVAS = "openvas"
TOOL_NESSUS = "nessus"

# Default Timeouts
DEFAULT_TOOL_TIMEOUT = 3600  # 1 hour
DEFAULT_API_TIMEOUT = 300    # 5 minutes
DEFAULT_SCAN_TIMEOUT = 7200  # 2 hours

# Database
DEFAULT_DB_URL = "sqlite:///./vapt.db"
DEFAULT_DB_ECHO = False

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 500

# API Configuration
API_V1_PREFIX = "/api/v1"
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]
