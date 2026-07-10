---
name: idrac
description: >-
  Use when the user says "@idrac", "iDRAC", "Dell server", "TSR report", "Technical Support Report", 
  "server management", "power management", "firmware update", "racadm", "Redfish", 
  "server inventory", "hardware diagnostics", or any request to interact with Dell iDRAC,
  analyze TSR reports, manage Dell server hardware, or perform server operations.
---

# Dell iDRAC Management & TSR Analysis Skill

This skill provides comprehensive workflows and reference material for interacting with Dell iDRAC (Integrated Dell Remote Access Controller) and analyzing Technical Support Reports (TSR). It supports multiple connection methods (Redfish API, racadm CLI, SNMP) and integrates with DAP blueprints for automated server management.

## Reference Files

Detailed reference material is in the `references/` directory:

| File | Content |
|---|---|
| `references/redfish-api.md` | Complete Redfish API reference for Dell servers - endpoints, authentication, operations |
| `references/racadm-cli.md` | racadm command reference - power operations, configuration, firmware updates |
| `references/tsr-analysis.md` | TSR report parsing, error detection, health analysis workflows |
| `references/connection-methods.md` | Connection setup guide for Redfish, racadm, and SNMP |
| `references/security-best-practices.md` | Security considerations for iDRAC access and credential management |

## Example Files

Practical examples in the `examples/` directory:

| File | Content |
|---|---|
| `examples/blueprint-templates/` | DAP blueprint templates for common iDRAC operations |
| `examples/scripts/` | Standalone Python scripts for iDRAC operations |
| `examples/workflows/` | Complete workflow examples for TSR analysis and server management |

---

## Quick Start - Connection Methods

Choose the appropriate connection method based on your environment:

### Redfish API (Recommended)
Modern REST API for Dell PowerEdge servers. Supports all iDRAC features and is the preferred method.

**Setup:**
```python
from redfish import RedfishClient

# Connection setup
client = RedfishClient(
    host="idrac-ip-address",
    username="root",
    password="calvin",
    default_prefix="/redfish/v1"
)
client.login()
```

### racadm CLI
Traditional command-line interface for iDRAC management. Works via SSH or local execution.

**Setup:**
```bash
# Remote execution
racadm -r <idrac-ip> -u root -p calvin command

# Local execution (on the server itself)
racadm command
```

### SNMP
Simple Network Management Protocol for basic monitoring and alerting.

**Setup:**
```python
from pysnmp.hlapi import *

# SNMP query example
errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('idrac-ip', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
)
```

---

## Common Workflows

### Power Management Workflow

**Use when:** User needs to power on/off servers, restart, or control boot settings

**Steps:**
1. Load `references/redfish-api.md` for power management endpoints
2. Choose connection method (Redfish recommended)
3. Implement power operation using appropriate API/CLI
4. Verify power state change
5. Document operation in deployment logs

**Example (Redfish):**
```python
# Power on server
response = client.post('/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
                      {'ResetType': 'On'})

# Power off server
response = client.post('/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
                      {'ResetType': 'ForceOff'})

# Graceful restart
response = client.post('/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
                      {'ResetType': 'GracefulRestart'})
```

---

### System Inventory Workflow

**Use when:** User needs hardware information, firmware versions, component details

**Steps:**
1. Load `references/redfish-api.md` for system inventory endpoints
2. Query system information (model, serial, service tag)
3. Get component inventory (CPU, memory, storage, network)
4. Retrieve firmware versions
5. Format output for user or blueprint capabilities

**Example:**
```python
# Get system information
system_info = client.get('/redfish/v1/Systems/System.Embedded.1')

# Get processor information
processors = client.get('/redfish/v1/Systems/System.Embedded.1/Processors')

# Get memory information
memory = client.get('/redfish/v1/Systems/System.Embedded.1/Memory')

# Get firmware information
firmware = client.get('/redfish/v1/Systems/System.Embedded.1/Firmware')
```

