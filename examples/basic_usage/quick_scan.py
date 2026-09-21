#!/usr/bin/env python3
"""
Basic example: Quick network and application scan

This example demonstrates:
1. Creating a scan configuration
2. Executing a scan
3. Retrieving results
4. Generating a report
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.logger import get_logger
from src.config import get_config
from src.core.engine import VAPTEngine
from src.core.scan_manager import ScanManager

logger = get_logger(__name__)


def main():
    """Run a quick scan example"""

    # Initialize configuration
    config = get_config()
    logger.info(f"Loaded configuration from {config.config_path}")

    # Initialize VAPT Engine
    engine = VAPTEngine(config)
    logger.info("Initialized VAPT Engine")

    # Create scan manager
    scan_manager = ScanManager(engine)

    # Define scan targets
    scan_config = {
        "name": "Quick Scan Example",
        "description": "Quick security assessment example",
        "targets": {
            "hosts": ["192.168.1.1"],
            "urls": ["https://example.com"]
        },
        "nvapt": {
            "enabled": True,
            "nmap": {
                "enabled": True,
                "scan_type": "top-1000"
            }
        },
        "avapt": {
            "enabled": True,
            "owasp_zap": {
                "enabled": True,
                "quick_scan": True
            }
        },
        "compliance": {
            "owasp_top10": True
        }
    }

    try:
        # Create scan
        logger.info("Creating scan...")
        scan = scan_manager.create_scan(scan_config)
        logger.info(f"Created scan: {scan['id']}")

        # Execute scan
        logger.info("Starting scan execution...")
        result = engine.execute_scan(scan['id'])

        if result['success']:
            logger.info(f"Scan completed successfully")
            logger.info(f"Findings: {result['findings_count']}")
            logger.info(f"Critical: {result['critical_count']}")
            logger.info(f"High: {result['high_count']}")
        else:
            logger.error(f"Scan failed: {result['error']}")
            return 1

        # Generate report
        logger.info("Generating report...")
        report = engine.generate_report(
            scan_id=scan['id'],
            format='html',
            template='technical'
        )
        logger.info(f"Report generated: {report['path']}")

        return 0

    except Exception as e:
        logger.error(f"Error during scan: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
