# Security Audit Detection Patterns

## Overview

This reference contains all detection patterns used by the security audit skill to identify credentials, secrets, tokens, and sensitive information.

## Pattern Categories

### 1. Credential Patterns

#### Basic Authentication
```regex
password\s*=\s*["'][^"']{4,}["']
passwd\s*=\s*["'][^"']{4,}["']
secret\s*=\s*["'][^"']{4,}["']
```

#### Username/Password Pairs
```regex
username\s*=\s*["'][^"']+["'].*password\s*=\s*["'][^"']+["']
user\s*=\s*["'][^"']+["'].*pass\s*=\s*["'][^"']+["']
login\s*=\s*["'][^"']+["'].*password\s*=\s*["'][^"']+["']
```

#### Default Dell iDRAC Credentials
```regex
root.*calvin
admin.*admin
admin.*password
user.*user
```

#### Connection Strings with Credentials
```regex
mongodb://[^:]+:[^@]+@
postgres://[^:]+:[^@]+@
mysql://[^:]+:[^@]+@
redis://:[^@]+@
```

### 2. API Key Patterns

#### AWS Keys
```regex
AKIA[0-9A-Z]{16}                    # AWS Access Key ID
[A-Za-z0-9+/]{40}                   # AWS Secret Access Key
aws_access_key_id\s*=\s*["'][A-Z0-9]+["']
aws_secret_access_key\s*=\s*["'][A-Za-z0-9+/]+["']
```

#### GitHub Tokens
```regex
ghp_[a-zA-Z0-9]{36}                 # GitHub Personal Access Token
gho_[a-zA-Z0-9]{36}                 # GitHub OAuth Token
ghu_[a-zA-Z0-9]{36}                 # GitHub User Token
ghs_[a-zA-Z0-9]{36}                 # GitHub Server Token
ghr_[a-zA-Z0-9]{36}                 # GitHub Refresh Token
```

#### Stripe Keys
```regex
sk_test_[a-zA-Z0-9]{24}              # Stripe Test Key
sk_live_[a-zA-Z0-9]{24}              # Stripe Live Key
pk_test_[a-zA-Z0-9]{24}              # Stripe Test Publishable Key
pk_live_[a-zA-Z0-9]{24}              # Stripe Live Publishable Key
```

#### Slack Tokens
```regex
xoxb-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}  # Slack Bot Token
xoxp-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}  # Slack User Token
xoxa-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}           # Slack App Token
```

### 3. Secret Patterns

#### JWT Tokens
```regex
eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+
```

#### Base64 Encoded Secrets
```regex
["'][A-Za-z0-9+/]{32,}={0,2}["']
```

#### Private Keys
```regex
-----BEGIN [A-Z]+ PRIVATE KEY-----
-----BEGIN RSA PRIVATE KEY-----
-----BEGIN EC PRIVATE KEY-----
```

### 4. Database Patterns

#### Connection Strings
```regex
Server=.*;Database=.*;User Id=.*;Password=.*
Data Source=.*;User Id=.*;Password=.*
host=.*;user=.*;password=.*
```

#### MongoDB Connection
```regex
mongodb://[^:]+:[^@]+@[^:]+:[0-9]+
mongodb\+srv://[^:]+:[^@]+@
```

### 5. Cloud Provider Patterns

#### Google Cloud
```regex
google\.application\.credentials\s*=\s*["'][^"']+["']
GOOGLE_APPLICATION_CREDENTIALS\s*=\s*["'][^"']+["']
```

#### Azure
```regex
azure\.storage\.connection\.string\s*=\s*["'][^"']+["']
AZURE_STORAGE_CONNECTION_STRING\s*=\s*["'][^"']+["']
```

#### AWS
```regex
AWS_ACCESS_KEY_ID\s*=\s*["'][A-Z0-9]+["']
AWS_SECRET_ACCESS_KEY\s*=\s*["'][A-Za-z0-9+/]+["']
AWS_SESSION_TOKEN\s*=\s*["'][A-Za-z0-9+/]+["']
```

### 6. Token Patterns

#### Bearer Tokens
```regex
Bearer\s+[A-Za-z0-9\-._~+/]+=*
Authorization:\s*Bearer\s+[A-Za-z0-9\-._~+/]+=*
```

#### API Tokens
```regex
api[_-]?key\s*=\s*["'][A-Za-z0-9]{20,}["']
api[_-]?secret\s*=\s*["'][A-Za-z0-9]{20,}["']
api[_-]?token\s*=\s*["'][A-Za-z0-9]{20,}["']
```

#### OAuth Tokens
```regex
oauth[_-]?token\s*=\s*["'][A-Za-z0-9]{20,}["']
access[_-]?token\s*=\s*["'][A-Za-z0-9]{20,}["']
refresh[_-]?token\s*=\s*["'][A-Za-z0-9]{20,}["']
```

### 7. Configuration File Patterns

#### YAML/JSON Configuration
```regex
password:\s*["'][^"']{4,}["']
secret:\s*["'][^"']{4,}["']
token:\s*["'][^"']{4,}["']
api_key:\s*["'][A-Za-z0-9]{20,}["']
```

