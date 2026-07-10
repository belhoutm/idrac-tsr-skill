# Security Remediation Guide

## Overview

This guide provides comprehensive remediation strategies for security issues detected during security audits. Each issue type includes specific remediation steps and code examples.

## Remediation Strategies

### 1. Hardcoded Credentials

#### Issue: Hardcoded Password
**Before**:
```python
database_password = "hardcoded_password_123"
```

**Remediation**:
```python
import os
database_password = os.getenv("DATABASE_PASSWORD")

# Or use secret management
from secret_manager import get_secret
database_password = get_secret("DATABASE_PASSWORD")
```

**Configuration File Alternative**:
```yaml
# config.yaml
database:
  password: ${DATABASE_PASSWORD}
```

#### Issue: Hardcoded API Key
**Before**:
```python
api_key = "sk-1234567890abcdef"
```

**Remediation**:
```python
import os
api_key = os.getenv("API_KEY")

# Or use secret management service
from secret_manager import get_secret
api_key = get_secret("API_KEY")
```

### 2. Default Credentials

#### Issue: Default Dell iDRAC Credentials
**Before**:
```python
username = "root"
password = "calvin"
```

**Remediation**:
```python
import os
username = os.getenv("IDRAC_USERNAME")
password = os.getenv("IDRAC_PASSWORD")

# Or use DAP secret management
from dell import ctx
username = ctx.get_secret("idrac_username")
password = ctx.get_secret("idrac_password")
```

#### Issue: Default Database Credentials
**Before**:
```python
db_user = "admin"
db_password = "admin"
```

**Remediation**:
```python
import os
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
```

### 3. Connection Strings with Credentials

#### Issue: Connection String with Embedded Credentials
**Before**:
```python
connection_string = "mongodb://user:password@localhost:27017/mydb"
```

**Remediation**:
```python
import os
connection_string = f"mongodb://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:27017/mydb"

# Or use URI format with environment variables
connection_string = os.getenv("DATABASE_CONNECTION_STRING")
```

**Configuration File Alternative**:
```yaml
# config.yaml
database:
  connection_string: ${DATABASE_CONNECTION_STRING}
```

### 4. API Tokens in Configuration

#### Issue: Token in Configuration File
**Before**:
```yaml
api:
  token: "ghp_1234567890abcdef1234567890abcdef"
```

**Remediation**:
```yaml
api:
  token: ${API_TOKEN}
```

**Environment File**:
```bash
# .env
API_TOKEN=ghp_1234567890abcdef1234567890abcdef
```

### 5. Secret Management Integration

#### AWS Secrets Manager
**Before**:
```python
aws_access_key = "AKIAIOSFODNN7EXAMPLE"
aws_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

**Remediation**:
```python
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

aws_access_key = get_secret("/aws/credentials/access_key")
aws_secret_key = get_secret("/aws/credentials/secret_key")
```

#### HashiCorp Vault
**Before**:
```python
api_key = "hardcoded_api_key"
```

**Remediation**:
```python
import hvac

client = hvac.Client(url='http://vault:8200')
client.auth.approle.login(role_id='my-role', secret_id='my-secret')
api_key = client.read('secret/data/api_key')['data']['value']
```

#### Azure Key Vault
**Before**:
```python
storage_key = "storage_account_key_here"
```

**Remediation**:
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net", credential=credential)
storage_key = client.get_secret("storage-key").value
```

### 6. Environment Variable Usage

#### Issue: Direct Environment Variable Access
**Before**:
```python
password = os.environ["DATABASE_PASSWORD"]
```

**Remediation**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# With default value
password = os.getenv("DATABASE_PASSWORD", "")
password = os.getenv("DATABASE_PASSWORD") or raise ValueError("DATABASE_PASSWORD not set")

# Or use typed environment variables
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_password: str

    class Config:
        env_file = ".env"

settings = Settings()
password = settings.database_password
```

### 7. Git Pre-commit Integration

#### Issue: Accidental Credential Commits
**Remediation**:
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔒 Running security audit..."

# Run security scanner
python -m security_audit.scan --pre-commit

# Check exit code
if [ $? -ne 0 ]; then
    echo "❌ Security issues found - commit blocked"
    echo "Run 'security-audit scan --fix' to see remediation suggestions"
    exit 1
fi

echo "✅ Security check passed"
exit 0
```

**Install Hook**:
```bash
chmod +x .git/hooks/pre-commit
```

### 8. Configuration File Security

#### Issue: Secrets in Configuration Files
**Before**:
```yaml
# config.yaml
database:
  host: localhost
  port: 5432
  username: admin
  password: secret123
```

