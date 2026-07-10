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

**Documentation**: See `idrac/SKILL.md` for complete reference

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

**Documentation**: See `tsr-analysis/SKILL.md` for complete reference

## Integration Between Skills

The two skills are designed to work together:

### Typical Workflow

1. **Active Management** (idrac skill):
   - Monitor server health via iDRAC
   - Collect TSR reports when issues are detected
   - Perform initial diagnostics

2. **Deep Analysis** (tsr-analysis skill):
   - Analyze collected TSR reports
   - Identify root causes of failures
   - Compare with baseline configurations

3. **Resolution** (idrac skill):
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
├── idrac/                       # iDRAC management skill
│   ├── SKILL.md                # Main skill documentation
│   ├── README.md             # Skill-specific readme
│   ├── references/             # Reference materials
│   ├── examples/               # Example scripts and templates
│   ├── scripts/              # Python scripts for iDRAC operations
│   ├── patterns/             # Analysis patterns
│   ├── known-issues/         # Known issues database
│   └── idrac-architecture/    # Architecture documentation
├── tsr-analysis/               # TSR analysis skill
│   └── SKILL.md              # Main skill documentation
└── security-audit/           # Security audit skill
    ├── SKILL.md              # Main skill documentation
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

## Contributing

When extending these skills:

1. Maintain consistency with existing documentation
2. Add security considerations for new operations
3. Include examples for new functionality
4. Update integration documentation
5. Test thoroughly in non-production environments

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