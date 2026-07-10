---
name: tsr-analysis
description: >-
  Use when the user says "@tsr", "@tsr-analysis", "TSR analysis", "Technical Support Report analysis",
  "server log analysis", "hardware failure diagnosis", "deployment failure analysis",
  or any request to analyze Dell TSR logs, diagnose hardware issues, or investigate system failures.
---

# TSR Analysis Skill

## Overview

This skill provides comprehensive analysis capabilities for Dell Technical Support Report (TSR) logs, which contain detailed system configuration, hardware state, iDRAC logs, and lifecycle events for Dell PowerEdge servers. Use this skill when analyzing server hardware issues, deployment failures, or system diagnostics.

## TSR Package Structure

TSR logs are delivered as `.zip` files containing nested structure:

```
TSR<ServiceTag>_<timestamp>.zip
└── TSR<ServiceTag>_<timestamp>.pl.zip
    └── tsr/
        ├── hardware/
        │   ├── idracstateinfo/
        │   │   ├── iDRACStateInfo.txt
        │   │   ├── PCIBIB.DAT
        │   │   ├── avc.log
        │   │   ├── cpld-dump.log
        │   │   └── iDRACFirstPowerOnTime.txt
        │   ├── sysinfo/
        │   │   ├── inventory/
        │   │   │   ├── sysinfo_CIM_BIOSAttribute.xml
        │   │   │   ├── sysinfo_CIM_Sensor.xml
        │   │   │   ├── sysinfo_DCIM_View.xml
        │   │   │   └── sysinfo_DCIM_SoftwareIdentity.xml
        │   │   └── lcfiles/
        │   │       ├── curr_lclog.xml
        │   │       ├── lclog_0.xml.gz
        │   │       └── debuglog-1.json
        │   ├── memory/
        │   ├── pci-tree/
        │   ├── psu/
        │   └── spd/
        ├── dbglog/logs/
        │   ├── idraclogs
        │   ├── idraclogs.1
        │   ├── idraclogs.persistent
        │   ├── iDRACDebug.txt
        │   ├── messages
        │   ├── bop.log
        │   ├── ipmcilog
        │   ├── sidebandlog
        │   └── bootcapture_*.rfb.zip
        ├── mut/
        │   ├── mut_day_report.xml
        │   ├── mut_week_report.xml
        │   ├── mut_month_report.xml
        │   └── mut_year_report_2026.xml
        ├── idracsdk/
        │   └── idracsdk.txt
        ├── metadata.json
        └── viewer.html
```

## Key Analysis Areas

### 1. System Metadata (metadata.json)

**Purpose**: Quick system identification and basic configuration

**Key Fields**:
- `Model`: Server model (e.g., PowerEdge R760)
- `ServiceTag`: Unique system identifier
- `FirmwareVersion`: iDRAC firmware version
- `HostName`: System hostname
- `CollectionDateTime`: When TSR was collected
- `System Generation`: Hardware generation (e.g., 16G Monolithic)

**Analysis Checklist**:
- [ ] Verify service tag matches expected system
- [ ] Check firmware version for known issues
- [ ] Validate hostname is properly configured (not incomplete like "esxi3.")
- [ ] Compare collection time with issue timeframe
- [ ] Check system generation for compatibility

### 2. iDRAC State Information (hardware/idracstateinfo/)

**iDRACStateInfo.txt** - System runtime state and network configuration

**Key Sections**:
- System uptime and load average
- Memory usage and swap status
- Network interface statistics
- Active TCP connections
- Process list

**Analysis Checklist**:
- [ ] Check uptime - short uptime may indicate recent crashes/reboots
- [ ] Review load average - high load (>15) indicates system stress
- [ ] Verify network configuration (IP, gateway, DNS)
- [ ] Check for unusual network connections
- [ ] Review memory availability

**PCIBIB.DAT** - PCI device inventory and configuration

