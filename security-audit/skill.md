---
name: security-audit
description: >-
  Use when the user says "@security-audit", "@security", "security audit", "credential scan", 
  "secret detection", "check for credentials", "find secrets", "security check", 
  "pre-commit security", "git security scan", or any request to scan for credentials, 
  secrets, tokens, API keys, or sensitive information in code before Git operations.
---

# Security Audit Skill

## Overview

This skill provides comprehensive security scanning capabilities for detecting credentials, secrets, tokens, API keys, and sensitive information in code repositories before Git operations. Use this skill to perform pre-commit security audits, credential scanning, and secret detection.

## Key Capabilities

- **Credential Scanning**: Detect hardcoded credentials, passwords, usernames
- **Secret Detection**: Identify API keys, tokens, authentication secrets
- **Pattern Matching**: Recognize common sensitive data patterns
- **Variable Suggestion**: Recommend secure variable replacements
- **Pre-commit Integration**: Support for Git pre-commit hooks
- **Security Reporting**: Generate comprehensive security audit reports

## Common Use Cases

### Pre-commit Security Check
**Use when**: About to commit code to Git repository

**Steps**:
1. Load `references/patterns.md` for detection patterns
2. Scan staged files for sensitive information
3. Generate security findings report
4. Provide remediation recommendations
5. Block commit if critical issues found (optional)

### Credential Scan
**Use when**: Need to find hardcoded credentials in codebase

**Steps**:
1. Scan all files in project directory
2. Match against credential patterns
3. Identify severity levels (critical, high, medium, low)
4. Provide file locations and line numbers
5. Suggest secure alternatives

### Secret Detection
**Use when**: Checking for API keys, tokens, or secrets

**Steps**:
1. Load secret detection patterns
2. Scan for common secret formats (AWS keys, GitHub tokens, etc.)
3. Validate potential secrets against known formats
4. Report findings with confidence levels
5. Recommend secure storage solutions

## Detection Patterns

### Credential Patterns

**User/Password Combinations**:
- `username.*password`
- `user.*passwd`
- `login.*pass`
- `auth.*credential`

**Default Credentials**:
- `root.*calvin` (Dell iDRAC)
- `admin.*admin`
- `admin.*password`
- `user.*user`

**Hardcoded Values**:
- `password.*=.*["'].*["']`
- `secret.*=.*["'].*["']`
- `token.*=.*["'].*["']`
- `api_key.*=.*["'].*["']`

### Secret Patterns

**API Keys**:
- `AKIA[0-9A-Z]{16}` (AWS Access Key)
- `sk-[a-zA-Z0-9]{32}` (Stripe API Key)
- `ghp_[a-zA-Z0-9]{36}` (GitHub Personal Access Token)
- `xox[bp]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}` (Slack Token)

**Database Credentials**:
- `mongodb://.*:.*@`
- `postgres://.*:.*@`
- `mysql://.*:.*@`

**Cloud Provider Secrets**:
- `google.*credential`
- `azure.*key`
- `aws.*secret`

## Security Levels

### Critical
- Hardcoded production credentials
- Valid API keys or tokens
- Database connection strings with credentials

### High
- Default credentials
- Hardcoded passwords in examples
- API key placeholders that look real

### Medium
- Suspicious patterns
- Credential-like strings
- Configuration files with secrets

### Low
- Placeholder credentials
- Example code with obvious placeholders
- Documentation with example credentials

## Workflow Examples

### Example 1: Pre-commit Security Scan
```python
from security_audit import SecurityScanner

# Initialize scanner
scanner = SecurityScanner(project_path="/path/to/project")

# Scan staged files
findings = scanner.scan_staged_files()

# Generate report
report = scanner.generate_report(findings)

# Check if safe to commit
if report.critical_count > 0:
    print("❌ Critical security issues found - commit blocked")
    print(report.summary)
else:
    print("✅ Safe to commit")
```

### Example 2: Full Repository Scan
```python
from security_audit import SecurityScanner

# Initialize scanner with custom patterns
scanner = SecurityScanner(
    project_path="/path/to/project",
    custom_patterns=["CUSTOM_API_KEY_PATTERN"]
)

# Scan all files
findings = scanner.scan_all_files()

# Filter by severity
critical_findings = [f for f in findings if f.severity == "critical"]

# Generate remediation suggestions
for finding in critical_findings:
    print(f"File: {finding.file}")
    print(f"Line: {finding.line}")
    print(f"Issue: {finding.issue}")
    print(f"Suggestion: {finding.suggestion}")
    print("---")
```

### Example 3: Git Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔒 Running security audit..."

# Run security scanner
python3 -m security_audit.scan --pre-commit

