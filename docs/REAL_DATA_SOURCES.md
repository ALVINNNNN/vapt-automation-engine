# Real Bug Bounty Data Sources

The VAPT engine currently uses **simulated example data** for demonstrations. Here's how to integrate with **real public vulnerability databases** instead.

---

## Available Real Data Sources

### 1. **National Vulnerability Database (NVD)** ⭐ Recommended
**Best for:** Real, structured vulnerability data with CVSS scores

```python
from vapt.bug_bounty.real_data_integrations import NVDIntegration

# Fetch real CVEs
nvd = NVDIntegration(api_key="your-nvd-api-key")
reports = nvd.fetch_recent_vulnerabilities(limit=50)

# Use in pattern learner
learner.train_from_reports(reports)
```

**Features:**
- ✅ Free public API (register at https://nvd.nist.gov)
- ✅ Real CVE data with CVSS scores
- ✅ Structured JSON format
- ✅ 20+ years of vulnerability history
- ✅ No authentication required for basic access

**Pros:** Most reliable, government-backed, comprehensive  
**Cons:** Generic CVEs, not bounty-specific

---

### 2. **HackerOne Public Disclosures**
**Best for:** Real bug bounty findings with bounty amounts

```python
from vapt.bug_bounty.real_data_integrations import HackerOneIntegration

# Fetch HackerOne disclosures
h1 = HackerOneIntegration()
reports = h1.fetch_disclosures(limit=50)
```

**Features:**
- ✅ Real bug bounty reports
- ✅ Bounty amounts included
- ✅ Researcher-found vulnerabilities
- ✅ Public RSS feed available
- ✅ Historical data available

**API Options:**
1. **Public RSS Feed** (free, no auth needed)
   - URL: `https://hackerone.com/hacktivity.json`
   - Updated: Real-time
   - Rate limit: Reasonable

2. **HackerOne API** (requires program membership)
   - Comprehensive data
   - Higher rate limits
   - Full access to program details

**Pros:** Real bounty data, researcher insights  
**Cons:** Limited to disclosed reports only

---

### 3. **GitHub Security Advisories**
**Best for:** Software package vulnerabilities

```python
from vapt.bug_bounty.real_data_integrations import GitHubSecurityAlertsIntegration

# Fetch GitHub advisories
github = GitHubSecurityAlertsIntegration(github_token="your-github-token")
reports = github.fetch_security_advisories(limit=50)
```

**Features:**
- ✅ Package vulnerability data
- ✅ Multiple ecosystems (npm, PyPI, RubyGems, Maven, etc.)
- ✅ Severity ratings
- ✅ Free with GitHub account

**Supported Ecosystems:**
- JavaScript/npm
- Python (PyPI)
- Ruby (RubyGems)
- Java (Maven)
- .NET (NuGet)
- Go
- Rust
- PHP (Composer)

**Pros:** Practical, ecosystem-specific, well-maintained  
**Cons:** Package-focused, not general web app vulnerabilities

---

### 4. **Bugcrowd Public Data**
**Best for:** Industry statistics and vulnerability trends

```python
from vapt.bug_bounty.real_data_integrations import BugcrowdIntegration

bc = BugcrowdIntegration()
reports = bc.fetch_reports(limit=50)
```

**Features:**
- ✅ Annual vulnerability reports
- ✅ Industry trends
- ✅ Average bounty data
- ✅ Public research pages

**Pros:** Statistical insights, trend analysis  
**Cons:** Limited real vulnerability details

---

### 5. **Google Project Zero**
**Best for:** High-impact, well-researched vulnerabilities

```python
from vapt.bug_bounty.real_data_integrations import GoogleProjectZeroIntegration

pz = GoogleProjectZeroIntegration()
reports = pz.fetch_disclosures(limit=50)
```

**Features:**
- ✅ High-quality research
- ✅ Detailed technical analysis
- ✅ Responsible disclosure timeline
- ✅ Published CVEs

**Pros:** Quality over quantity, deep technical insights  
**Cons:** Fewer reports, focused on critical issues

---

### 6. **Intigriti Disclosures**
**Best for:** European vulnerability data

```python
from vapt.bug_bounty.real_data_integrations import IntigritiIntegration

intigriti = IntigritiIntegration()
reports = intigriti.fetch_disclosures(limit=50)
```

**Features:**
- ✅ Public disclosures
- ✅ European researcher focus
- ✅ Structured data

---

## How to Use Real Data

### Option 1: Use NVD (Easiest, Free)

**Step 1: Get Free API Key**
```bash
# Visit https://nvd.nist.gov/developers/request-an-api-key
# Takes 2 minutes, get instant approval
```

**Step 2: Update Your Code**
```python
from vapt.bug_bounty.real_data_integrations import NVDIntegration
from vapt.bug_bounty.vulnerability_pattern_learner import VulnerabilityPatternLearner

# Fetch real CVE data
nvd = NVDIntegration(api_key="your-api-key")
reports = nvd.fetch_recent_vulnerabilities(limit=100)

# Train on real data
learner = VulnerabilityPatternLearner()
learner.train_from_reports(reports)
```

**Step 3: Hunt with Real Patterns**
```bash
vapt bug-bounty hunt --client "MyClient" --target "https://target.com"
# Now uses patterns learned from real CVEs!
```

---

### Option 2: Use Multiple Sources

```python
from vapt.bug_bounty.real_data_integrations import get_real_bug_bounty_data

# Fetch from all available sources
all_data = get_real_bug_bounty_data(source="all", limit=100)

# Or specific source
nvd_data = get_real_bug_bounty_data(source="nvd", limit=50)
h1_data = get_real_bug_bounty_data(source="hackerone", limit=50)
github_data = get_real_bug_bounty_data(source="github", limit=50)

# Train on combined real data
learner.train_from_reports(all_data)
```

---

### Option 3: Replace YesWeHack Completely

Update `yeswehack_integration.py` to use real data:

```python
# In yeswehack_integration.py

from .real_data_integrations import (
    NVDIntegration,
    HackerOneIntegration,
    GitHubSecurityAlertsIntegration
)

class YesWeHackIntegration:
    def fetch_recent_reports(self, limit: int = 50):
        """Fetch real reports from NVD + HackerOne"""
        reports = []
        
        # Get NVD data
        nvd = NVDIntegration(api_key=os.getenv("NVD_API_KEY"))
        reports.extend(nvd.fetch_recent_vulnerabilities(limit=limit//2))
        
        # Get HackerOne data
        h1 = HackerOneIntegration()
        reports.extend(h1.fetch_disclosures(limit=limit//2))
        
        return reports
```

---

## Recommended Setup

### For Development/Testing
```bash
# Use simulated data (current setup)
# Instant, no dependencies
vapt bug-bounty train
```

### For Production/Real Assessments
```bash
# Setup
export NVD_API_KEY="your-nvd-api-key"
export GITHUB_TOKEN="your-github-token"

# Train on real data
# Trains once, caches locally
python -m vapt.bug_bounty.bug_bounty_cli train --source nvd

# Hunt using real patterns
vapt bug-bounty hunt --client "Client" --target "https://target.com"
```

---

## Data Source Comparison

| Source | Type | Quality | Real Bounty | Free | Auth Required |
|--------|------|---------|-------------|------|---|
| **NVD** | CVE Database | High | No | Yes | Optional API Key |
| **HackerOne** | Bug Bounty | High | **Yes** | Yes | No |
| **GitHub** | Packages | High | No | Yes | GitHub Account |
| **Bugcrowd** | Statistics | Medium | **Yes** | Yes | No |
| **Project Zero** | Research | Very High | No | Yes | No |
| **Intigriti** | Bug Bounty | High | **Yes** | Yes | No |

---

## Setup Instructions

### 1. NVD (Recommended - Free)

```bash
# Step 1: Get API Key
# Visit: https://nvd.nist.gov/developers/request-an-api-key
# Instant approval, free forever

# Step 2: Set environment variable
export NVD_API_KEY="your-api-key"

# Step 3: Test
python -c "from vapt.bug_bounty.real_data_integrations import NVDIntegration; \
NVDIntegration(api_key='$NVD_API_KEY').fetch_recent_vulnerabilities(limit=5)"
```

### 2. GitHub (Free with GitHub Account)

```bash
# Step 1: Create GitHub Personal Access Token
# Visit: https://github.com/settings/tokens
# Select scopes: read:public_repo, read:security_events
# Copy the token

# Step 2: Set environment variable
export GITHUB_TOKEN="your-github-token"

# Step 3: Test
python -c "from vapt.bug_bounty.real_data_integrations import GitHubSecurityAlertsIntegration; \
GitHubSecurityAlertsIntegration(github_token='$GITHUB_TOKEN').fetch_security_advisories(limit=5)"
```

### 3. HackerOne (Free, No Auth)

```bash
# No setup needed! Works out of the box
python -c "from vapt.bug_bounty.real_data_integrations import HackerOneIntegration; \
HackerOneIntegration().fetch_disclosures(limit=5)"
```

---

## Currently: Simulated Data

The engine ships with **10 realistic example reports** to demonstrate functionality:

```python
# Current simulated reports in yeswehack_integration.py:
1. IDOR - /api/users/{id}
2. JWT Auth Bypass
3. SQL Injection
4. Privilege Escalation
5. AWS S3 Exposure
6. CORS Misconfiguration
7. API Rate Limiting Bypass
8. Reflected XSS
9. Information Disclosure
10. Sensitive Data Exposure
```

These are **realistic examples based on real bug bounty trends**, but not actual reports.

---

## Next Steps

1. **Choose a data source** (NVD recommended for free access)
2. **Get API key** if needed (takes 2 minutes)
3. **Update training**:
   ```bash
   export NVD_API_KEY="your-key"
   python -m vapt.bug_bounty.bug_bounty_cli train --source nvd
   ```
4. **Hunt on real patterns** - all subsequent hunts use real vulnerability data

---

## Disclaimer

- Only use this system on targets you have authorization to test
- Respect responsible disclosure timelines
- Follow each platform's terms of service
- NVD data may lag behind active exploits by days/weeks
- Combine multiple sources for comprehensive coverage

---

## Adding More Sources

To add another data source:

```python
# In real_data_integrations.py

class MyBugBountyIntegration:
    def fetch_reports(self, limit: int = 50):
        """Fetch from your data source"""
        reports = []
        # Fetch logic here
        return reports

# Export from get_real_bug_bounty_data()
if source in ["all", "mybugbounty"]:
    my_platform = MyBugBountyIntegration()
    reports.extend(my_platform.fetch_reports(limit=limit))
```

---

## Questions?

- **NVD API Issues?** Check: https://nvd.nist.gov/developers
- **GitHub Token Issues?** Check: https://github.com/settings/tokens
- **HackerOne Data?** Visit: https://hackerone.com/hacktivity
- **Rate Limiting?** Most public APIs have generous free limits

Start with **NVD** - it's the most reliable, free, and requires zero authentication!