#### Environment Variables
```regex
export\s+[A-Z_]+_PASSWORD\s*=\s*["'][^"']+["']
export\s+[A-Z_]+_SECRET\s*=\s*["'][^"']+["']
export\s+[A-Z_]+_TOKEN\s*=\s*["'][^"']+["']
```

### 8. URL Patterns with Credentials

#### URLs with User/Pass
```regex
https?://[^:]+:[^@]+@
ftp://[^:]+:[^@]+@
sftp://[^:]+:[^@]+@
```

#### API URLs with Keys
```regex
https?://[^/]+\?api[_-]?key=[^&\s]+
https?://[^/]+\?token=[^&\s]+
https?://[^/]+\?secret=[^&\s]+
```

### 9. Certificate Patterns

#### Certificate Files
```regex
\.crt
\.pem
\.key
\.p12
\.pfx
\.der
\.cer
```

#### Certificate Content
```regex
-----BEGIN CERTIFICATE-----
-----BEGIN TRUSTED CERTIFICATE-----
-----BEGIN ENCRYPTED PRIVATE KEY-----
```

### 10. Sensitive File Patterns

#### Configuration Files
```regex
config\.yaml
config\.yml
config\.json
settings\.py
\.env
\.env\..*
credentials\.json
secrets\.json
```

#### Temporary Files
```regex
\.tmp
\.temp
\.bak
\.backup
*_secret.*
*_credential.*
```

## Severity Levels

### Critical (CRITICAL)
- Valid API keys or tokens
- Database connection strings with credentials
- Private keys or certificates
- Valid authentication credentials

### High (HIGH)
- Default credentials
- Hardcoded passwords
- API key patterns that look real
- Connection strings with placeholder but real-looking credentials

### Medium (MEDIUM)
- Suspicious patterns
- Credential-like strings
- Configuration files with secret fields
- Environment variable assignments with secrets

### Low (LOW)
- Placeholder credentials
- Example code with obvious placeholders
- Documentation with example credentials
- Test data with fake credentials

## File Type Specific Patterns

### Python Files (.py)
```regex
os\.environ\(["'][A-Z_]+["']\)  # Environment variable access
getenv\(["'][A-Z_]+["']\)       # Environment variable access
```

### JavaScript Files (.js, .ts)
```regex
process\.env\.[A-Z_]+           # Environment variable access
import\.meta\.env\.[A-Z_]+       # Environment variable access
```

### YAML Files (.yaml, .yml)
```regex
\$\{[A-Z_]+\}                     # Variable substitution
```

### Shell Scripts (.sh, .bash)
```regex
export\s+[A-Z_]+                  # Environment variable export
```

## Exclusion Patterns

### Safe Patterns
```regex
password\s*=\s*["']<[^>]+>["']     # Placeholder format
password\s*=\s*["']\{[^}]+\}["'] # Placeholder format
password\s*=\s*["'\$\{[^}]+\}["'] # Environment variable format
example.*password                  # Documentation examples
test.*password                     # Test data
demo.*password                    # Demo data
```

### Safe Comments
```regex
#.*password
#.*secret
#.*token
//.*password
//.*secret
//.*token
```

## Pattern Matching Rules

### Context-Aware Matching
- Check surrounding context for placeholders
- Verify if in comment or string literal
- Consider file type and purpose
- Evaluate variable names and usage

### False Positive Reduction
- Exclude test files and examples
- Check for placeholder indicators
- Verify pattern context
- Consider common naming conventions

### Confidence Levels
- **High**: Exact pattern match with valid format
- **Medium**: Pattern match with potential context
- **Low**: Pattern match with high false positive probability

## Custom Pattern Addition

Users can add custom patterns in `.security-audit.yaml`:

```yaml
custom_patterns:
  - name: "Custom API Key"
    pattern: "CUSTOM_KEY_[A-Z0-9]{32}"
    severity: "critical"
    description: "Custom API key format"
  - name: "Internal Token"
    pattern: "INTERNAL_TOKEN_[a-zA-Z0-9]{40}"
    severity: "high"
    description: "Internal authentication token"
```

## Performance Considerations

### Optimization Strategies
- Exclude large binary files
- Use incremental scanning for large projects
- Cache scan results for unchanged files
- Parallel scanning for multiple files

### Memory Management
- Stream file processing for large files
- Limit concurrent file scans
- Use efficient regex compilation
- Implement pattern caching

## Pattern Updates

### Regular Updates
- Add new patterns as vulnerabilities are discovered
- Update existing patterns for new formats
- Remove outdated or ineffective patterns
- Adjust severity levels based on threat intelligence

### Community Contributions
- Submit new patterns via pull requests
- Share false positive findings
- Suggest pattern improvements
- Document new threat vectors

## Testing Patterns

### Test Cases
- Valid credentials should trigger detection
- Placeholders should not trigger false positives
- Comments should be excluded
- Different file types should be handled correctly

### Validation
- Test against known security datasets
- Validate pattern accuracy
- Measure false positive rates
- Benchmark performance

## References

- OWASP Cheat Sheet Series
- GitGuardian Secrets Detection
- TruffleHog Patterns
- Gitleaks Configuration
- Secret Scanning Best Practices