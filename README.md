# iDRAC-TSR-Skill Project

Integrated Dell server management and analysis skills combining active iDRAC operations with specialized TSR (Technical Support Report) log analysis.

## Overview

This project contains two complementary skills for Dell PowerEdge server management:

- **idrac**: Comprehensive iDRAC management and server operations
- **tsr-analysis**: Specialized TSR log analysis and diagnostics

## Skills

### 1. idrac Skill

**Purpose**: Active iDRAC management and server operations

**Capabilities**:
- Power management (power on/off, restart, boot control)
- System inventory and hardware information
- Firmware updates and configuration management
- Multiple connection methods (Redfish API, racadm CLI, SNMP)
- DAP blueprint integration for automation
- Security best practices for credential management

**Key Features**:
- Redfish API integration for modern server management
- racadm CLI support for traditional operations
- SNMP monitoring capabilities
- Automated workflows via DAP blueprints
- Batch operations across multiple servers
- Scheduled maintenance windows

**Use Cases**:
- Server power control and lifecycle management
- Firmware updates and maintenance
- Hardware inventory and configuration
- Automated server provisioning
- System monitoring and health checks

**Documentation**: See `skills/idrac/skill.md` for complete reference

### 2. tsr-analysis Skill

**Purpose**: Deep-dive analysis of Dell Technical Support Reports

**Capabilities**:
- TSR package structure analysis
- Hardware state and configuration review
- Lifecycle log analysis and event correlation
- Critical failure pattern detection
- System comparison and baseline analysis
- Deployment failure diagnosis

**Key Features**:
- I2C/VR communication failure detection
- Power supply issue analysis
- Memory and hardware diagnostics
- Timeline analysis of system events
- Configuration comparison between systems
- Known issue pattern matching

**Use Cases**:
- Hardware failure diagnosis
- Deployment failure investigation
- System health assessment
- Post-mortem analysis
- Configuration drift detection
- Performance issue troubleshooting

**Documentation**: See `tsr-analysis/skill.md` for complete reference

## Integration Between Skills

The skills are designed to work together:

### Typical Workflow

1. **Orchestration** (`workflows/main.md`):
   - Parse timestamps and analyze lifecycle logs
   - Route to the right `skills/<subsystem>/skill.md`
   - Correlate findings across subsystems

2. **Active Management** (idrac skill):
   - Monitor server health via iDRAC
   - Collect TSR reports when issues are detected
   - Perform initial diagnostics

3. **Deep Analysis** (tsr-analysis skill):
   - Analyze collected TSR reports
   - Identify root causes of failures
   - Compare with baseline configurations

4. **Security Audit** (security-audit skill):
   - Scan code and artifacts for credentials or secrets
   - Run before any Git operation

5. **Resolution** (idrac skill):
   - Apply configuration fixes
   - Update firmware if needed
   - Verify resolution

### Example Use Case

**Scenario**: Server experiencing intermittent reboots

```bash
# Step 1: Use idrac skill to collect TSR
# SECURITY: Replace with your actual credentials
# Never commit real credentials to Git
racadm -r <server-ip> -u <YOUR_USERNAME> -p <YOUR_PASSWORD> techsupportreport

# Step 2: Use tsr-analysis skill to analyze
cd tsr-analysis
python analyze_tsr.py TSR<ServiceTag>_<timestamp>.zip

# Step 3: Use idrac skill to apply fixes
# SECURITY: Replace with your actual credentials
# Never commit real credentials to Git
racadm -r <server-ip> -u <YOUR_USERNAME> -p <YOUR_PASSWORD> set BIOS.ProcSettings.LogicalProc Enable
```

## Project Structure

