# Redfish API Reference for Dell iDRAC

This reference provides detailed information about using the Redfish API for Dell PowerEdge server management through iDRAC.

## Overview

Redfish is a modern RESTful API for server management that provides a standardized interface for hardware management. Dell iDRAC implements Redfish starting from firmware version 2.0.0.

### Base URL Structure

```
https://<idrac-ip>/redfish/v1
```

### Authentication Methods

1. **Basic Authentication** (Simple, but less secure)
```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get(
    'https://idrac-ip/redfish/v1/Systems',
    auth=HTTPBasicAuth('username', 'password'),
    verify=False  # Only for testing
)
```

2. **Session Authentication** (Recommended for multiple operations)
```python
from redfish import RedfishClient

client = RedfishClient(
    host='idrac-ip',
    username='username',
    password='password',
    default_prefix='/redfish/v1'
)
client.login()
# Perform operations
client.logout()
```

3. **Token Authentication** (For long-running sessions)
```python
# Get session token
response = requests.post(
    'https://idrac-ip/redfish/v1/SessionsService/Sessions',
    auth=HTTPBasicAuth('username', 'password'),
    json={'UserName': 'username', 'Password': 'password'},
    verify=False
)

token = response.json()['@odata.id']
# Use token in subsequent requests
headers = {'X-Auth-Token': token}
```

---

## Core Endpoints

### System Information

**Get System Details**
```http
GET /redfish/v1/Systems/System.Embedded.1
```

**Response Structure:**
```json
{
  "@odata.id": "/redfish/v1/Systems/System.Embedded.1",
  "Id": "System.Embedded.1",
  "SystemType": "Physical",
  "Manufacturer": "Dell Inc.",
  "Model": "PowerEdge R740",
  "SerialNumber": "ABC1234",
  "SKU": "SKU12345",
  "PartNumber": "PN12345",
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  "Boot": {
    "BootSourceOverrideEnabled": "Once",
    "BootSourceOverrideTarget": "Pxe"
  }
}
```

**Get All Systems**
```http
GET /redfish/v1/Systems
```

### Power Management

**Get Power State**
```http
GET /redfish/v1/Systems/System.Embedded.1/PowerState
```

**Power Operations**
```http
POST /redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset
Content-Type: application/json

{
  "ResetType": "On"  // Options: On, ForceOff, GracefulShutdown, ForceRestart, GracefulRestart, Nmi
}
```

**Reset Type Options:**
- `On` - Power on the system
- `ForceOff` - Force power off (ungraceful)
- `GracefulShutdown` - Graceful shutdown (OS must support)
- `ForceRestart` - Force restart (ungraceful)
- `GracefulRestart` - Graceful restart
- `Nmi` - Generate non-maskable interrupt

**Python Example:**
```python
def power_on(client):
    response = client.post(
        '/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
        {'ResetType': 'On'}
    )
    return response.status == 200

def power_off(client, force=False):
    reset_type = 'ForceOff' if force else 'GracefulShutdown'
    response = client.post(
        '/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
        {'ResetType': reset_type}
    )
    return response.status == 200

def restart_server(client, force=False):
    reset_type = 'ForceRestart' if force else 'GracefulRestart'
    response = client.post(
        '/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
        {'ResetType': reset_type}
    )
    return response.status == 200
```

### Processor Information

**Get All Processors**
```http
GET /redfish/v1/Systems/System.Embedded.1/Processors
```

**Get Specific Processor**
```http
GET /redfish/v1/Systems/System.Embedded.1/Processors/CPU.Socket.1
```

**Response Structure:**
```json
{
  "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Processors/CPU.Socket.1",
  "Id": "CPU.Socket.1",
  "Manufacturer": "Intel",
  "Model": "Intel(R) Xeon(R) Gold 6130 CPU @ 2.10GHz",
  "ProcessorType": "CPU",
  "TotalCores": 16,
  "TotalThreads": 32,
  "MaxSpeedMHz": 2100,
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  }
}
```

