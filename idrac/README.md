# Dell iDRAC Management & TSR Analysis Skill

A comprehensive skill for interacting with Dell iDRAC (Integrated Dell Remote Access Controller) and analyzing Technical Support Reports (TSR). This skill supports multiple connection methods (Redfish API, racadm CLI, SNMP) and integrates with DAP blueprints for automated server management.

## Skill Overview

This skill provides:

- **Multiple Connection Methods**: Redfish API, racadm CLI, and SNMP support
- **Power Management**: Power on/off, restart, boot configuration
- **System Inventory**: Hardware information, firmware versions, component details
- **TSR Analysis**: Comprehensive analysis of Technical Support Reports
- **Health Monitoring**: System health assessment and error detection
- **DAP Integration**: Blueprint templates for automated server management
- **Security Best Practices**: Secure credential handling and SSL/TLS support

## Directory Structure

```
.devin/skills/idrac/
├── SKILL.md                          # Main skill documentation
├── README.md                         # This file
├── references/                       # Reference documentation
│   ├── redfish-api.md               # Redfish API reference
│   ├── racadm-cli.md                # racadm CLI reference
│   ├── tsr-analysis.md              # TSR analysis workflows
│   └── workflow-guide.md            # Step-by-step workflow guides
├── scripts/                          # Example Python scripts
│   ├── idrac_redfish_client.py      # Redfish API client
│   └── tsr_analyzer.py              # TSR analysis tool
├── examples/                         # Example blueprints and templates
│   └── blueprint-templates/
│       ├── idrac-power-management.yaml
│       ├── idrac-power-management-inputs.yaml
│       └── idrac-power-management-capabilities.yaml
├── idrac-architecture/               # Architecture documentation
│   ├── lld/                         # Low-Level Design documents
│   ├── hld/                         # High-Level Design documents
│   ├── guides/                      # User guides and manuals
│   │   └── documentation-index.md   # Documentation index
│   ├── specs/                       # Technical specifications
│   └── release-notes/               # Version release notes
│       └── release-notes-index.md  # Release notes index
├── known-issues/                     # Known issues database
│   └── known-issues-index.md        # Known issues catalog
└── patterns/                         # Error patterns and troubleshooting
    └── error-patterns-index.md      # Error patterns database
```

## Quick Start

### 1. Using the Skill

When you need to work with Dell iDRAC, simply mention iDRAC-related tasks:

- "Configure iDRAC network settings"
- "Analyze TSR report for errors"
- "Update server firmware"
- "Check server health status"
- "Power management operations"

### 2. Basic iDRAC Operations

#### Using Redfish API (Recommended)

```python
from scripts.idrac_redfish_client import IDRACRedfishClient

# Initialize client
client = IDRACRedfishClient(
    host='192.168.1.100',
    username='root',
    password='calvin',
    verify_ssl=False
)

# Get system information
system_info = client.get_system_info()
print(f"Model: {system_info['Model']}")

# Power on server
client.power_on()

# Restart server
client.restart_server()
```

#### Using racadm CLI

```bash
# Get system information
racadm -r 192.168.1.100 -u root -p calvin get System

# Power on server
racadm -r 192.168.1.100 -u root -p calvin serveraction powerup

# Get system logs
racadm -r 192.168.1.100 -u root -p calvin getsel
```

### 3. TSR Analysis

```python
from scripts.tsr_analyzer import TSRAnalyzer

# Analyze TSR report
analyzer = TSRAnalyzer('tsr_report.zip')

# Generate comprehensive report
report = analyzer.generate_report()

# Get health assessment
health = report['health_assessment']
print(f"Overall Health: {health['overall_health']}")
print(f"Health Score: {health['health_score']}")

# Get error analysis
errors = report['error_analysis']
print(f"Critical Errors: {len(errors['critical'])}")
print(f"Warnings: {len(errors['warning'])}")
```

### 4. DAP Blueprint Integration

Use the provided blueprint templates for DAP integration:

```bash
# Copy blueprint templates to your project
cp examples/blueprint-templates/* /path/to/your/blueprint/

# Customize inputs for your environment
# Deploy via DAP
```

## Key Features

### Connection Methods

- **Redfish API**: Modern REST API for comprehensive iDRAC management
- **racadm CLI**: Traditional command-line interface for quick operations
- **SNMP**: Simple Network Management Protocol for basic monitoring

### Power Management

- Power on/off operations
- Graceful and forced shutdown
- Server restart
- Boot configuration (PXE, USB, CD, etc.)
- Boot override settings

### System Information

- Hardware inventory (CPU, memory, storage, network)
- Firmware version information
- System health status
- Component health monitoring
- Temperature and power monitoring

### TSR Analysis

- Automatic parsing of TSR ZIP files
- Error detection and categorization
- Health assessment with scoring
- Firmware compatibility checking
- Comparative analysis across time periods
- Automated diagnostic workflows

### Security

- Secure credential handling
- SSL/TLS support
- Integration with DAP secret management
- Best practices for credential storage

## Workflow Guides

The skill includes comprehensive workflow guides for common tasks:

1. **Initial Server Setup** - Configure new servers with proper iDRAC settings
2. **Firmware Updates** - Safe firmware update procedures
3. **Troubleshooting** - Hardware issue diagnosis and resolution
4. **Health Monitoring** - Automated health monitoring setup
5. **Disaster Recovery** - Backup and recovery procedures

See `references/workflow-guide.md` for detailed step-by-step instructions.

## Reference Documentation

- **Redfish API**: `references/redfish-api.md` - Complete Redfish API reference
- **racadm CLI**: `references/racadm-cli.md` - Comprehensive racadm command reference
- **TSR Analysis**: `references/tsr-analysis.md` - TSR structure and analysis methods
- **Workflow Guide**: `references/workflow-guide.md` - Step-by-step operational workflows

## Architecture Documentation

The `idrac-architecture/` directory contains comprehensive Dell iDRAC documentation:

- **Documentation Index**: `idrac-architecture/guides/documentation-index.md` - Complete index of available Dell documentation
- **Release Notes**: `idrac-architecture/release-notes/release-notes-index.md` - iDRAC9 Version 7.x release notes tracking
- **Low-Level Design**: `idrac-architecture/lld/` - Technical LLD documents
- **High-Level Design**: `idrac-architecture/hld/` - Architecture HLD documents
- **Specifications**: `idrac-architecture/specs/` - Technical specifications and reference guides

**Note**: Due to Dell's access restrictions, some documentation requires manual download from the Dell support portal with authentication.

## Known Issues Database

The `known-issues/` directory contains documented known issues for Dell iDRAC:

- **Known Issues Index**: `known-issues/known-issues-index.md` - Catalog of known issues by version and component
- **Workarounds**: Documented workarounds for common issues
- **Resolution Tracking**: Track issue resolutions and fixes

## Error Patterns Database

The `patterns/` directory contains error patterns and troubleshooting information:

- **Error Patterns Index**: `patterns/error-patterns-index.md` - Comprehensive error pattern database
- **Pattern Sources**: Patterns sourced from Dell manuals, release notes, and field experience
- **Automated Analysis**: Patterns for use in TSR analysis and automated diagnostics

## Example Scripts

### iDRAC Redfish Client

A Python client for iDRAC Redfish API operations:

```bash
python scripts/idrac_redfish_client.py
```

Features:
- System information retrieval
- Power management operations
- Hardware inventory
- Health monitoring
- Log retrieval
- Firmware updates

### TSR Analyzer

A tool for analyzing Dell Technical Support Reports:

```bash
python scripts/tsr_analyzer.py tsr_report.zip
```

Features:
- System information extraction
- Hardware inventory analysis
- Error detection and categorization
- Health assessment
- Comprehensive reporting
- JSON output for integration

## DAP Blueprint Templates

Example blueprints are provided in `examples/blueprint-templates/`:

- **idrac-power-management.yaml**: Power management operations
- **idrac-power-management-inputs.yaml**: Input definitions
- **idrac-power-management-capabilities.yaml**: Output capabilities

These templates demonstrate how to integrate iDRAC operations with DAP blueprints using the script-plugin skill.

## Best Practices

### Security

1. **Never hardcode credentials** - Use DAP secret management
2. **Use HTTPS** - Always use SSL/TLS for iDRAC connections
3. **Least privilege** - Use appropriate user permissions
4. **Regular updates** - Keep iDRAC firmware updated
5. **Audit access** - Monitor iDRAC access logs

### Operations

1. **Test first** - Test procedures on non-production servers
2. **Backup configuration** - Export configuration before changes
3. **Monitor logs** - Regularly check system event logs
4. **Document changes** - Keep detailed change records
5. **Plan maintenance** - Schedule maintenance windows for updates

### TSR Analysis

1. **Regular collection** - Generate TSRs regularly for baselines
2. **Historical comparison** - Compare TSRs over time to identify trends
3. **Automated analysis** - Implement automated analysis scripts
4. **Proactive monitoring** - Use TSR data for proactive issue detection
5. **Integration** - Integrate with monitoring and alerting systems

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to iDRAC
- Check network connectivity
- Verify IP address and credentials
- Ensure iDRAC firmware supports selected connection method
- Check firewall rules

**Problem**: Redfish API errors
- Verify iDRAC firmware version (2.0.0+ required)
- Check SSL certificate validity
- Ensure proper authentication
- Review API endpoint URLs

### TSR Analysis Issues

**Problem**: TSR parsing fails
- Ensure TSR file is complete and not corrupted
- Check file format (ZIP with XML structure)
- Verify sufficient disk space for extraction
- Check for password-protected TSRs

## Getting Help

For specific iDRAC operations or TSR analysis questions:

1. Load the appropriate reference file from `references/`
2. Check example scripts in `scripts/`
3. Review workflow guides in `references/workflow-guide.md`
4. Consult Dell official documentation for your iDRAC version
5. Use debug mode for troubleshooting

## Requirements

### Python Dependencies

```bash
pip install requests
```

### System Requirements

- Python 3.6+
- Network access to iDRAC interfaces
- Appropriate permissions for server management

### DAP Integration

- DAP with script-plugin skill
- Ansible plugin for blueprint operations
- Appropriate DAP permissions

## Contributing

To extend this skill:

1. Add new reference files to `references/`
2. Create additional example scripts in `scripts/`
3. Develop new blueprint templates in `examples/blueprint-templates/`
4. Add architecture documents to `idrac-architecture/` (lld, hld, guides, specs)
5. Document known issues in `known-issues/`
6. Add error patterns to `patterns/`
7. Update documentation indices when adding new files
8. Update this README with new features
9. Document new workflows in `references/workflow-guide.md`

### Documentation Guidelines

When adding Dell documentation:
1. Update the documentation index in `idrac-architecture/guides/documentation-index.md`
2. Note any access restrictions or authentication requirements
3. Include version information and update dates
4. Cross-reference with related documentation

When adding known issues:
1. Use the template provided in `known-issues/known-issues-index.md`
2. Include severity, affected versions, and workarounds
3. Cross-reference with release notes when applicable
4. Update when resolutions become available

When adding error patterns:
1. Use the template provided in `patterns/error-patterns-index.md`
2. Source information from Dell manuals or release notes
3. Include troubleshooting steps and prevention measures
4. Update TSR analysis patterns if applicable

## License

This skill is provided as-is for Dell server management and TSR analysis.

## Support

For issues specific to:
- **iDRAC operations**: Consult Dell official documentation
- **DAP integration**: Refer to DAP documentation
- **Script errors**: Check Python dependencies and error messages
- **TSR analysis**: Verify TSR file integrity and structure

## Version History

- **v1.1.0**: Added architecture documentation, known issues database, and error patterns
- **v1.0.0**: Initial release with Redfish API, racadm CLI, and TSR analysis support
