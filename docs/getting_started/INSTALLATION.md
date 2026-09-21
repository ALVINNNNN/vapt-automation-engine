# Installation Guide

## Prerequisites

### System Requirements

#### Linux (Recommended)
- **OS**: Ubuntu 20.04+, Debian 10+, CentOS 8+, Kali Linux 2021+
- **RAM**: Minimum 4GB (8GB+ recommended)
- **CPU**: 2 cores minimum (4+ cores recommended)
- **Disk Space**: 20GB+ for tools and results
- **Python**: 3.10 or higher

#### Windows
- **OS**: Windows 10/11, Windows Server 2019+
- **RAM**: Minimum 4GB (8GB+ recommended)
- **CPU**: 2 cores minimum (4+ cores recommended)
- **Disk Space**: 20GB+ for tools and results
- **Python**: 3.10 or higher
- **PowerShell**: 5.0+ or PowerShell Core

#### macOS
- **OS**: macOS 11+
- **RAM**: Minimum 4GB (8GB+ recommended)
- **CPU**: 2 cores minimum
- **Disk Space**: 20GB+
- **Python**: 3.10 or higher
- **Homebrew**: Recommended for package management

### Required Tools

#### Network Testing (nVAPT)
- **Nmap**: `nmap >= 7.92`
- **Metasploit Framework**: Latest version (optional)
- **OpenVAS**: (optional)

#### Application Testing (AVAPT)
- **Burp Suite Professional**: Latest version with API enabled
- **OWASP ZAP**: 2.11+ (optional)
- **sslyze**: Installed via pip

#### General Requirements
- **Git**: For cloning the repository
- **pip**: Python package manager
- **curl** or **wget**: For downloading dependencies

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/vapt-automation-engine.git
cd vapt-automation-engine
```

### 2. Create Virtual Environment (Recommended)

#### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Security Tools

#### Linux (Ubuntu/Debian)
```bash
# Run automated installer
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

#### Linux (Kali Linux - Tools Pre-installed)
```bash
# Most tools come pre-installed, just verify
./scripts/verify_tools.sh
```

#### Windows (PowerShell)
```powershell
# Run automated installer
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\install_dependencies.ps1
```

#### Manual Tool Installation

**Nmap:**
```bash
# Linux
sudo apt-get install nmap  # Ubuntu/Debian
sudo yum install nmap      # CentOS/RHEL

# Windows
# Download from https://nmap.org/download.html

# macOS
brew install nmap
```

**Burp Suite Professional:**
- Download from https://portswigger.net/burp/communitydownload
- Install according to platform guidelines
- Obtain and configure API key

**OWASP ZAP:**
```bash
# Linux
sudo apt-get install zaproxy

# macOS
brew install zaproxy

# Windows
# Download from https://www.zaproxy.org/download/
```

**sslyze:**
```bash
pip install sslyze
```

### 5. Configure Environment

#### Create Environment File
```bash
cp .env.example .env
```

#### Edit .env File
```bash
# Database Configuration
DATABASE_URL=sqlite:///./vapt.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Tool API Keys (get these from tool settings)
BURP_API_KEY=your_burp_api_key
METASPLOIT_USER=your_metasploit_user
METASPLOIT_PASS=your_metasploit_password
ZAP_API_KEY=your_zap_api_key

# Security
SECRET_KEY=your_secret_key_here
```

### 6. Initialize Database

```bash
python -m scripts.migrate_database
```

### 7. Verify Installation

```bash
# Run verification script
./scripts/verify_tools.sh

# Run test suite
pytest tests/ -v

# Generate sample report
python examples/basic_usage/quick_scan.py
```

## Docker Installation

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+

### Quick Start
```bash
# Build Docker image
docker-compose build

# Start services
docker-compose up -d

# Verify
docker-compose logs -f vapt-engine

# Access API
curl http://localhost:8000/api/v1/health
```

### Docker Compose Configuration
See `docker/docker-compose.yml` for complete configuration.

## Kubernetes Deployment

### Prerequisites
- Kubernetes 1.20+
- Helm 3.0+ (optional)

### Deploy to Kubernetes
```bash
# Create namespace
kubectl create namespace vapt

# Apply configurations
kubectl apply -f kubernetes/

# Check deployment
kubectl get pods -n vapt
kubectl logs -n vapt -l app=vapt-engine
```

## Troubleshooting

### Issue: Python Module Not Found
**Solution:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Issue: Tool Not Found in PATH
**Solution:**
```bash
# Verify tool installation
which nmap
which zaproxy

# Add to PATH if needed
export PATH=$PATH:/path/to/tool/bin
```

### Issue: Permission Denied on Linux
**Solution:**
```bash
chmod +x scripts/*.sh
sudo usermod -aG docker $USER  # For Docker
```

### Issue: Cannot Connect to Burp Suite
**Solution:**
1. Start Burp Suite
2. Enable API: Settings > Tools > Burp's REST API > Enable
3. Configure API port (default 1337)
4. Set API key: User Options > API Key
5. Update config with correct URL and key

### Issue: Database Lock Error
**Solution:**
```bash
# Delete existing database
rm vapt.db

# Recreate database
python -m scripts.migrate_database
```

## Post-Installation

### 1. Configure Scan Profiles
Edit scan profiles in `config/profiles/`:
- `quick_scan.yaml` - For quick assessments
- `comprehensive_scan.yaml` - For full audits

### 2. Configure Tool Integrations
Edit tool configurations in `config/tools/`:
- Set API credentials
- Configure timeouts and options
- Specify tool-specific settings

### 3. Configure Compliance Frameworks
Select frameworks in `config/frameworks/`:
- OWASP Top 10
- NIST Cybersecurity Framework
- PCI-DSS
- ISO 27001

### 4. Generate Sample Report
```bash
python examples/basic_usage/quick_scan.py
```

## Next Steps

- Read [Quick Start Guide](./QUICK_START.md)
- Review [Configuration Guide](./CONFIGURATION.md)
- Check [First Scan Walkthrough](./FIRST_SCAN.md)
- Explore [Examples](../examples/)

## Support

For issues or questions:
- Check [Troubleshooting Guide](../troubleshooting/)
- Review [FAQ](../faq/)
- Submit issue on GitHub
- Check documentation at https://docs.example.com

## Uninstallation

### Remove Python Environment
```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv
```

### Remove Docker
```bash
docker-compose down
docker rmi vapt-automation-engine:latest
```

### Remove Database
```bash
rm vapt.db
rm -rf logs/
rm -rf reports/
```
