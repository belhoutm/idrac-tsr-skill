# iDRAC Examples

## Redfish Python Client

Use `scripts/idrac_redfish_client.py` for quick operations:

```python
from scripts.idrac_redfish_client import IDRACRedfishClient

client = IDRACRedfishClient(
    host='192.168.1.100',
    username='root',
    password='calvin',
    verify_ssl=False
)

# System info
system_info = client.get_system_info()
print(f"Model: {system_info.get('Model')}")
print(f"Power State: {system_info.get('PowerState')}")

# Power operations
client.power_on()
client.power_off(force=False)
client.restart_server(force=False)

# Inventory
processors = client.get_processors()
memory = client.get_memory()
storage = client.get_storage()

# Logs
sel_entries = client.get_system_logs('SEL')
```

## racadm CLI

```bash
# Power management
racadm -r 192.168.1.100 -u root -p calvin serveraction powerup
racadm -r 192.168.1.100 -u root -p calvin serveraction powerdown
racadm -r 192.168.1.100 -u root -p calvin serveraction powercycle

# Inventory
racadm -r 192.168.1.100 -u root -p calvin get System
racadm -r 192.168.1.100 -u root -p calvin get System.Processor
racadm -r 192.168.1.100 -u root -p calvin get System.Memory
racadm -r 192.168.1.100 -u root -p calvin get Storage

# Logs
racadm -r 192.168.1.100 -u root -p calvin getsel -d
racadm -r 192.168.1.100 -u root -p calvin getlclog -d

# TSR collection
racadm -r 192.168.1.100 -u root -p calvin techsupreport export -f tsr_$(date +%Y%m%d).zip
```

## TSR Analysis

Use `scripts/tsr_analyzer.py`:

```bash
python scripts/tsr_analyzer.py TSR<ServiceTag>_<timestamp>.zip
```

The script extracts the TSR ZIP, parses `support.xml`, `system.xml`, `sel.xml`, `firmware.xml`, and produces a JSON report with:

- System info
- Hardware inventory
- Error analysis (critical/warning/info)
- Health assessment and score
- Recommendations

## DAP Blueprint Template

The full templates are in `examples/blueprint-templates/`:

- `idrac-power-management.yaml`
- `idrac-power-management-inputs.yaml`
- `idrac-power-management-capabilities.yaml`

Key points:

- Use `secret_key` inputs for `idrac_username` and `idrac_password`.
- Use `get_secret: { get_input: idrac_username }` to resolve credentials in node properties.
- Keep node lifecycle operations idempotent and use `get_attribute` for capabilities.

Example `inputs.yaml` snippet:

```yaml
inputs:
  idrac_host:
    type: string
    display_label: iDRAC Host
    description: IP address or hostname of the iDRAC interface
    hidden: false
    constraints:
      - pattern: '^([0-9]{1,3}\.){3}[0-9]{1,3}$|^[a-zA-Z0-9\-\.]+$'
        error_message: Must be a valid IP address or hostname

  idrac_username:
    type: secret_key
    display_label: iDRAC Username
    description: Username for iDRAC authentication
    hidden: false

  idrac_password:
    type: secret_key
    display_label: iDRAC Password
    description: Password for iDRAC authentication
    hidden: false

  connection_method:
    type: string
    display_label: Connection Method
    default: redfish
    hidden: false
    constraints:
      - valid_values: [redfish, racadm, snmp]
        error_message: Must be one of redfish, racadm, snmp
```

## SNMP Basic Monitoring

```python
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('idrac-ip', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
)
```