### Memory Information

**Get All Memory Modules**
```http
GET /redfish/v1/Systems/System.Embedded.1/Memory
```

**Get Specific Memory Module**
```http
GET /redfish/v1/Systems/System.Embedded.1/Memory/DIMM.Socket.A1
```

**Response Structure:**
```json
{
  "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Memory/DIMM.Socket.A1",
  "Id": "DIMM.Socket.A1",
  "Manufacturer": "Samsung",
  "CapacityMiB": 16384,
  "MemoryType": "DDR4",
  "SpeedMHz": 2666,
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  }
}
```

### Storage Information

**Get Storage Controllers**
```http
GET /redfish/v1/Systems/System.Embedded.1/Storage
```

**Get Specific Controller**
```http
GET /redfish/v1/Systems/System.Embedded.1/Storage/RAID.Integrated.1-1
```

**Get Drives for Controller**
```http
GET /redfish/v1/Systems/System.Embedded.1/Storage/RAID.Integrated.1-1/Drives
```

**Response Structure:**
```json
{
  "@odata.id": "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.Integrated.1-1/Drives/Disk.Bay.0:Enclosure.Internal.0-1:RAID.Integrated.1-1",
  "Id": "Disk.Bay.0:Enclosure.Internal.0-1:RAID.Integrated.1-1",
  "Manufacturer": "Dell",
  "Model": "PERC H740P",
  "CapacityBytes": 9601971245056,
  "MediaType": "SSD",
  "Protocol": "SAS",
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  }
}
```

### Network Information

**Get Network Interfaces**
```http
GET /redfish/v1/Systems/System.Embedded.1/EthernetInterfaces
```

**Get Specific Interface**
```http
GET /redfish/v1/Systems/System.Embedded.1/EthernetInterfaces/NIC.Embedded.1-1-1
```

**Response Structure:**
```json
{
  "@odata.id": "/redfish/v1/Systems/System.Embedded.1/EthernetInterfaces/NIC.Embedded.1-1-1",
  "Id": "NIC.Embedded.1-1-1",
  "MACAddress": "00:1E:67:4B:7F:8C",
  "SpeedMbps": 10000,
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  "IPv4Addresses": [
    {
      "Address": "192.168.1.100",
      "SubnetMask": "255.255.255.0",
      "Gateway": "192.168.1.1"
    }
  ]
}
```

---

## Firmware Management

### Get Firmware Information

**Get System Firmware**
```http
GET /redfish/v1/Systems/System.Embedded.1/Firmware
```

**Get Specific Component Firmware**
```http
GET /redfish/v1/UpdateService/FirmwareInventory/{component_id}
```

**Response Structure:**
```json
{
  "@odata.id": "/redfish/v1/UpdateService/FirmwareInventory/Bios",
  "Id": "Bios",
  "Name": "BIOS",
  "Version": "2.8.1",
  "ReleaseDate": "2021-03-15T00:00:00Z",
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  }
}
```

### Firmware Updates

**Get Update Service Information**
```http
GET /redfish/v1/UpdateService
```

**Upload and Apply Firmware**
```http
POST /redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate
Content-Type: application/json

{
  "ImageURI": "http://server/firmware.exe",
  "Targets": [
    "/redfish/v1/Systems/System.Embedded.1"
  ]
}
```

**Python Example:**
```python
def update_firmware(client, firmware_url, component_target):
    """Update firmware via Redfish"""
    response = client.post(
        '/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate',
        {
            'ImageURI': firmware_url,
            'Targets': [component_target]
        }
    )
    
    if response.status == 202:
        job_id = response.headers['Location']
        return monitor_update_job(client, job_id)
    return False

def monitor_update_job(client, job_id):
    """Monitor firmware update job progress"""
    while True:
        job = client.get(job_id)
        state = job['JobState']
        
        if state == 'Completed':
            return True
        elif state in ['Failed', 'Exception']:
            print(f"Update failed: {job.get('Message', 'Unknown error')}")
            return False
        
        print(f"Progress: {job.get('PercentComplete', 0)}%")
        time.sleep(10)
```