---

### Firmware Update Workflow

**Use when:** User needs to update iDRAC, BIOS, or component firmware

**Steps:**
1. Load `references/redfish-api.md` for firmware update procedures
2. Check current firmware versions
3. Download firmware from Dell support site
4. Upload firmware to iDRAC
5. Schedule or immediately apply update
6. Monitor update progress
7. Verify successful update

**Example:**
```python
# Upload firmware update
with open('firmware.exe', 'rb') as f:
    firmware_data = f.read()

response = client.post('/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate',
                      {
                          'ImageURI': 'http://server/firmware.exe',
                          'Targets': ['/redfish/v1/Systems/System.Embedded.1']
                      })

# Monitor update job
job_id = response.headers['Location']
while True:
    job_status = client.get(job_id)
    if job_status['JobState'] in ['Completed', 'Failed', 'Exception']:
        break
    time.sleep(10)
```

---

### TSR Report Analysis Workflow

**Use when:** User needs to analyze Technical Support Reports for errors, health status, or diagnostics

**Steps:**
1. Load `references/tsr-analysis.md` for TSR structure and analysis methods
2. Obtain TSR report (via iDRAC web UI or racadm)
3. Parse TSR XML/ZIP structure
4. Extract system information and error logs
5. Analyze for critical errors, warnings, and hardware failures
6. Generate health report with recommendations
7. Compare against known issues and best practices

**Example:**
```python
from idrac_tsr_analyzer import TSRAnalyzer

# Analyze TSR report
analyzer = TSRAnalyzer('tsr_report.zip')
report = analyzer.analyze()

# Get critical errors
critical_errors = report.get_critical_errors()

# Get health summary
health_summary = report.get_health_summary()

# Get recommendations
recommendations = report.get_recommendations()
```

---

### Configuration Management Workflow

**Use when:** User needs to modify BIOS settings, network configuration, or user accounts

**Steps:**
1. Load `references/racadm-cli.md` or `references/redfish-api.md` for configuration operations
2. Backup current configuration
3. Apply configuration changes
4. Verify changes applied correctly
5. Document configuration changes

**Example (racadm):**
```bash
# Backup current configuration
racadm -r <idrac-ip> -u root -p calvin get

# Set BIOS attribute
racadm -r <idrac-ip> -u root -p calvin set BIOS.ProcSettings.LogicalProc Enable

# Set network configuration
racadm -r <idrac-ip> -u root -p calvin set NIC.1.IPv4Address 192.168.1.100

# Verify configuration
racadm -r <idrac-ip> -u root -p calvin get BIOS.ProcSettings.LogicalProc
```

---

## DAP Blueprint Integration

This skill integrates with DAP blueprints through custom Python scripts and the script-plugin skill.

### Blueprint Template Structure

```yaml
node_templates:
  idrac_server:
    type: dell.nodes.SoftwareComponent
    properties:
      idrac_host: { get_input: idrac_host }
      idrac_username: { get_secret: { get_input: idrac_username } }
      idrac_password: { get_secret: { get_input: idrac_password } }
      connection_method: { get_input: connection_method }
    interfaces:
      dell.interfaces.lifecycle:
        create:
          implementation: idrac.power_on
          inputs:
            idrac_host: { get_property: [ SELF, idrac_host ] }
            idrac_username: { get_secret: { get_input: idrac_username } }
            idrac_password: { get_secret: { get_input: idrac_password } }
        delete:
          implementation: idrac.power_off
          inputs:
            idrac_host: { get_property: [ SELF, idrac_host ] }
            idrac_username: { get_secret: { get_input: idrac_username } }
            idrac_password: { get_secret: { get_input: idrac_password } }
```

### Custom Script Functions

Create custom Python scripts in the `scripts/` directory for blueprint integration:

```python
# scripts/idrac_operations.py
from redfish import RedfishClient

def power_on(ctx, idrac_host, idrac_username, idrac_password):
    """Power on Dell server via iDRAC"""
    client = RedfishClient(
        host=idrac_host,
        username=idrac_username,
        password=idrac_password
    )
    client.login()
    
    response = client.post('/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
                          {'ResetType': 'On'})
    
    client.logout()
    return response.status == 200
```

---

## Security Best Practices

**CRITICAL:** iDRAC credentials must be handled securely:

1. **Never hardcode credentials** - Always use DAP secret management
2. **Use secret_key inputs** for iDRAC usernames and passwords
3. **Never log credentials** - Avoid logging any sensitive information
4. **Use HTTPS** for Redfish connections
5. **Implement credential rotation** - Regularly update iDRAC passwords
6. **Limit access** - Use least-privilege accounts for automation

**Example secure credential handling:**
```yaml
inputs:
  idrac_username:
    type: secret_key
    display_label: iDRAC Username
    description: Username for iDRAC authentication
    hidden: false
    display:
      group: idrac_credentials
  
  idrac_password:
    type: secret_key
    display_label: iDRAC Password
    description: Password for iDRAC authentication
    hidden: false
    display:
      group: idrac_credentials
```

---

## Troubleshooting

### Common iDRAC Connection Issues

**Problem:** Cannot connect to iDRAC via Redfish
- Check network connectivity and firewall rules
- Verify iDRAC IP address is correct
- Ensure iDRAC firmware supports Redfish (firmware 2.0.0 or later)
- Check if HTTPS certificate is valid (may need to disable SSL verification for testing)

**Problem:** racadm commands fail
- Verify racadm is installed on the management station
- Check SSH connectivity to iDRAC
- Verify credentials and permissions
- Some commands require local execution on the server

**Problem:** TSR analysis fails
- Ensure TSR report is complete and not corrupted
- Check if TSR is in supported format (ZIP with XML structure)
- Verify sufficient disk space for extraction
- Some TSR reports may be password-protected

### Debug Mode

Enable debug logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Redfish client debug
client = RedfishClient(host, username, password, debug=True)
```

---

## Advanced Features

### Batch Operations

Perform operations on multiple servers:

```python
servers = ['server1-ip', 'server2-ip', 'server3-ip']
results = []

for server_ip in servers:
    client = RedfishClient(server_ip, username, password)
    client.login()
    
    # Perform operation
    result = client.post('/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
                        {'ResetType': 'GracefulRestart'})
    results.append((server_ip, result.status))
    
    client.logout()
```

### Scheduled Operations

Schedule firmware updates or maintenance windows:

```python
# Schedule firmware update for specific time
response = client.post('/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/DellManager.ScheduleUpdate',
                      {
                          'StartTime': '2024-01-15T02:00:00Z',
                          'FirmwareURI': 'http://server/firmware.exe'
                      })
```

### Health Monitoring

Continuous monitoring of server health:

```python
def monitor_server_health(client, interval=300):
    """Monitor server health at regular intervals"""
    while True:
        health = client.get('/redfish/v1/Systems/System.Embedded.1/Health')
        
        if health['Status']['Health'] != 'OK':
            alert_admin(health)
        
        time.sleep(interval)
```

---

## Reference Quick Links

- **Redfish API:** `references/redfish-api.md`
- **racadm CLI:** `references/racadm-cli.md`
- **TSR Analysis:** `references/tsr-analysis.md`
- **Connection Setup:** `references/connection-methods.md`
- **Security:** `references/security-best-practices.md`
- **Blueprint Examples:** `examples/blueprint-templates/`
- **Script Examples:** `examples/scripts/`

---

## Getting Help

For specific iDRAC operations or TSR analysis questions:
1. Load the appropriate reference file from `references/`
2. Check example scripts in `examples/`
3. Review Dell official documentation for specific iDRAC versions
4. Use debug mode to troubleshoot connection issues
