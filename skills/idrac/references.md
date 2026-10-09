# iDRAC References

## Connection Methods

| Method | Tool | Use Case |
|--------|------|----------|
| Redfish | `requests`, `redfish` Python client | Modern, full-featured REST API |
| racadm | `racadm` CLI | Local or remote command-line automation |
| SNMP | `pysnmp` | Basic monitoring and alerting |

## Redfish Core Endpoints

Base URL: `https://<idrac-ip>/redfish/v1`

| Operation | Method | Endpoint |
|-----------|--------|----------|
| System info | GET | `/Systems/System.Embedded.1` |
| Power state | GET | `/Systems/System.Embedded.1` (`PowerState`) |
| Power action | POST | `/Systems/System.Embedded.1/Actions/ComputerSystem.Reset` |
| Processors | GET | `/Systems/System.Embedded.1/Processors` |
| Memory | GET | `/Systems/System.Embedded.1/Memory` |
| Storage | GET | `/Systems/System.Embedded.1/Storage` |
| Network | GET | `/Systems/System.Embedded.1/EthernetInterfaces` |
| Firmware inventory | GET | `/UpdateService/FirmwareInventory` |
| Firmware update | POST | `/UpdateService/Actions/UpdateService.SimpleUpdate` |
| SEL logs | GET | `/Systems/System.Embedded.1/LogServices/SEL/Entries` |
| Lifecycle logs | GET | `/Systems/System.Embedded.1/LogServices/LifecycleLog/Entries` |
| Thermal | GET | `/Systems/System.Embedded.1/Thermal` |
| Power metrics | GET | `/Systems/System.Embedded.1/Power` |
| Virtual media | GET/POST | `/Managers/iDRAC.Embedded.1/VirtualMedia` |
| Dell OEM info | GET | `/Systems/System.Embedded.1/Oem/Dell` |
| Dell LC logs | GET | `/Managers/iDRAC.Embedded.1/Oem/Dell/LCLogs` |

### Power Reset Types

- `On`
- `ForceOff`
- `GracefulShutdown`
- `ForceRestart`
- `GracefulRestart`
- `Nmi`

### Boot Override Targets

- `Pxe`
- `Cd`
- `Usb`
- `Hdd`
- `BiosSetup`
- `UefiTarget`

## racadm Quick Reference

### Power

```bash
racadm -r <idrac-ip> -u <user> -p <pass> serveraction powerup
racadm -r <idrac-ip> -u <user> -p <pass> serveraction powerdown
racadm -r <idrac-ip> -u <user> -p <pass> serveraction powercycle
racadm -r <idrac-ip> -u <user> -p <pass> get System.Power
```

### Inventory

```bash
racadm -r <idrac-ip> -u <user> -p <pass> get System
racadm -r <idrac-ip> -u <user> -p <pass> get System.Processor
racadm -r <idrac-ip> -u <user> -p <pass> get System.Memory
racadm -r <idrac-ip> -u <user> -p <pass> get Storage
racadm -r <idrac-ip> -u <user> -p <pass> get System.Firmware
```

### Configuration

```bash
racadm -r <idrac-ip> -u <user> -p <pass> set idrac.IPv4.Address <ip>
racadm -r <idrac-ip> -u <user> -p <pass> set idrac.IPv4.Netmask <mask>
racadm -r <idrac-ip> -u <user> -p <pass> set idrac.IPv4.Gateway <gw>
racadm -r <idrac-ip> -u <user> -p <pass> set idrac.IPv4.DHCPEnable <0|1>
racadm -r <idrac-ip> -u <user> -p <pass> set BIOS.ProcSettings.LogicalProc <Enable|Disable>
racadm -r <idrac-ip> -u <user> -p <pass> get -f config.txt
racadm -r <idrac-ip> -u <user> -p <pass> set -f config.txt
```

### Logs

```bash
racadm -r <idrac-ip> -u <user> -p <pass> getsel -d
racadm -r <idrac-ip> -u <user> -p <pass> getlclog -d
racadm -r <idrac-ip> -u <user> -p <pass> clrsel
```

### Firmware and Jobs

```bash
racadm -r <idrac-ip> -u <user> -p <pass> update -f <firmware.exe> -l <component>
racadm -r <idrac-ip> -u <user> -p <pass> jobqueue view
racadm -r <idrac-ip> -u <user> -p <pass> jobqueue create <job_id> -s <time>
racadm -r <idrac-ip> -u <user> -p <pass> techsupreport export -f <filename>.zip
```

## TSR Structure

A TSR ZIP contains:

```
<tsr>.zip
├── support.xml          # System overview, service tag, model, iDRAC version
├── system.xml           # CPU, memory, storage, network inventory
├── firmware.xml         # Firmware versions
├── sel.xml              # System Event Log
├── lclog.xml            # Lifecycle Controller log
├── storage.xml          # Storage configuration
├── network.xml          # Network configuration
├── bios.xml             # BIOS configuration
├── power.xml            # Power data
├── temperature.xml      # Thermal data
├── fan.xml              # Fan status
└── logs/                # Additional logs
```

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Operation completed |
| 202 | Accepted | Check job status |
| 400 | Bad Request | Validate parameters |
| 401 | Unauthorized | Check credentials |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Verify endpoint |
| 500 | Internal Server Error | Retry or check iDRAC |
| 503 | Service Unavailable | iDRAC busy or in maintenance |

## Security Best Practices

- Always use HTTPS in production.
- Use session or token authentication for multiple operations.
- Store credentials in DAP secrets or environment variables.
- Never commit passwords, TSR files, or private keys.
- Use least-privilege iDRAC users.
- Rotate credentials regularly.

## Troubleshooting

| Symptom | Likely Cause | Action |
|---------|--------------|--------|
| Cannot connect to Redfish | Network or SSL | Verify IP, firewall, firmware, certificate |
| racadm command fails | Credentials or SSH | Verify user, permissions, local vs remote |
| TSR parse fails | Corruption or format | Check ZIP integrity, XML structure, disk space |
| Firmware update hangs | Job queue | View job queue, clear failed jobs, retry |
| Authentication locked | Bad password | Unlock user in iDRAC web UI or racadm |

## External Links

- Dell Redfish Documentation: https://www.dell.com/support/home/en-us/drivers/details?driverId=K3KMH
- Redfish Specification: https://www.dmtf.org/standards/redfish
- Dell racadm Guide: https://www.dell.com/support/manuals/en-us/poweredge-r740/idrac9_4.00.00.00_pub/racadm