# Check exit code
if [ $? -ne 0 ]; then
    echo "❌ Security issues found - commit blocked"
    echo "Run 'security-audit scan --fix' to see remediation suggestions"
    exit 1
fi

echo "✅ Security check passed"
exit 0
```

## Remediation Strategies

### Variable Replacement
**Before**:
```python
password = "hardcoded_password"
```

**After**:
```python
import os
password = os.getenv("DB_PASSWORD")
```

### Configuration Files
**Before**:
```yaml
database:
  password: "secret123"
```

**After**:
```yaml
database:
  password: ${DB_PASSWORD}
```

### Secret Management
**Before**:
```python
api_key = "sk-1234567890abcdef"
```

**After**:
```python
from secret_manager import get_secret
api_key = get_secret("API_KEY")
```

## Integration with Git

### Pre-commit Hook
```bash
# Install pre-commit hook
security-audit install-hook

# Or manually:
cp .security-audit/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Pre-push Hook
```bash
# Install pre-push hook
security-audit install-hook --pre-push
```

### CI/CD Integration
```yaml
# Example GitHub Actions
- name: Security Audit
  run: |
    python -m security_audit.scan --ci-mode
    security-audit report --format sarif --output security-results.sarif
```

## Configuration

### Security Audit Configuration
Create `.security-audit.yaml` in project root:

```yaml
# Security Audit Configuration
scan:
  exclude_patterns:
    - "*.log"
    - "node_modules/"
    - ".git/"
    - "venv/"
  
  severity_threshold: "high"  # Block commits at this level
  
  custom_patterns:
    - name: "Custom API Key"
      pattern: "CUSTOM_KEY_[A-Z0-9]{32}"
      severity: "critical"
  
  file_types:
    - "*.py"
    - "*.js"
    - "*.yaml"
    - "*.yml"
    - "*.json"
    - "*.md"
  
  ignore_files:
    - "examples/*"
    - "tests/*"
```

## Reference Materials

Detailed reference material in `references/` directory:

| File | Content |
|---|---|
| `references/patterns.md` | Complete detection patterns and regex |
| `references/remediation.md` | Remediation strategies and best practices |
| `references/git-integration.md` | Git hook integration guide |
| `references/ci-cd.md` | CI/CD pipeline integration |

## Example Files

Practical examples in `scripts/` directory:

| File | Content |
|---|---|
| `scripts/security_scanner.py` | Main security scanning script |
| `scripts/pattern_matcher.py` | Pattern matching engine |
| `scripts/remediation_helper.py` | Remediation suggestion generator |
| `scripts/git_hooks.py` | Git hook installation script |

## Security Best Practices

1. **Never commit credentials** - Always use environment variables or secret management
2. **Use secret scanning** - Run security audit before every commit
3. **Implement pre-commit hooks** - Automate security checks
4. **Regular audits** - Schedule periodic security scans
5. **Educate team** - Train developers on security best practices
6. **Monitor for leaks** - Set up secret scanning in CI/CD pipelines

## Troubleshooting

### False Positives
- Add patterns to exclude list in configuration
- Use placeholder format that doesn't trigger patterns
- Mark specific files as safe in configuration

### Performance Issues
- Exclude large directories from scanning
- Use incremental scanning for large projects
- Cache scan results for unchanged files

### Integration Issues
- Ensure Python dependencies are installed
- Check Git hook permissions
- Verify configuration file syntax

## Getting Help

For specific security audit questions:
1. Load appropriate reference file from `references/`
2. Check example scripts in `scripts/`
3. Review configuration options in `.security-audit.yaml`
4. Enable debug mode for detailed logging

## Quick Start

### Basic Scan
```bash
security-audit scan
```

### Scan with Report
```bash
security-audit scan --report security-report.html
```

### Pre-commit Mode
```bash
security-audit scan --pre-commit
```

### Install Git Hooks
```bash
security-audit install-hook
```

## Advanced Features

### Custom Pattern Addition
```python
from security_audit import SecurityScanner

scanner = SecurityScanner()
scanner.add_pattern(
    name="Custom Secret",
    pattern=r"CUSTOM_SECRET_[A-Z0-9]{40}",
    severity="critical"
)
findings = scanner.scan()
```

### Baseline Comparison
```bash
# Compare against baseline
security-audit scan --baseline baseline.json
```

### SARIF Output
```bash
# Generate SARIF format for CI/CD tools
security-audit scan --format sarif --output results.sarif
```

## Integration with Other Skills

This skill can be used alongside:
- **session-memory**: Store security audit results across sessions
- **blueprint**: Security audit for blueprint development
- **git-ssh**: Secure Git operations with security checks