**Analysis Checklist**:
- [ ] Verify all expected devices are present
- [ ] Check for PCI communication errors
- [ ] Compare device count between systems

### 3. Hardware Inventory (hardware/sysinfo/inventory/)

**sysinfo_CIM_BIOSAttribute.xml** - BIOS and firmware configuration

**Key Information**:
- BIOS version and settings
- Processor information
- Memory configuration
- Boot settings
- Secure boot status

**Analysis Checklist**:
- [ ] Verify BIOS version is current
- [ ] Check secure boot status (Disabled/Enabled)
- [ ] Review boot order configuration
- [ ] Check for BIOS configuration mismatches

**sysinfo_CIM_Sensor.xml** - Hardware sensor readings

**Key Information**:
- Temperature sensors
- Voltage readings
- Fan speeds
- Power supply status

**Analysis Checklist**:
- [ ] Check for temperature warnings
- [ ] Verify voltage readings are within spec
- [ ] Review fan speeds for anomalies
- [ ] Check power supply status codes

**sysinfo_DCIM_View.xml** - Complete system configuration view

**Analysis Checklist**:
- [ ] Review complete hardware inventory
- [ ] Check NIC configurations and mappings
- [ ] Verify storage controller configuration
- [ ] Compare with expected configuration

### 4. Lifecycle Log (hardware/sysinfo/lcfiles/)

**curr_lclog.xml** - System event log (Lifecycle Controller)

**Key Event Categories**:
- System Health - Hardware events, errors, warnings
- Audit - User logins, configuration changes
- Configuration - BIOS, iDRAC, system settings changes
- Storage - RAID controller, virtual disk events
- Power - Power supply, power state changes

**Critical Event Patterns**:

**Power Events**:
```
MessageID: SYS1000 - System is turning on
MessageID: SYS1001 - System is turning off
MessageID: SYS1003 - System CPU Resetting
MessageID: SYS1005 - Server power action initiated
```

**Secure Boot Events**:
```
MessageID: UEFI0074 - Secure Boot policy modified
```

**Power Supply Events**:
```
MessageID: PSU0800 - Power supply status changes
MessageID: PSU0802 - Power supply redundancy policy
```

**Analysis Checklist**:
- [ ] Review events around failure timeframe
- [ ] Check for repeated power cycles
- [ ] Identify secure boot policy changes
- [ ] Review power supply status changes
- [ ] Look for hardware error messages
- [ ] Check for user-initiated configuration changes

### 5. iDRAC Debug Logs (dbglog/logs/)

**idraclogs** - Real-time iDRAC operational logs

**Critical Error Patterns**:

**I2C Communication Failures**:
```
I2C_Master_Write_Read: I2CMstWrMstRd(Bus:X/YY, Command:ZZ) failed - rc 9
PMBusVR_req_blockAPI: VR cmd failed for bus 0x9 address 0xe0
```
**Impact**: Indicates hardware communication issues with voltage regulators, potential motherboard or VR failure.

**MCTP Discovery Issues**:
```
PUPOPMCTPClientCallback: Error in reading GPU PCI Info
PUPOPMCTPClientCallback: No Valid GPU device found
```
**Impact**: GPU inventory or PCIe communication issues.

**Analysis Checklist**:
- [ ] Search for I2C/VR communication failures
- [ ] Check for repeated error patterns
- [ ] Review timestamps around failure events
- [ ] Identify hardware communication issues
- [ ] Compare error rates between systems

**iDRACDebug.txt** - Comprehensive iDRAC dump

**Key Sections**:
- General System/RAC Information
- Network Interface Statistics
- Active Internet connections
- System Information
- Embedded NIC MAC Addresses

**Analysis Checklist**:
- [ ] Verify network configuration matches expectations
- [ ] Check for unusual network connections
- [ ] Review NIC MAC addresses
- [ ] Compare with other systems in cluster

