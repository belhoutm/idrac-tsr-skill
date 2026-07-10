#!/usr/bin/env python3
"""
Security Scanner - Scans code for credentials, secrets, and sensitive information
"""

import os
import re
import json
import hashlib
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from enum import Enum
import fnmatch


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class SecurityFinding:
    """Represents a security finding"""
    file: str
    line: int
    column: int
    severity: Severity
    issue: str
    pattern: str
    matched_text: str
    suggestion: str
    confidence: str = "HIGH"
    
    def to_dict(self) -> Dict:
        return {
            'file': self.file,
            'line': self.line,
            'column': self.column,
            'severity': self.severity.value,
            'issue': self.issue,
            'pattern': self.pattern,
            'matched_text': self.matched_text,
            'suggestion': self.suggestion,
            'confidence': self.confidence
        }


class SecurityScanner:
    """Main security scanning class"""
    
    def __init__(self, project_path: str = ".", config_file: str = ".security-audit.yaml"):
        self.project_path = Path(project_path)
        self.config_file = Path(config_file)
        self.findings: List[SecurityFinding] = []
        self.config = self._load_config()
        self.patterns = self._load_patterns()
        self.excluded_files = self._load_exclusions()
        
    def _load_config(self) -> Dict:
        """Load configuration from YAML file"""
        config = {
            'exclude_patterns': ['*.log', 'node_modules/', '.git/', 'venv/', '__pycache__/', 'security-audit/'],
            'severity_threshold': 'HIGH',
            'file_types': ['.py', '.js', '.ts', '.yaml', '.yml', '.json', '.md', '.sh', '.bash'],
            'ignore_files': ['examples/*', 'tests/*', 'security-audit/*', '*/references/*'],
            'custom_patterns': []
        }
        
        if self.config_file.exists():
            try:
                import yaml
                with open(self.config_file, 'r') as f:
                    user_config = yaml.safe_load(f)
                    config.update(user_config)
            except ImportError:
                print("Warning: PyYAML not installed, using default configuration")
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return config
    
    def _load_patterns(self) -> List[Dict]:
        """Load security patterns"""
        patterns = [
            # Credential patterns
            {
                'name': 'password_assignment',
                'pattern': r'password\s*=\s*["\'][^"\']{4,}["\']',
                'severity': 'HIGH',
                'issue': 'Hardcoded password detected',
                'suggestion': 'Use environment variables or secret management'
            },
            {
                'name': 'api_key_assignment',
                'pattern': r'api[_-]?key\s*=\s*["\'][A-Za-z0-9]{20,}["\']',
                'severity': 'CRITICAL',
                'issue': 'Hardcoded API key detected',
                'suggestion': 'Use environment variables or secret management'
            },
            {
                'name': 'secret_assignment',
                'pattern': r'secret\s*=\s*["\'][^"\']{4,}["\']',
                'severity': 'HIGH',
                'issue': 'Hardcoded secret detected',
                'suggestion': 'Use environment variables or secret management'
            },
            {
                'name': 'token_assignment',
                'pattern': r'token\s*=\s*["\'][A-Za-z0-9]{20,}["\']',
                'severity': 'HIGH',
                'issue': 'Hardcoded token detected',
                'suggestion': 'Use environment variables or secret management'
            },
            # Default credentials
            {
                'name': 'default_dell_idrac',
                'pattern': r'root.*calvin',
                'severity': 'HIGH',
                'issue': 'Default Dell iDRAC credentials detected',
                'suggestion': 'Use secure credential management'
            },
            {
                'name': 'default_admin_credentials',
                'pattern': r'admin.*admin|admin.*password',
                'severity': 'HIGH',
                'issue': 'Default admin credentials detected',
                'suggestion': 'Use secure credential management'
            },
            # AWS patterns
            {
                'name': 'aws_access_key',
                'pattern': r'AKIA[0-9A-Z]{16}',
                'severity': 'CRITICAL',
                'issue': 'AWS Access Key detected',
                'suggestion': 'Use AWS IAM roles or secrets manager'
            },
            {
                'name': 'aws_secret_key',
                'pattern': r'aws[_-]?secret[_-]?access[_-]?key\s*=\s*["\'][A-Za-z0-9+/]{20,}["\']',
                'severity': 'CRITICAL',
                'issue': 'AWS Secret Key detected',
                'suggestion': 'Use AWS Secrets Manager'
            },
            # GitHub tokens
            {
                'name': 'github_token',
                'pattern': r'gh[pous]_[a-zA-Z0-9]{36}',
                'severity': 'CRITICAL',
                'issue': 'GitHub token detected',
                'suggestion': 'Use GitHub Actions secrets or environment variables'
            },
            # Stripe keys
            {
                'name': 'stripe_key',
                'pattern': r'sk_[a-z]+_[a-zA-Z0-9]{24}',
                'severity': 'CRITICAL',
                'issue': 'Stripe API key detected',
                'suggestion': 'Use environment variables or secret management'
            },
            # Connection strings
            {
                'name': 'mongodb_connection_string',
                'pattern': r'mongodb://[^:]+:[^@]+@',
                'severity': 'CRITICAL',
                'issue': 'MongoDB connection string with credentials',
                'suggestion': 'Use environment variables for connection string'
            },
            {
                'name': 'database_connection_string',
                'pattern': r'(postgres|mysql)://[^:]+:[^@]+@',
                'severity': 'CRITICAL',
                'issue': 'Database connection string with credentials',
                'suggestion': 'Use environment variables for connection string'
            },
            # Bearer tokens
            {
                'name': 'bearer_token',
                'pattern': r'Bearer\s+[A-Za-z0-9\-._~+/]{20,}',
                'severity': 'HIGH',
                'issue': 'Bearer token detected',
                'suggestion': 'Use secure token management'
            },
            # JWT tokens
            {
                'name': 'jwt_token',
                'pattern': r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+',
                'severity': 'HIGH',
                'issue': 'JWT token detected',
                'suggestion': 'Use secure token management'
            },
            # Private keys
            {
                'name': 'private_key',
                'pattern': r'-----BEGIN [A-Z]+ PRIVATE KEY-----',
                'severity': 'CRITICAL',
                'issue': 'Private key detected',
                'suggestion': 'Never commit private keys to Git'
            },
        ]
        
        # Add custom patterns from config
        patterns.extend(self.config.get('custom_patterns', []))
        
        return patterns
    
    def _load_exclusions(self) -> Set[str]:
        """Load file exclusions"""
        exclusions = set()
        
        # Add patterns from config
        for pattern in self.config.get('exclude_patterns', []):
            exclusions.add(pattern)
        
        # Add gitignore patterns
        gitignore_path = self.project_path / '.gitignore'
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        exclusions.add(line)
        
        return exclusions
    
    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if file should be excluded from scanning"""
        relative_path = file_path.relative_to(self.project_path)
        path_str = str(relative_path)
        
        # Check exclusion patterns
        for pattern in self.excluded_files:
            if fnmatch.fnmatch(path_str, pattern):
                return True
        
        # Check file type
        file_extension = file_path.suffix.lower()
        if file_extension not in self.config.get('file_types', []):
            return True
        
        # Check ignore patterns
        for pattern in self.config.get('ignore_files', []):
            if fnmatch.fnmatch(path_str, pattern):
                return True
        
        return False
    
    def _is_placeholder(self, text: str) -> bool:
        """Check if matched text is a placeholder"""
        placeholder_patterns = [
            r'<[A-Z_]+>',
            r'\{[A-Z_]+\}',
            r'\$\{[A-Z_]+\}',
            r'example',
            r'test',
            r'demo',
            r'placeholder',
            r'xxx',
            r'replace'
        ]
        
        for pattern in placeholder_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _is_in_comment(self, line: str, column: int, file_extension: str) -> bool:
        """Check if match is in a comment"""
        # Simple check for common comment patterns
        comment_patterns = {
            '.py': [r'#.*'],
            '.js': [r'//.*', r'/\*.*?\*/'],
            '.ts': [r'//.*', r'/\*.*?\*/'],
            '.yaml': [r'#.*'],
            '.yml': [r'#.*'],
            '.sh': [r'#.*'],
            '.bash': [r'#.*'],
            '.md': [r'<!--.*-->', r'<!--'],
        }
        
        patterns = comment_patterns.get(file_extension, [r'#.*'])
        
        # Check if match position is after comment start
        for pattern in patterns:
            if re.search(pattern, line[:column]):
                return True
        
        return False
    
    def _scan_file(self, file_path: Path) -> List[SecurityFinding]:
        """Scan a single file for security issues"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            file_extension = file_path.suffix.lower()
            
            for line_num, line in enumerate(lines, 1):
                for pattern_info in self.patterns:
                    pattern = pattern_info['pattern']
                    
                    try:
                        for match in re.finditer(pattern, line):
                            matched_text = match.group()
                            start_col = match.start() + 1
                            end_col = match.end()
                            
                            # Skip if placeholder
                            if self._is_placeholder(matched_text):
                                continue
                            
                            # Skip if in comment
                            if self._is_in_comment(line, start_col, file_extension):
                                continue
                            
                            # Create finding
                            finding = SecurityFinding(
                                file=str(file_path.relative_to(self.project_path)),
                                line=line_num,
                                column=start_col,
                                severity=Severity[pattern_info['severity']],
                                issue=pattern_info['issue'],
                                pattern=pattern_info['name'],
                                matched_text=matched_text,
                                suggestion=pattern_info['suggestion'],
                                confidence="HIGH"
                            )
                            
                            findings.append(finding)
                    
                    except re.error:
                        continue
        
        except Exception as e:
            print(f"Error scanning file {file_path}: {e}")
        
        return findings
    
    def scan_all_files(self) -> List[SecurityFinding]:
        """Scan all files in the project"""
        self.findings = []
        
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and not self._should_exclude_file(file_path):
                findings = self._scan_file(file_path)
                self.findings.extend(findings)
        
        return self.findings
    
    def scan_staged_files(self) -> List[SecurityFinding]:
        """Scan only staged Git files"""
        import subprocess
        
        self.findings = []
        
        try:
            # Get staged files
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                capture_output=True,
                text=True,
                cwd=self.project_path
            )
            
            staged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            for file_path_str in staged_files:
                file_path = self.project_path / file_path_str
                if file_path.exists() and not self._should_exclude_file(file_path):
                    findings = self._scan_file(file_path)
                    self.findings.extend(findings)
        
        except Exception as e:
            print(f"Error getting staged files: {e}")
        
        return self.findings
    
    def generate_report(self, findings: List[SecurityFinding]) -> Dict:
        """Generate security audit report"""
        report = {
            'summary': {
                'total_findings': len(findings),
                'critical': len([f for f in findings if f.severity == Severity.CRITICAL]),
                'high': len([f for f in findings if f.severity == Severity.HIGH]),
                'medium': len([f for f in findings if f.severity == Severity.MEDIUM]),
                'low': len([f for f in findings if f.severity == Severity.LOW]),
            },
            'findings': [finding.to_dict() for finding in findings],
            'files_affected': len(set(f.file for f in findings)),
            'scan_timestamp': str(Path.cwd()),
            'project_path': str(self.project_path)
        }
        
        return report
    
    def print_report(self, findings: List[SecurityFinding]):
        """Print security audit report to console"""
        report = self.generate_report(findings)
        
        print("\n" + "="*60)
        print("SECURITY AUDIT REPORT")
        print("="*60)
        
        print(f"\n📊 Summary:")
        print(f"  Total Findings: {report['summary']['total_findings']}")
        print(f"  Critical: {report['summary']['critical']} 🔴")
        print(f"  High: {report['summary']['high']} 🟠")
        print(f"  Medium: {report['summary']['medium']} 🟡")
        print(f"  Low: {report['summary']['low']} 🟢")
        print(f"  Files Affected: {report['files_affected']}")
        
        # Check threshold
        threshold = self.config.get('severity_threshold', 'HIGH')
        threshold_severity = Severity[threshold]
        
        critical_findings = [f for f in findings if f.severity == Severity.CRITICAL]
        high_findings = [f for f in findings if f.severity == Severity.HIGH]
        
        if threshold_severity == Severity.CRITICAL and critical_findings:
            print(f"\n❌ CRITICAL issues found - scan failed threshold")
        elif threshold_severity == Severity.HIGH and (critical_findings or high_findings):
            print(f"\n❌ HIGH/CRITICAL issues found - scan failed threshold")
        else:
            print(f"\n✅ Scan passed threshold ({threshold})")
        
        if findings:
            print("\n🔍 Findings:")
            for finding in findings:
                emoji = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟠',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }[finding.severity.value]
                
                print(f"\n{emoji} {finding.file}:{finding.line}")
                print(f"   Issue: {finding.issue}")
                print(f"   Pattern: {finding.pattern}")
                print(f"   Found: {finding.matched_text}")
                print(f"   Suggestion: {finding.suggestion}")
        else:
            print("\n✅ No security issues found")
        
        print("\n" + "="*60)
    
    def save_report(self, findings: List[SecurityFinding], output_file: str = "security-report.json"):
        """Save security audit report to file"""
        report = self.generate_report(findings)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Report saved to {output_file}")