```
iDRAC-TSR-Skill/
├── README.md                    # This file
├── QUICKSTART.md               # Quick start guide
├── TRIGGER_GUIDE.md          # @ notation usage guide
├── PROJECT_SUMMARY.md        # Project overview
├── project-config.json       # Project configuration
├── workflows/                 # Cross-skill orchestration workflows
│   └── main.md               # Main troubleshooting workflow
├── skills/idrac/                 # iDRAC management skill
│   ├── skill.md              # Main skill documentation
│   ├── SKILL.md              # Symlink to skill.md for compatibility
│   ├── workflow.md           # Step-by-step workflows
│   ├── signatures.yaml       # Error signatures and health weights
│   ├── examples.md           # Usage examples and snippets
│   ├── references.md         # Command and endpoint reference
│   ├── examples/             # Blueprint templates
│   └── scripts/              # Python scripts for iDRAC operations
├── tsr-analysis/               # TSR analysis skill
│   ├── skill.md              # Main skill documentation
│   └── SKILL.md              # Symlink to skill.md for compatibility
└── security-audit/           # Security audit skill
    ├── skill.md              # Main skill documentation
    ├── SKILL.md              # Symlink to skill.md for compatibility
    ├── references/           # Security patterns and remediation
    ├── scripts/              # Security scanning scripts
    └── patterns/             # Detection patterns
```

## Installation

### Prerequisites

- Python 3.8+
- Access to Dell PowerEdge servers with iDRAC
- Network connectivity to iDRAC interfaces
- Appropriate credentials for server management

### Setup

1. Clone or copy this project to your desired location
2. Ensure Python dependencies are installed:
   ```bash
   pip install redfish argparse
   ```
3. Configure iDRAC credentials using environment variables or secure storage
4. Test connectivity to your iDRAC interfaces

## Usage

### Quick Trigger Notation

Both skills support quick `@` trigger notation for faster invocation:

- **@idrac** - Immediately invoke the idrac skill
- **@tsr** - Immediately invoke the tsr-analysis skill
- **@security-audit** - Immediately invoke the security-audit skill

**Examples:**
```
"@idrac power on server 192.168.1.100"
"@tsr analyze TSR<ServiceTag>_timestamp.zip"
"@idrac get system inventory"
"@tsr check for hardware failures"
"@security-audit scan for credentials"
"@security-audit pre-commit check"
```

### Using the idrac Skill

Invoke the skill when working with iDRAC operations:

```
"@idrac power on server 192.168.1.100"
"@idrac analyze the TSR report"
"@idrac create a blueprint for firmware updates"
"Use the idrac skill to power on server 192.168.1.100"
"Analyze the TSR report using idrac capabilities"
"Create a blueprint for iDRAC firmware updates"
```

### Using the tsr-analysis Skill

Invoke the skill when analyzing TSR logs:

```
"@tsr diagnose the hardware failure"
"@tsr analyze this TSR report for I2C communication failures"
"@tsr compare the TSR reports between working and failing systems"
"Use tsr-analysis to diagnose the hardware failure"
"Analyze this TSR report for I2C communication failures"
"Compare the TSR reports between working and failing systems"
```

### Using the security-audit Skill

Invoke the skill for security scanning and credential detection:

```
"@security-audit scan for credentials"
"@security-audit pre-commit check"
"@security-audit check for secrets"
"@security-audit generate security report"
```

**Security Features:**
- Pre-commit credential scanning
- Secret and token detection
- Comprehensive pattern matching
- Remediation suggestions
- Git hook integration

## Security Considerations

**CRITICAL**: Both skills involve server management credentials:

1. **Never hardcode credentials** - Use secure credential management
2. **Use secret_key inputs** for DAP blueprints
3. **Implement credential rotation** - Regularly update passwords
4. **Limit access** - Use least-privilege accounts
5. **Audit access** - Track who accesses server management functions
6. **Use HTTPS** - Ensure encrypted connections to iDRAC

## Common Workflows

### Hardware Failure Investigation

1. **Collect TSR** (idrac):
   ```bash
   racadm -r <server-ip> techsupportreport
   ```

2. **Analyze TSR** (tsr-analysis):
   - Extract and validate TSR structure
   - Search for I2C/VR communication failures
   - Review lifecycle events
   - Check hardware sensor data

3. **Apply Fixes** (idrac):
   - Update firmware if needed
   - Replace hardware components
   - Verify resolution

### Deployment Troubleshooting

1. **Monitor Deployment** (idrac):
   - Check server power state
   - Review network configuration
   - Verify firmware compatibility

2. **Analyze Failure** (tsr-analysis):
   - Review deployment timeline in TSR
   - Check for configuration errors
   - Identify hardware issues