### 6. System Messages (dbglog/logs/messages*)

**Linux system messages** - Kernel and system service logs

**Analysis Checklist**:
- [ ] Check for kernel errors
- [ ] Review filesystem issues
- [ ] Look for service failures
- [ ] Check for network-related errors

### 7. MUT Reports (mut/)

**Management Utility Reports** - System health and performance over time

**Files**:
- `mut_day_report.xml` - Daily system health summary
- `mut_week_report.xml` - Weekly trends
- `mut_month_report.xml` - Monthly analysis
- `mut_year_report_2026.xml` - Yearly overview

**Analysis Checklist**:
- [ ] Review trends in system health
- [ ] Check for recurring issues
- [ ] Identify performance degradation
- [ ] Compare with baseline metrics

## Common Analysis Patterns

### Deployment Failure Analysis

When analyzing deployment failures (e.g., ESXi reimage failures):

1. **Check System Stability**:
   - Review uptime and load average
   - Look for recent power cycles in lifecycle log
   - Check for I2C/VR communication failures

2. **Verify Network Configuration**:
   - Confirm iDRAC IP is accessible
   - Check network interface statistics
   - Verify hostname is properly configured

3. **Review Hardware Health**:
   - Check sensor readings for temperature/voltage issues
   - Review power supply status
   - Look for hardware error messages

4. **Analyze Timeline**:
   - Correlate lifecycle events with deployment timeline
   - Check for configuration changes during deployment
   - Review user access logs

### Hardware Issue Diagnosis

When diagnosing hardware problems:

1. **I2C/VR Communication Failures**:
   - Search idraclogs for "I2C_Master_Write_Read failed"
   - Check for "PMBusVR_req_blockAPI" errors
   - Review bus/address patterns (typically Bus 9, addresses 0xE0, 0xE4)
   - Impact: May cause system instability, power issues, or deployment failures

2. **Power Supply Issues**:
   - Review PSU status codes in lifecycle log
   - Check for redundancy policy changes
   - Look for input power fluctuations

3. **Memory Issues**:
   - Review memory configuration in BIOS attributes
   - Check for ECC errors in system messages
   - Verify memory capacity matches expectations

### System Comparison Analysis

When comparing working vs. problem systems:

1. **Configuration Comparison**:
   - Compare firmware versions
   - Compare BIOS settings
   - Compare network configurations
   - Compare hardware inventory

2. **Operational Comparison**:
   - Compare uptime and load averages
   - Compare error rates in logs
   - Compare network connection patterns
   - Compare sensor readings

3. **Timeline Comparison**:
   - Compare event sequences around failure
   - Compare configuration change history
   - Compare user access patterns

## Critical Failure Indicators

### High-Priority Issues

1. **I2C/VR Communication Failures**
   - Pattern: Repeated "I2C_Master_Write_Read failed - rc 9" errors
   - Severity: Critical - indicates hardware failure
   - Action: Hardware replacement likely required

2. **Repeated Power Cycles**
   - Pattern: Multiple power-on/off events in short timeframe
   - Severity: High - indicates system instability
   - Action: Investigate power supply, motherboard, or environmental issues

3. **Incomplete Hostname Configuration**
   - Pattern: Hostname like "esxi3." (trailing dot)
   - Severity: Medium - causes DNS/resolution issues
   - Action: Correct hostname configuration

4. **High Load Average with Short Uptime**
   - Pattern: Load >15 with uptime <1 hour
   - Severity: High - indicates system stress or hardware issues
   - Action: Investigate resource usage, hardware health

5. **Secure Boot Policy Modifications**
   - Pattern: Multiple UEFI0074 events
   - Severity: Medium - may cause boot issues
   - Action: Verify secure boot configuration is stable

## Analysis Workflow