def main():
    """Main entry point for security scanner"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Security Scanner for Git Repositories')
    parser.add_argument('--path', default='.', help='Project path to scan')
    parser.add_argument('--config', default='.security-audit.yaml', help='Configuration file')
    parser.add_argument('--staged', action='store_true', help='Scan only staged files')
    parser.add_argument('--report', help='Output report file')
    parser.add_argument('--pre-commit', action='store_true', help='Run in pre-commit mode')
    
    args = parser.parse_args()
    
    scanner = SecurityScanner(args.path, args.config)
    
    if args.staged:
        print("🔒 Scanning staged files...")
        findings = scanner.scan_staged_files()
    else:
        print("🔒 Scanning all files...")
        findings = scanner.scan_all_files()
    
    scanner.print_report(findings)
    
    if args.report:
        scanner.save_report(findings, args.report)
    
    # Pre-commit mode: exit with error if critical issues found
    if args.pre_commit:
        critical_findings = [f for f in findings if f.severity == Severity.CRITICAL]
        high_findings = [f for f in findings if f.severity == Severity.HIGH]
        
        if critical_findings or high_findings:
            print("\n❌ Security issues found - commit blocked")
            exit(1)
        else:
            print("\n✅ Security check passed - commit allowed")
            exit(0)


if __name__ == "__main__":
    main()