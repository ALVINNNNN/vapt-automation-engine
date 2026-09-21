"""
Custom exceptions for VAPT Automation Engine
"""


class VAPTException(Exception):
    """Base exception for VAPT Automation Engine"""
    pass


class ConfigurationError(VAPTException):
    """Configuration loading or parsing error"""
    pass


class ToolNotFoundError(VAPTException):
    """Required security tool not found"""
    pass


class ToolIntegrationError(VAPTException):
    """Error integrating with security tool"""
    pass


class ScanError(VAPTException):
    """Error during scan execution"""
    pass


class ScanNotFoundError(ScanError):
    """Scan not found in database"""
    pass


class InvalidScanStateError(ScanError):
    """Invalid scan state transition"""
    pass


class ResultProcessingError(VAPTException):
    """Error processing scan results"""
    pass


class ReportGenerationError(VAPTException):
    """Error generating report"""
    pass


class FrameworkMappingError(VAPTException):
    """Error mapping findings to compliance framework"""
    pass


class AuthenticationError(VAPTException):
    """Authentication failed"""
    pass


class AuthorizationError(VAPTException):
    """Authorization failed (insufficient permissions)"""
    pass


class APIError(VAPTException):
    """API error"""
    pass


class DatabaseError(VAPTException):
    """Database operation error"""
    pass


class ValidationError(VAPTException):
    """Input validation error"""
    pass


class TimeoutError(VAPTException):
    """Operation timeout"""
    pass


class ToolExecutionError(VAPTException):
    """Error executing external tool"""
    pass


class ToolVersionError(VAPTException):
    """Tool version incompatibility"""
    pass


class EnvironmentError(VAPTException):
    """Environment configuration error"""
    pass