**Remediation**:
```yaml
# config.yaml
database:
  host: localhost
  port: 5432
  username: ${DB_USER}
  password: ${DB_PASSWORD}
```

**Environment File**:
```bash
# .env
DB_USER=admin
DB_PASSWORD=secret123
```

**.gitignore**:
```
.env
.env.local
.env.*.local
```

### 9. Logging Security

#### Issue: Logging Sensitive Information
**Before**:
```python
logger.info(f"Connecting to database with user {username} and password {password}")
```

**Remediation**:
```python
logger.info(f"Connecting to database with user {username}")
# Never log passwords or sensitive data
```

#### Issue: Debug Logging with Secrets
**Before**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger.debug(f"API Key: {api_key}")
```

**Remediation**:
```python
import logging
import os

# Custom filter to hide sensitive data
class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        msg = msg.replace(api_key, "***REDACTED***")
        record.msg = msg
        return True

logger.addFilter(SensitiveDataFilter())
```

### 10. Docker Secrets

#### Issue: Secrets in Dockerfile
**Before**:
```dockerfile
ENV API_KEY=sk-1234567890abcdef
```

**Remediation**:
```dockerfile
# Dockerfile
ENV API_KEY=""
```

**Docker Compose**:
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    environment:
      - API_KEY_FILE=/run/secrets/api_key
    secrets:
      - api_key

secrets:
  api_key:
    file: ./secrets/api_key.txt
```

### 11. Kubernetes Secrets

#### Issue: Secrets in Deployment Configurations
**Before**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  api.key: "sk-1234567890abcdef"
```

**Remediation**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  api.key: "sk-1234567890abcdef"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  api.key.from.secret: "/etc/secrets/api.key"
```

**Secret Creation**:
```bash
kubectl create secret generic app-secrets \
  --from-literal=api.key="sk-1234567890abcdef"
```

### 12. CI/CD Pipeline Security

#### Issue: Secrets in CI/CD Configuration
**Before**:
```yaml
# .gitlab-ci.yml
deploy:
  script:
    - echo "Deploying with API_KEY=sk-1234567890abcdef"
```

**Remediation**:
```yaml
# .gitlab-ci.yml
deploy:
  script:
    - echo "Deploying with masked API key"
    - export API_KEY=$CI_API_KEY
    - ./deploy.sh
  variables:
    CI_API_KEY: $CI_API_KEY  # Masked variable
```

#### Issue: GitHub Actions Secrets
**Before**:
```yaml
# .github/workflows/deploy.yml
- name: Deploy
  run: |
    echo "Deploying with token=ghp_1234567890abcdef"
```

**Remediation**:
```yaml
# .github/workflows/deploy.yml
- name: Deploy
  run: |
    echo "Deploying with masked token"
    ./deploy.sh
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 13. Database Credentials Management

#### Issue: Hardcoded Database Credentials
**Before**:
```python
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="admin",
    password="secret123"
)
```

**Remediation**:
```python
import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "mydb"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

# Or use connection string
connection_string = os.getenv("DATABASE_CONNECTION_STRING")
conn = psycopg2.connect(connection_string)
```

### 14. API Client Security

#### Issue: Hardcoded API Credentials
**Before**:
```python
import requests

response = requests.get(
    "https://api.example.com/data",
    headers={"Authorization": "Bearer sk-1234567890abcdef"}
)
```

**Remediation**:
```python
import os
import requests

api_key = os.getenv("API_KEY")
response = requests.get(
    "https://api.example.com/data",
    headers={"Authorization": f"Bearer {api_key}"}
)

# Or use session with token
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {api_key}"})
```

### 15. File Permission Security

#### Issue: World-readable Credential Files
**Before**:
```bash
# File with credentials has insecure permissions
-rw-r--r-- 1 user user 100 Jan 1 12:00 credentials.txt
```

**Remediation**:
```bash
# Restrict file permissions
chmod 600 credentials.txt
# Result: -rw------- 1 user user 100 Jan 1 12:00 credentials.txt

# For directories
chmod 700 .secrets
```

**Python Script**:
```python
import os

def secure_file_permissions(file_path):
    """Set secure file permissions (600 for files, 700 for directories)"""
    if os.path.isfile(file_path):
        os.chmod(file_path, 0o600)
    elif os.path.isdir(file_path):
        os.chmod(file_path, 0o700)
```

### 16. Temporary File Security

#### Issue: Sensitive Data in Temporary Files
**Before**:
```python
# Writing sensitive data to temp file
with open("/tmp/sensitive_data.txt", "w") as f:
    f.write(secret_data)