---

## System Health and Logs

### Get System Health

**Get Overall Health**
```http
GET /redfish/v1/Systems/System.Embedded.1/Health
```

**Response Structure:**
```json
{
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  "OverallHealth": "OK"
}
```

### System Logs

**Get System Event Log (SEL)**
```http
GET /redfish/v1/Systems/System.Embedded.1/LogServices/SEL/Entries
```

**Get Lifecycle Log**
```http
GET /redfish/v1/Systems/System.Embedded.1/LogServices/LifecycleLog/Entries
```

**Response Structure:**
```json
{
  "@odata.id": "/redfish/v1/Systems/System.Embedded.1/LogServices/SEL/Entries",
  "Members": [
    {
      "@odata.id": "/redfish/v1/Systems/System.Embedded.1/LogServices/SEL/Entries/1",
      "Id": "1",
      "Severity": "Warning",
      "Message": "Temperature threshold exceeded",
      "Created": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Python Example:**
```python
def get_system_logs(client, log_type='SEL'):
    """Retrieve system logs"""
    endpoint = f'/redfish/v1/Systems/System.Embedded.1/LogServices/{log_type}/Entries'
    logs = client.get(endpoint)
    
    return logs.get('Members', [])

def analyze_logs(client):
    """Analyze system logs for critical issues"""
    logs = get_system_logs(client)
    critical_issues = []
    
    for log in logs:
        if log.get('Severity') in ['Critical', 'Warning']:
            critical_issues.append({
                'timestamp': log.get('Created'),
                'severity': log.get('Severity'),
                'message': log.get('Message')
            })
    
    return critical_issues
```

---

## Boot Configuration

### Get Boot Settings

**Get Boot Configuration**
```http
GET /redfish/v1/Systems/System.Embedded.1/Boot
```

**Response Structure:**
```json
{
  "BootSourceOverrideEnabled": "Once",
  "BootSourceOverrideTarget": "Pxe",
  "BootSourceOverrideMode": "UEFI",
  "BootOrder": [
    "Boot0000",
    "Boot0001",
    "Boot0002"
  ]
}
```

### Set Boot Override

**Set Boot Override**
```http
PATCH /redfish/v1/Systems/System.Embedded.1
Content-Type: application/json

{
  "Boot": {
    "BootSourceOverrideEnabled": "Once",
    "BootSourceOverrideTarget": "Pxe",
    "BootSourceOverrideMode": "UEFI"
  }
}
```

**Boot Source Options:**
- `Pxe` - Network boot via PXE
- `Cd` - Boot from CD/DVD
- `Usb` - Boot from USB
- `Hdd` - Boot from hard drive
- `BiosSetup` - Boot into BIOS setup
- `UefiTarget` - Boot to specific UEFI target

**Python Example:**
```python
def set_boot_override(client, boot_target, mode='UEFI'):
    """Set boot override for next boot"""
    response = client.patch(
        '/redfish/v1/Systems/System.Embedded.1',
        {
            'Boot': {
                'BootSourceOverrideEnabled': 'Once',
                'BootSourceOverrideTarget': boot_target,
                'BootSourceOverrideMode': mode
            }
        }
    )
    return response.status == 200

def set_pxe_boot(client):
    """Set server to boot from network on next restart"""
    return set_boot_override(client, 'Pxe')

def set_bios_boot(client):
    """Set server to boot into BIOS setup on next restart"""
    return set_boot_override(client, 'BiosSetup')
```

---

## Virtual Media

### Virtual Media Management

**Get Virtual Media Status**
```http
GET /redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia
```

**Mount Virtual Media**
```http
POST /redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/{media_id}/Actions/VirtualMedia.InsertMedia
Content-Type: application/json

