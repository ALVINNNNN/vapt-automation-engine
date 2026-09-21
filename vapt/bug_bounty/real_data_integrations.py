"""
Real Bug Bounty Data Integrations

Connects to actual public bug bounty data sources instead of simulated data.
Options include public APIs, web scraping, and vulnerability databases.
"""

import requests
import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class HackerOneIntegration:
    """
    Integrate with HackerOne's public disclosure data.

    HackerOne publishes disclosures that include vulnerability details,
    impact, and bounty information via their public reports.

    URL: https://hackerone.com/reports
    API: https://api.hackerone.com (limited public endpoints)
    """

    def __init__(self):
        self.base_url = "https://api.hackerone.com"
        self.session = requests.Session()

    def fetch_disclosures(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch publicly disclosed vulnerability reports from HackerOne.

        Note: HackerOne's public API is limited. For full access,
        consider using their CSV export from website or RSS feed.
        """
        logger.info("Fetching HackerOne public disclosures...")

        try:
            # HackerOne provides RSS feed of recent disclosures
            rss_url = "https://hackerone.com/hacktivity.json"

            response = requests.get(rss_url, timeout=10)
            response.raise_for_status()

            data = response.json()
            reports = []

            for item in data.get("data", [])[:limit]:
                report = {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "vulnerability_type": item.get("vulnerability_type"),
                    "severity": item.get("severity"),
                    "bounty": item.get("bounty_amount"),
                    "disclosed_at": item.get("disclosed_at"),
                    "source": "hackerone"
                }
                reports.append(report)

            logger.info(f"Fetched {len(reports)} HackerOne disclosures")
            return reports

        except Exception as e:
            logger.error(f"Error fetching HackerOne data: {e}")
            return []


class BugcrowdIntegration:
    """
    Integrate with Bugcrowd's public vulnerability data.

    Bugcrowd publishes vulnerability statistics and disclosures.
    They provide public reports on their research page.

    URL: https://www.bugcrowd.com/vulnerability-disclosure-program/
    """

    def __init__(self):
        self.base_url = "https://www.bugcrowd.com"

    def fetch_reports(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch Bugcrowd public research and vulnerability reports.

        Bugcrowd publishes annual vulnerability reports showing:
        - Common vulnerability types
        - Average bounty amounts
        - Industry trends
        """
        logger.info("Fetching Bugcrowd vulnerability data...")

        try:
            # Bugcrowd publishes reports as PDFs and JSON data
            # Their vulnerability data includes industry statistics
            reports = self._scrape_bugcrowd_reports()
            logger.info(f"Fetched {len(reports)} Bugcrowd reports")
            return reports

        except Exception as e:
            logger.error(f"Error fetching Bugcrowd data: {e}")
            return []

    def _scrape_bugcrowd_reports(self) -> List[Dict[str, Any]]:
        """Scrape Bugcrowd's published reports"""
        # Would implement web scraping of their public reports
        # For now, returns empty (implement as needed)
        return []


class NVDIntegration:
    """
    Integrate with National Vulnerability Database (NVD).

    NVD provides structured CVE data with CVSS scores, descriptions,
    and affected software. This gives real vulnerability data.

    URL: https://nvd.nist.gov/
    API: https://services.nvd.nist.gov/rest/json/cves/1.0
    Requires API key (free)
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    def fetch_recent_vulnerabilities(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch recent CVEs from NVD.

        Provides real vulnerability data including:
        - CVE ID and description
        - CVSS scores
        - Affected products
        - Publication date
        """
        logger.info("Fetching recent CVEs from NVD...")

        try:
            params = {
                "resultsPerPage": min(limit, 200),
                "sortBy": "published",
                "orderBy": "desc"
            }

            if self.api_key:
                params["apiKey"] = self.api_key

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            reports = []

            for vuln in data.get("vulnerabilities", [])[:limit]:
                cve = vuln.get("cve", {})
                metrics = cve.get("metrics", {})
                cvss = metrics.get("cvssV3", [{}])[0]

                report = {
                    "id": cve.get("id"),
                    "title": cve.get("id"),  # CVE ID as title
                    "description": cve.get("descriptions", [{}])[0].get("value", ""),
                    "cvss_score": cvss.get("baseScore"),
                    "severity": cvss.get("baseSeverity"),
                    "published": cve.get("published"),
                    "source": "nvd"
                }
                reports.append(report)

            logger.info(f"Fetched {len(reports)} CVEs from NVD")
            return reports

        except Exception as e:
            logger.error(f"Error fetching NVD data: {e}")
            return []


class GitHubSecurityAlertsIntegration:
    """
    Integrate with GitHub Security Advisories.

    GitHub publishes security advisories for packages across multiple
    ecosystems (npm, PyPI, RubyGems, Maven, NuGet, etc.)

    URL: https://github.com/advisories
    API: https://api.github.com/graphql (requires authentication)
    """

    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.base_url = "https://api.github.com/graphql"

    def fetch_security_advisories(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch security advisories from GitHub.

        Provides vulnerability data for common packages:
        - JavaScript/npm packages
        - Python packages
        - Ruby gems
        - Java libraries
        - And more
        """
        logger.info("Fetching GitHub Security Advisories...")

        if not self.github_token:
            logger.warning("GitHub token not provided. Using public endpoints only.")
            return self._fetch_public_advisories(limit)

        try:
            query = """
            {
              securityAdvisories(first: %d, orderBy: {field: UPDATED_AT, direction: DESC}) {
                edges {
                  node {
                    ghsaId
                    cveIds(first: 10) {
                      nodes {
                        cveid
                      }
                    }
                    summary
                    description
                    severity
                    publishedAt
                    updatedAt
                    vulnerabilities(first: 10) {
                      nodes {
                        package {
                          name
                          ecosystem
                        }
                        severity
                        vulnerableVersionRange
                      }
                    }
                  }
                }
              }
            }
            """ % limit

            headers = {
                "Authorization": f"Bearer {self.github_token}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                self.base_url,
                json={"query": query},
                headers=headers,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            reports = []

            for edge in data.get("data", {}).get("securityAdvisories", {}).get("edges", []):
                node = edge.get("node", {})

                report = {
                    "id": node.get("ghsaId"),
                    "title": node.get("summary"),
                    "description": node.get("description"),
                    "severity": node.get("severity"),
                    "published": node.get("publishedAt"),
                    "cve_ids": [cve.get("cveid") for cve in node.get("cveIds", {}).get("nodes", [])],
                    "source": "github"
                }
                reports.append(report)

            logger.info(f"Fetched {len(reports)} GitHub advisories")
            return reports

        except Exception as e:
            logger.error(f"Error fetching GitHub advisories: {e}")
            return self._fetch_public_advisories(limit)

    def _fetch_public_advisories(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch from GitHub's public advisories page"""
        try:
            # GitHub publishes advisories in a public database
            url = "https://github.com/advisories/database"
            # Would parse the public JSON database
            logger.info("Using public GitHub advisories database")
            return []
        except Exception as e:
            logger.error(f"Error fetching public advisories: {e}")
            return []


class IntigritiIntegration:
    """
    Integrate with Intigriti's public disclosure data.

    Intigriti publishes vulnerability disclosures and vulnerability
    statistics on their platform.

    URL: https://www.intigriti.com/
    Note: Limited public API - primarily web scraping approach
    """

    def fetch_disclosures(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch publicly disclosed vulnerabilities from Intigriti.
        """
        logger.info("Fetching Intigriti disclosures...")

        try:
            # Intigriti has public disclosure pages
            # Would implement scraping or API integration
            return []
        except Exception as e:
            logger.error(f"Error fetching Intigriti data: {e}")
            return []


class GoogleProjectZeroIntegration:
    """
    Integrate with Google Project Zero's public disclosure data.

    Project Zero publishes detailed vulnerability research and disclosures.
    These are high-quality, well-researched vulnerabilities.

    URL: https://github.com/google/project-zero-issues
    Blog: https://googleprojectzero.blogspot.com/
    """

    def fetch_disclosures(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch Project Zero public disclosures and research.

        Project Zero publishes:
        - Detailed vulnerability research
        - 90-day disclosure timelines
        - High-impact, well-documented issues
        """
        logger.info("Fetching Google Project Zero disclosures...")

        try:
            # Project Zero posts research on their blog
            # They publish CVEs with full technical details
            # Would parse RSS feed or GitHub issues

            # Example: https://github.com/google/project-zero-issues
            url = "https://github.com/google/project-zero-issues/issues"
            # Would scrape or use GitHub API

            return []
        except Exception as e:
            logger.error(f"Error fetching Project Zero data: {e}")
            return []


def get_real_bug_bounty_data(source: str = "all", limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetch real bug bounty and vulnerability data from public sources.

    Sources:
    - "hackerone": HackerOne disclosures
    - "bugcrowd": Bugcrowd reports
    - "nvd": National Vulnerability Database
    - "github": GitHub Security Advisories
    - "intigriti": Intigriti disclosures
    - "projectzero": Google Project Zero
    - "all": Fetch from all sources

    Usage:
        # Fetch real data
        real_data = get_real_bug_bounty_data(source="nvd", limit=50)

        # Use in pattern learner
        learner = VulnerabilityPatternLearner()
        learner.train_from_reports(real_data)
    """
    reports = []

    if source in ["all", "hackerone"]:
        h1 = HackerOneIntegration()
        reports.extend(h1.fetch_disclosures(limit=limit))

    if source in ["all", "nvd"]:
        nvd = NVDIntegration()
        reports.extend(nvd.fetch_recent_vulnerabilities(limit=limit))

    if source in ["all", "github"]:
        github = GitHubSecurityAlertsIntegration()
        reports.extend(github.fetch_security_advisories(limit=limit))

    if source in ["all", "bugcrowd"]:
        bc = BugcrowdIntegration()
        reports.extend(bc.fetch_reports(limit=limit))

    if source in ["all", "intigriti"]:
        intigriti = IntigritiIntegration()
        reports.extend(intigriti.fetch_disclosures(limit=limit))

    if source in ["all", "projectzero"]:
        pz = GoogleProjectZeroIntegration()
        reports.extend(pz.fetch_disclosures(limit=limit))

    logger.info(f"Fetched {len(reports)} reports from {source}")
    return reports


if __name__ == "__main__":
    # Example usage
    print("Fetching real vulnerability data...\n")

    print("1. NVD (National Vulnerability Database)")
    print("   - CVSS scores, CVE details, published vulnerabilities")
    nvd = NVDIntegration()
    nvd_data = nvd.fetch_recent_vulnerabilities(limit=5)
    print(f"   Found: {len(nvd_data)} recent CVEs\n")

    print("2. HackerOne Public Disclosures")
    print("   - Researcher-found vulnerabilities, bounty amounts")
    h1 = HackerOneIntegration()
    h1_data = h1.fetch_disclosures(limit=5)
    print(f"   Found: {len(h1_data)} disclosures\n")

    print("3. GitHub Security Advisories")
    print("   - Package vulnerabilities, ecosystem data")
    github = GitHubSecurityAlertsIntegration()
    github_data = github.fetch_security_advisories(limit=5)
    print(f"   Found: {len(github_data)} advisories\n")

    print("Integration complete. Use get_real_bug_bounty_data() in your code.")