```

**Remediation**:
```python
import os
import tempfile

# Use secure temporary file with restricted permissions
with tempfile.NamedTemporaryFile(mode='w', delete=True, prefix='secure_') as f:
    f.write(secret_data)
    # File is automatically deleted and has restricted permissions
```

### 17. Memory Security

#### Issue: Sensitive Data in Memory
**Before**:
```python
password = "secret_password_123"
# Password remains in memory for program lifetime
```

**Remediation**:
```python
import sys

def secure_string(s):
    """Zero out sensitive string from memory"""
    try:
        # Zero out the string
        zeroed = '\x00' * len(s)
        s = zeroed
    except:
        pass

password = "secret_password_123"
# Use password...
secure_string(password)
```

### 18. Encryption at Rest

#### Issue: Unencrypted Secrets in Files
**Before**:
```python
# Storing secrets in plain text
with open("secrets.txt", "w") as f:
    f.write("api_key=sk-1234567890abcdef")
```

**Remediation**:
```python
from cryptography.fernet import Fernet
import os

# Generate or load encryption key
key = os.getenv("ENCRYPTION_KEY") or Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt secret
secret = "sk-1234567890abcdef"
encrypted_secret = cipher_suite.encrypt(secret.encode())

# Store encrypted secret
with open("secrets.enc", "wb") as f:
    f.write(encrypted_secret)

# Decrypt when needed
with open("secrets.enc", "rb") as f:
    encrypted_secret = f.read()
    decrypted_secret = cipher_suite.decrypt(encrypted_secret).decode()
```

### 19. Logging and Monitoring

#### Issue: Insufficient Security Logging
**Remediation**:
```python
import logging
from datetime import datetime

class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)
        
        # Log to file with restricted permissions
        handler = logging.FileHandler('security.log')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
    
    def log_credential_access(self, user, resource):
        self.logger.info(f"Credential access - User: {user}, Resource: {resource}, Time: {datetime.now()}")
    
    def log_security_event(self, event_type, details):
        self.logger.warning(f"Security event - Type: {event_type}, Details: {details}, Time: {datetime.now()}")

security_logger = SecurityLogger()
security_logger.log_credential_access("user123", "database")
```

### 20. Post-Remediation Validation

#### Validation Checklist
- [ ] No hardcoded credentials in code
- [ ] All secrets use environment variables or secret management
- [ ] .gitignore excludes sensitive files
- [ ] File permissions are secure (600/700)
- [ ] Logging does not expose sensitive data
- [ ] Pre-commit hooks are installed
- [ ] CI/CD pipelines use secret management
- [ ] Temporary files are securely handled
- [ ] Encryption is used for stored secrets
- [ ] Security audit passes

#### Automated Validation
```python
from security_audit import SecurityScanner

def validate_remediation():
    """Validate that all security issues have been remediated"""
    scanner = SecurityScanner(project_path=".")
    findings = scanner.scan_all_files()
    
    critical_issues = [f for f in findings if f.severity == "critical"]
    high_issues = [f for f in findings if f.severity == "high"]
    
    if critical_issues:
        print("❌ Critical security issues remain:")
        for issue in critical_issues:
            print(f"  - {issue.file}:{issue.line} - {issue.issue}")
        return False
    
    if high_issues:
        print("⚠️  High severity issues remain:")
        for issue in high_issues:
            print(f"  - {issue.file}:{issue.line} - {issue.issue}")
    
    print("✅ All critical issues resolved")
    return len(high_issues) == 0

if __name__ == "__main__":
    validate_remediation()
```

## Best Practices Summary

1. **Never hardcode credentials** - Always use environment variables or secret management
2. **Use secret management services** - AWS Secrets Manager, HashiCorp Vault, Azure Key Vault
3. **Implement pre-commit hooks** - Automate security checks before Git commits
4. **Secure file permissions** - Use 600 for files, 700 for directories
5. **Encrypt secrets at rest** - Use encryption for stored secrets
6. **Log security events** - Monitor credential access and security events
7. **Regular security audits** - Schedule periodic security scans
8. **Educate team members** - Train developers on security best practices
9. **Use secure defaults** - Configure secure defaults for all systems
10. **Monitor for leaks** - Implement secret scanning in CI/CD pipelines

## Additional Resources

- OWASP Cheat Sheet Series
- NIST Cybersecurity Framework
- CIS Benchmarks
- Cloud Provider Security Best Practices
- Secret Scanning Tools Documentation