{
  "Image": "http://server/iso/image.iso",
  "Inserted": true,
  "WriteProtected": true
}
```

**Eject Virtual Media**
```http
POST /redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/{media_id}/Actions/VirtualMedia.EjectMedia
```

**Python Example:**
```python
def mount_virtual_media(client, media_id, image_url):
    """Mount virtual media ISO"""
    response = client.post(
        f'/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/{media_id}/Actions/VirtualMedia.InsertMedia',
        {
            'Image': image_url,
            'Inserted': True,
            'WriteProtected': True
        }
    )
    return response.status == 200

def eject_virtual_media(client, media_id):
    """Eject virtual media"""
    response = client.post(
        f'/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/{media_id}/Actions/VirtualMedia.EjectMedia'
    )
    return response.status == 200
```

---

## Error Handling

### Common HTTP Status Codes

| Status | Meaning | Action |
|---|---|---|
| 200 | Success | Operation completed successfully |
| 202 | Accepted | Operation accepted, check job status |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication failed |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | iDRAC error |
| 503 | Service Unavailable | iDRAC busy or maintenance mode |

### Error Response Structure

```json
{
  "error": {
    "code": "Base.1.0.GeneralError",
    "message": "A general error has occurred",
    "@Message.ExtendedInfo": [
      {
        "MessageId": "Base.1.0.PropertyValueNotInList",
        "Message": "The property ResetType is not in the list of valid values"
      }
    ]
  }
}
```

### Python Error Handling

```python
def safe_redfish_operation(client, operation, *args, **kwargs):
    """Execute Redfish operation with error handling"""
    try:
        response = operation(*args, **kwargs)
        
        if response.status in [200, 202]:
            return response.json() if response.content else True
        else:
            error_info = response.json()
            print(f"Error {response.status}: {error_info.get('error', {}).get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False
```

---

## Best Practices

1. **Use Session Authentication** for multiple operations
2. **Handle Rate Limiting** - iDRAC may limit request frequency
3. **Check Job Status** - Long operations return job IDs
4. **Validate Responses** - Always check HTTP status codes
5. **Use HTTPS** - Never use HTTP in production
6. **Implement Retry Logic** - Network issues may occur
7. **Cache System Information** - Reduce redundant queries
8. **Monitor Resource Usage** - Avoid overwhelming iDRAC

---

## Dell-Specific Extensions

Dell provides additional OEM extensions beyond standard Redfish:

### Dell OEM Endpoints

**Get Dell OEM Information**
```http
GET /redfish/v1/Systems/System.Embedded.1/Oem/Dell
```

**Get Dell LC Logs**
```http
GET /redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/LCLogs
```

**Get Dell System Information**
```http
GET /redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellSystem
```

**Python Example:**
```python
def get_dell_system_info(client):
    """Get Dell-specific system information"""
    dell_info = client.get('/redfish/v1/Systems/System.Embedded.1/Oem/Dell/DellSystem')
    return dell_info

def get_lc_logs(client):
    """Get Dell Lifecycle Controller logs"""
    logs = client.get('/redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/LCLogs')
    return logs.get('Entries', [])
```

---

## Testing and Debugging

### Test Connection

```python
def test_idrac_connection(host, username, password):
    """Test iDRAC Redfish connection"""
    try:
        client = RedfishClient(host, username, password)
        client.login()
        
        # Simple test - get system info
        system = client.get('/redfish/v1/Systems/System.Embedded.1')
        
        client.logout()
        return True, system.get('Model', 'Unknown')
        
    except Exception as e:
        return False, str(e)
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Create client with debug enabled
client = RedfishClient(
    host='idrac-ip',
    username='username',
    password='password',
    debug=True  # Enables detailed logging
)
```

---

## Reference Links

- **Dell Redfish Documentation:** https://www.dell.com/support/home/en-us/drivers/details?driverId=K3KMH
- **Redfish Specification:** https://www.dmtf.org/standards/redfish
- **iDRAC REST API Guide:** Check Dell support site for your iDRAC version