### Step 1: Extract and Validate TSR
```bash
# Extract outer zip
unzip TSR<ServiceTag>_<timestamp>.zip -d <service_tag>_logs

# Extract inner zip
unzip <service_tag>_logs/TSR<ServiceTag>_<timestamp>.pl.zip -d <service_tag>_logs/extracted
```

### Step 2: Review Metadata
```bash
# Check metadata.json
cat <service_tag>_logs/extracted/tsr/metadata.json
```

### Step 3: Analyze System State
```bash
# Review iDRAC state
cat <service_tag>_logs/extracted/tsr/hardware/idracstateinfo/iDRACStateInfo.txt

# Check iDRAC debug
cat <service_tag>_logs/extracted/tsr/dbglog/logs/iDRACDebug.txt
```

### Step 4: Search for Critical Errors
```bash
# Search for I2C failures
grep -i "I2C_Master_Write_Read.*failed" <service_tag>_logs/extracted/tsr/dbglog/logs/idraclogs

# Search for VR errors
grep -i "PMBusVR.*failed" <service_tag>_logs/extracted/tsr/dbglog/logs/idraclogs

# Search for power events
grep -i "SYS10" <service_tag>_logs/extracted/tsr/hardware/sysinfo/lcfiles/curr_lclog.xml
```

### Step 5: Review Lifecycle Events
```bash
# Review recent lifecycle events
tail -100 <service_tag>_logs/extracted/tsr/hardware/sysinfo/lcfiles/curr_lclog.xml
```

### Step 6: Compare Systems
```bash
# Compare configurations between systems
diff <system1>_logs/extracted/tsr/metadata.json <system2>_logs/extracted/tsr/metadata.json
```

## Reporting Template

### TSR Analysis Report

**System Information**:
- Service Tag: [SERVICE_TAG]
- Model: [MODEL]
- Firmware: [FIRMWARE_VERSION]
- Hostname: [HOSTNAME]
- Collection Time: [COLLECTION_TIME]
- Uptime: [UPTIME]
- Load Average: [LOAD_AVG]

**Critical Findings**:
1. [Finding 1]
   - Severity: [Critical/High/Medium/Low]
   - Evidence: [Log excerpts]
   - Impact: [Description]

2. [Finding 2]
   - Severity: [Critical/High/Medium/Low]
   - Evidence: [Log excerpts]
   - Impact: [Description]

**Configuration Analysis**:
- Network: [IP, Gateway, DNS]
- Hardware: [Key components]
- BIOS: [Version, secure boot status]
- NICs: [Count and types]

**Timeline Analysis**:
- [Event 1]: [Timestamp] - [Description]
- [Event 2]: [Timestamp] - [Description]

**Recommendations**:
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

**Next Steps**:
- [Action item 1]
- [Action item 2]

## Known Issues and Solutions

### Issue: I2C/VR Communication Failures
**Symptoms**: Repeated I2C communication errors with voltage regulators
**Root Cause**: Hardware failure on motherboard or voltage regulators
**Solution**: Replace motherboard or affected VR components
**Workaround**: None - hardware replacement required

### Issue: Incomplete Hostname
**Symptoms**: Hostname ends with dot (e.g., "esxi3.")
**Root Cause**: Configuration error during setup
**Solution**: Correct hostname via iDRAC or OS
**Command**: `racadm set system.hostname <correct_hostname>`

### Issue: High Load After Reboot
**Symptoms**: Load average >15 with short uptime
**Root Cause**: System instability or hardware issues
**Solution**: Investigate hardware health, check for failed components
**Diagnostic**: Run hardware diagnostics, review sensor data

## Integration with Other Skills

This skill can be used alongside:
- **dpc-blueprint-analysis**: When analyzing DPC deployment failures
- **k8s-debugging**: When investigating Kubernetes node issues
- **ece-debugging**: When diagnosing endpoint connectivity issues

## References

- Dell PowerEdge Server Documentation
- iDRAC User Guide
- Lifecycle Controller Documentation
- Dell Technical Support Guide
