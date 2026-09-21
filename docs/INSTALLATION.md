# VAPT Automation Engine - Installation Guide

## System Requirements

### Minimum Requirements
- Python 3.8+
- 4GB RAM
- 20GB disk space (for scanning data)
- Linux (Kali Linux recommended) or Windows (WSL2)

### Recommended Requirements
- Python 3.10+
- 8GB+ RAM
- 50GB+ disk space
- Kali Linux 2024+

## Installation Steps

### 1. Prerequisites Installation

#### On Kali Linux
```bash
sudo apt-get update
sudo apt-get install -y \
    python3.11 python3-pip python3-venv \
    nmap masscan \
    git curl \
    libssl-dev libffi-dev \
    build-essential
```

#### On Windows (WSL2)
```bash
# In PowerShell (Admin)
wsl --install Ubuntu-24.04

# In WSL
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip python3-venv nmap git
```

### 2. Clone Repository

```bash
git clone https://github.com/alvinnnnn/vapt-automation-engine.git
cd vapt-automation-engine
```

### 3. Create Virtual Environment

```bash
# Linux/Mac/WSL
python3.11 -m venv venv
source venv/bin/activate

# Windows (CMD)
python -m venv venv
venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 5. Install VAPT Package

```bash
pip install -e .
```

### 6. Tool Configuration

#### Burp Suite Professional Setup

1. Install Burp Suite Professional
2. Configure API access:
   ```bash
   # Create config file: config/burp_config.json
   {
       "api_url": "http://localhost:1337",
       "api_key": "YOUR_API_KEY_HERE",
       "timeout": 3600
   }
   ```

3. Enable REST API in Burp:
   - User Options → Misc → REST API → Enable REST API

#### Metasploit Framework

```bash
# Install Metasploit
sudo apt-get install -y metasploit-framework

# Verify installation
msfconsole --version
```

#### Nmap Scripts

```bash
# NSE scripts are included with Nmap
# Verify installation
nmap --script-help vuln
```

## Verification

Test installation:

```bash
# Check Python version
python3 --version

# Check VAPT installation
vapt --help

# Test Nmap
nmap --version

# Verify virtual environment
which python
```

## Docker Installation (Optional)

For containerized deployment:

```bash
# Build Docker image
docker build -t vapt-automation-engine .

# Run container
docker run -it -v /path/to/assessments:/assessments vapt-automation-engine bash

# Inside container
vapt init --client "Acme Corp"
```

## Troubleshooting

### Issue: "nmap: command not found"
```bash
sudo apt-get install -y nmap
# or
brew install nmap  # macOS
```

### Issue: "Python 3.8+ required"
```bash
# Upgrade Python
sudo apt-get install -y python3.11
python3.11 -m venv venv
```

### Issue: "Burp API Connection Failed"
- Verify Burp Suite is running
- Check API URL: default is `http://localhost:1337`
- Enable REST API in Burp: User Options → Misc → REST API
- Check firewall rules

### Issue: "Permission Denied" on Linux
```bash
# Add user to sudoers for Nmap (if needed)
sudo usermod -aG sudo $USER

# Or use with sudo
sudo vapt network-scan --targets targets.txt
```

## Post-Installation

1. **Create assessment workspace:**
   ```bash
   mkdir -p ~/vapt-assessments
   cd ~/vapt-assessments
   ```

2. **Verify all tools:**
   ```bash
   vapt --help
   nmap --version
   msfconsole --version
   ```

3. **Configure credentials (if needed):**
   ```bash
   # Create secure credentials file
   cp config/template.env .env
   # Edit .env with your API keys
   ```

## Next Steps

- Read [USAGE_GUIDE.md](USAGE_GUIDE.md) for operational instructions
- Review [FRAMEWORKS.md](FRAMEWORKS.md) for compliance details
- Check [examples/](../examples/) for sample assessments
