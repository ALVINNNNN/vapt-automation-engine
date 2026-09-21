# Contributing to VAPT Automation Engine

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and professional
- Report security vulnerabilities privately
- Help others understand your contributions
- Focus on making penetration testing better and safer

## Getting Started

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/alvinnnnn/vapt-automation-engine.git
cd vapt-automation-engine

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### 2. Understanding the Architecture

- Read `docs/ARCHITECTURE.md` for system design
- Review `docs/FRAMEWORKS.md` for compliance details
- Examine existing scanners in `vapt/scanners/`

### 3. Development Workflow

```bash
# Create feature branch
git checkout -b feature/new-scanner

# Make changes
# Test thoroughly
pytest tests/

# Commit with clear messages
git commit -m "Add new scanner for tool XYZ"

# Push and create pull request
git push origin feature/new-scanner
```

## Contributing Scanner Implementations

### 1. Create New Scanner

```python
# vapt/scanners/my_scanner.py
from vapt.core.scanner import BaseScanner, ScannerType, ScanResult

class MyScanner(BaseScanner):
    """Scanner description"""
    
    def __init__(self):
        super().__init__("my_scanner", ScannerType.NETWORK)
    
    def configure(self, config):
        self.config = config
        self.is_configured = True
    
    def validate_configuration(self):
        return self.is_configured
    
    def execute(self, targets):
        # Implementation
        pass
    
    def parse_results(self, raw_output):
        # Parsing logic
        return []
```

### 2. Write Tests

```python
# tests/test_my_scanner.py
import pytest
from vapt.scanners.my_scanner import MyScanner

def test_scanner_initialization():
    scanner = MyScanner()
    assert scanner.name == "my_scanner"
    assert not scanner.is_configured

def test_scanner_configuration():
    scanner = MyScanner()
    scanner.configure({"option": "value"})
    assert scanner.validate_configuration()

def test_scanner_execution():
    scanner = MyScanner()
    scanner.configure({})
    result = scanner.execute(["target.com"])
    assert result.scanner_name == "my_scanner"
```

### 3. Document Scanner

- Add description to `README.md`
- Create usage example
- Document configuration options
- Provide sample output

## Contributing Report Generators

### 1. Create Reporter

```python
# vapt/reporters/my_reporter.py
from vapt.core.reporter import BaseReporter, ReportFormat

class MyReporter(BaseReporter):
    def __init__(self):
        super().__init__(ReportFormat.CUSTOM)
    
    def generate(self, assessment_data, findings, output_path):
        # Generate report
        pass
    
    def validate_data(self, assessment_data):
        return True
```

### 2. Register Reporter

```python
# In vapt/cli.py
reporter.register_reporter(ReportFormat.CUSTOM, MyReporter())
```

## Contributing Compliance Mappings

### 1. Add Framework Support

```python
# vapt/compliance/my_framework.py
class MyFrameworkMapper:
    def __init__(self):
        self.mappings = {
            "vulnerability_type": ["Framework-Requirement-ID"],
        }
    
    def map_finding(self, finding):
        # Mapping logic
        pass
```

### 2. Integrate into Mapper

```python
# vapt/compliance/framework_mapper.py
from vapt.compliance.my_framework import MyFrameworkMapper

self.my_framework_mappings = self._init_my_framework_mappings()
```

## Code Quality

### Python Standards

```bash
# Format code
black vapt/

# Check style
flake8 vapt/

# Run linter
pylint vapt/

# Type checking
mypy vapt/
```

### Pre-commit Checks

```bash
# Pre-commit runs automatically on commit
# Or manually:
pre-commit run --all-files
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vapt tests/

# Run specific test
pytest tests/test_scanner.py::test_initialization
```

## Documentation

### Code Documentation

```python
def function_name(param: str) -> bool:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
        
    Raises:
        ValueError: When this condition occurs
    """
    pass
```

### Update Docs

- Keep `README.md` current
- Update `docs/` with new features
- Add examples for new functionality
- Document breaking changes

## Commit Guidelines

### Message Format

```
Type: Brief description (50 chars)

Longer explanation if needed (72 char wrap).

- Bullet points for details
- Reference issues: Fixes #123

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
Claude-Session: <session-link>
```

### Types

- **feat**: New feature or scanner
- **fix**: Bug fix
- **docs**: Documentation update
- **test**: Test additions/updates
- **refactor**: Code reorganization
- **perf**: Performance improvement
- **chore**: Build, dependencies, etc.

## Pull Request Process

### Before Submitting

1. Update code to latest `main` branch
2. Run all tests and linters
3. Update documentation
4. Add changelog entry
5. Verify no credentials in code

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No security issues
- [ ] No credentials exposed
```

## Security Considerations

### Sensitive Data

- Never commit API keys or credentials
- Use environment variables for secrets
- Add sensitive files to `.gitignore`
- Clean commit history if needed

### Code Security

- Validate all inputs
- Use secure defaults
- Handle exceptions properly
- Keep dependencies updated
- Run security checks

## Reporting Issues

### Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error logs/screenshots

### Security Issues

**Do not** create public issues for security vulnerabilities.

Email: alvinseahsq@gmail.com

Include:
- Vulnerability description
- Impact assessment
- Recommended fix
- Timeline for disclosure

## License

By contributing, you agree that your contributions are licensed under the project's license.

## Questions?

- Check existing documentation
- Review similar implementations
- Ask in pull request discussions
- Email: alvinseahsq@gmail.com

---

Thank you for making VAPT Automation Engine better!
