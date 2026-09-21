# Quick Start Guide

Get started with VAPT Automation Engine in 5 minutes!

## 1. Installation (2 minutes)

### Linux/macOS
```bash
git clone https://github.com/yourusername/vapt-automation-engine.git
cd vapt-automation-engine
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./scripts/install_dependencies.sh
```

### Windows
```powershell
git clone https://github.com/yourusername/vapt-automation-engine.git
cd vapt-automation-engine
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\scripts\install_dependencies.ps1
```

## 2. Configuration (1 minute)

```bash
cp .env.example .env
# Edit .env with your tool credentials
```

## 3. Run Your First Scan (2 minutes)

### Via CLI
```bash
# Quick scan on a target
python -m src.cli scan \
  --target 192.168.1.1 \
  --profile quick_scan \
  --format html

# View results
open reports/scan_*.html
```

### Via Python
```python
from src.core.engine import VAPTEngine
from src.config import get_config

config = get_config()
engine = VAPTEngine(config)

# Execute scan
result = engine.execute_scan({
    "targets": ["192.168.1.1"],
    "profile": "quick_scan"
})

# Generate report
engine.generate_report(result['scan_id'], format='html')
```

### Via REST API
```bash
# Start API server
python -m src.api.app

# Create scan
curl -X POST http://localhost:8000/api/v1/scans \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quick Scan",
    "targets": ["192.168.1.1"],
    "profile": "quick_scan"
  }'

# View results
curl http://localhost:8000/api/v1/scans/{scan_id}
```

## 4. View Results

### HTML Report
```bash
# Automatic browser open
open reports/quick_scan_*.html

# Or use any browser
firefox reports/quick_scan_*.html
```

### JSON Output
```bash
cat reports/quick_scan_*.json | jq .
```

### Compliance Mapping
```bash
# View OWASP Top 10 findings
curl http://localhost:8000/api/v1/scans/{id}/compliance/owasp-top10
```

## Available Scan Profiles

### Quick Scan (15-30 minutes)
```bash
python -m src.cli scan --target <target> --profile quick_scan
```

### Standard Scan (1-2 hours)
```bash
python -m src.cli scan --target <target> --profile standard_scan
```

### Comprehensive Scan (4+ hours)
```bash
python -m src.cli scan --target <target> --profile comprehensive_scan
```

### Compliance Scan
```bash
python -m src.cli scan --target <target> --profile compliance_scan
```

## Common Commands

### List Available Tools
```bash
python -m src.cli tool list
```

### Check Tool Status
```bash
python -m src.cli tool status
```

### Generate Report from Scan
```bash
python -m src.cli report generate \
  --scan-id <scan_id> \
  --format pdf \
  --template executive
```

### View Scan History
```bash
python -m src.cli scan list
```

### Export Findings
```bash
python -m src.cli export \
  --scan-id <scan_id> \
  --format json \
  --output results.json
```

## Next Steps

1. **Read Full Documentation**: See [docs/](../README.md)
2. **Configure Tools**: Edit [config/tools/](../../config/tools/)
3. **Customize Scan Profiles**: Edit [config/profiles/](../../config/profiles/)
4. **Set Up Compliance Frameworks**: Edit [config/frameworks/](../../config/frameworks/)
5. **Explore API**: Visit http://localhost:8000/docs (Swagger UI)
6. **Run Tests**: `pytest tests/ -v`

## Troubleshooting

### Tools Not Found
```bash
./scripts/verify_tools.sh
```

### API Connection Error
```bash
# Check if API is running
curl http://localhost:8000/api/v1/health

# Start API if not running
python -m src.api.app --host 0.0.0.0 --port 8000
```

### Scan Failures
```bash
# Check logs
tail -f logs/vapt_*.log

# Run with debug logging
python -m src.cli scan --target <target> --debug
```

## Getting Help

- **Documentation**: https://github.com/yourusername/vapt-automation-engine/docs
- **Issues**: https://github.com/yourusername/vapt-automation-engine/issues
- **Examples**: See [examples/](../../examples/) directory
- **FAQ**: https://github.com/yourusername/vapt-automation-engine/docs/faq

## Tips

1. **Start with quick_scan** to test your setup
2. **Check API docs** at `/docs` for available endpoints
3. **Monitor logs** during first scans to verify tool integration
4. **Review sample reports** in examples/
5. **Join community** for updates and support

Enjoy automated penetration testing!
