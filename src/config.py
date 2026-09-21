"""
Configuration management for VAPT Automation Engine
"""

import os
import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict

from src.logger import get_logger
from src.exceptions import ConfigurationError

logger = get_logger(__name__)


@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str = "sqlite:///./vapt.db"
    echo: bool = False
    pool_size: int = 20
    max_overflow: int = 40


@dataclass
class APIConfig:
    """API configuration"""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    workers: int = 4
    timeout: int = 300


@dataclass
class ScanConfig:
    """Default scan configuration"""
    default_timeout: int = 3600  # 1 hour
    max_concurrent_scans: int = 5
    result_retention_days: int = 90


@dataclass
class ReportConfig:
    """Report generation configuration"""
    output_dir: str = "./reports"
    default_format: str = "html"
    include_raw_findings: bool = True
    include_compliance_mapping: bool = True


class Config:
    """Main configuration manager"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration

        Args:
            config_path: Path to configuration file (YAML or JSON)
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config_data: Dict[str, Any] = {}
        self._load_config()
        self._initialize_subdirs()

    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        env = os.getenv("VAPT_ENV", "development")
        config_dir = Path(__file__).parent.parent / "config"

        # Try environment-specific config first
        env_config = config_dir / f"{env}.yaml"
        if env_config.exists():
            return str(env_config)

        # Fall back to default config
        default_config = config_dir / "default_config.yaml"
        if default_config.exists():
            return str(default_config)

        # If no config file exists, return default path
        return str(default_config)

    def _load_config(self):
        """Load configuration from file"""
        if not Path(self.config_path).exists():
            logger.warning(f"Configuration file not found: {self.config_path}")
            self.config_data = self._get_default_config()
            return

        try:
            with open(self.config_path, 'r') as f:
                if self.config_path.endswith('.json'):
                    self.config_data = json.load(f)
                else:  # YAML
                    self.config_data = yaml.safe_load(f) or {}
            logger.info(f"Loaded configuration from {self.config_path}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "database": asdict(DatabaseConfig()),
            "api": asdict(APIConfig()),
            "scan": asdict(ScanConfig()),
            "report": asdict(ReportConfig()),
        }

    def _initialize_subdirs(self):
        """Initialize required subdirectories"""
        report_dir = Path(self.get("report.output_dir", "./reports"))
        report_dir.mkdir(parents=True, exist_ok=True)

        logs_dir = Path(__file__).parent.parent / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value with dot notation

        Examples:
            config.get("database.url")
            config.get("api.port", 8000)
        """
        keys = key.split(".")
        value = self.config_data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def set(self, key: str, value: Any):
        """Set configuration value with dot notation"""
        keys = key.split(".")
        config = self.config_data

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def get_database_config(self) -> DatabaseConfig:
        """Get database configuration"""
        db_config = self.get("database", {})
        return DatabaseConfig(**db_config)

    def get_api_config(self) -> APIConfig:
        """Get API configuration"""
        api_config = self.get("api", {})
        return APIConfig(**api_config)

    def get_scan_config(self) -> ScanConfig:
        """Get scan configuration"""
        scan_config = self.get("scan", {})
        return ScanConfig(**scan_config)

    def get_report_config(self) -> ReportConfig:
        """Get report configuration"""
        report_config = self.get("report", {})
        return ReportConfig(**report_config)

    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return self.config_data.copy()


# Global configuration instance
_config: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get or initialize global configuration"""
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config


def reset_config():
    """Reset global configuration (for testing)"""
    global _config
    _config = None