3. **Resolve Issues** (idrac):
   - Apply configuration corrections
   - Update components
   - Retry deployment

### System Health Monitoring

1. **Continuous Monitoring** (idrac):
   - Set up health checks via Redfish
   - Monitor sensor readings
   - Track system events

2. **Periodic Analysis** (tsr-analysis):
   - Collect and analyze TSR reports regularly
   - Identify trends and degradation
   - Compare with baseline configurations

3. **Preventive Maintenance** (idrac):
   - Schedule firmware updates
   - Replace degrading components
   - Optimize configurations

## Troubleshooting

### Common Issues

**Cannot connect to iDRAC**:
- Verify network connectivity
- Check iDRAC IP address
- Ensure credentials are correct
- Check firewall rules

**TSR analysis fails**:
- Verify TSR file is not corrupted
- Ensure sufficient disk space for extraction
- Check if TSR is password-protected
- Validate TSR format

**Permission errors**:
- Verify account has sufficient privileges
- Check iDRAC user role assignments
- Ensure proper authentication method

### Debug Mode

Enable debug logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# For Redfish operations
client = RedfishClient(host, username, password, debug=True)
```

## Best Practices

1. **Always backup configurations** before making changes
2. **Test in non-production** before applying to production systems
3. **Document all changes** for audit trails
4. **Use automated workflows** to reduce human error
5. **Regularly update firmware** for security and stability
6. **Monitor system health** proactively
7. **Analyze TSR reports** periodically for trend analysis

## Integration with Other Tools

### DAP Blueprints

Both skills integrate with DAP (Dell NativeEdge) blueprints:

- **idrac**: Custom node types for server operations
- **tsr-analysis**: Analysis scripts for deployment troubleshooting

### Monitoring Systems

- Export TSR analysis results to monitoring platforms
- Integrate iDRAC health checks with alerting systems
- Automate TSR collection on alert triggers

### Automation

- Use with CI/CD pipelines for server provisioning
- Integrate with configuration management tools
- Automate periodic TSR collection and analysis

## Git Workflow

This project follows a feature-branch workflow with small, testable commits. See [`.github/workflows/git-workflow-guide.md`](.github/workflows/git-workflow-guide.md) for detailed documentation.

### Quick Start

```bash
# Create a new feature branch
./scripts/git-helpers.sh new-feature add-nic-sensor

# Make changes and commit
./scripts/git-helpers.sh save "Add NIC sensor detection"

# Push feature branch
./scripts/git-helpers.sh push-feature

# Create Pull Request on GitHub
# ... (via GitHub UI)

# Merge after approval
./scripts/git-helpers.sh merge-feature
```

### Git Helper Script

Use the helper script for common operations:

```bash
./scripts/git-helpers.sh new-feature <name>    # Create feature branch
./scripts/git-helpers.sh new-fix <name>        # Create fix branch
./scripts/git-helpers.sh save <message>        # Stage and commit
./scripts/git-helpers.sh push-feature          # Push to origin
./scripts/git-helpers.sh merge-feature         # Merge to master
./scripts/git-helpers.sh cleanup               # Delete merged branches
./scripts/git-helpers.sh status                # Show status
./scripts/git-helpers.sh undo-last             # Undo last commit
```

### Pre-commit Hooks

Pre-commit hooks automatically check for:
- Hardcoded credentials (passwords, secrets, tokens)
- Large files (>1MB)
- Python syntax errors
- YAML syntax issues

## Contributing

When extending these skills:

1. **Follow Git workflow**: Use feature branches and small commits
2. **Test changes**: Verify functionality before committing
3. **Security first**: Never hardcode credentials
4. **Document changes**: Update relevant documentation
5. **Maintain consistency**: Follow existing patterns
6. **Add examples**: Include usage examples for new features

## Support

For issues or questions:

1. Check the individual skill documentation
2. Review Dell official documentation
3. Enable debug mode for detailed logging
4. Contact Dell support for hardware-specific issues

## License

This project provides integration and documentation for Dell server management tools. Dell iDRAC and TSR analysis tools are subject to Dell's licensing terms.

## Version History

- **v1.0** - Initial integration of idrac and tsr-analysis skills
- Combined active server management with passive log analysis
- Comprehensive documentation and workflow examples