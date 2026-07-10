# racadm CLI Reference for Dell iDRAC

This reference provides comprehensive information about using the racadm command-line interface for Dell iDRAC management.

## Overview

racadm (Remote Access Controller Admin) is Dell's command-line tool for managing iDRAC. It can be used locally on the server or remotely via SSH.

### Basic Syntax

```bash
# Remote execution
racadm -r <idrac-ip> -u <username> -p <password> <command>

# Local execution (on the server)
racadm <command>

# Using configuration file
racadm -r <idrac-ip> -u <username> -p <password> -f <config-file>
```

### Authentication Options

| Option | Description |
|---|---|
| `-r <ip>` | Remote iDRAC IP address |
| `-u <username>` | iDRAC username |
| `-p <password>` | iDRAC password |
| `-c <certificate>` | Use SSL certificate for authentication |
| `-s` | Use SSL/TLS connection |

---

## Power Management Commands

### Power Operations

**Power On Server**
```bash
racadm -r <idrac-ip> -u root -p calvin serveraction powerup
```

**Power Off Server**
```bash
racadm -r <idrac-ip> -u root -p calvin serveraction powerdown
```

**Graceful Shutdown**
```bash
racadm -r <idrac-ip> -u root -p calvin serveraction graceshutdown
```

**Power Cycle**
```bash
racadm -r <idrac-ip> -u root -p calvin serveraction powercycle
```

**Hard Reset**
```bash
racadm -r <idrac-ip> -u root -p calvin serveraction hardreset
```

**Reboot**
```bash
racadm -r <idrac-ip> -u root -p calvin serveraction powercycle
```

### Power Status

**Get Power State**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Power
```

**Get Power Consumption**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Power.Consumption
```

**Set Power Cap**
```bash
racadm -r <idrac-ip> -u root -p calvin set System.Power.PowerCap 500
```

### Next Boot Settings

**Set PXE Boot**
```bash
racadm -r <idrac-ip> -u root -p calvin set BootSeq.1.BootSeqEnumeration PXE
```

**Set BIOS Boot**
```bash
racadm -r <idrac-ip> -u root -p calvin set BootSeq.1.BootSeqEnumeration BIOS
```

**Set Boot Once**
```bash
racadm -r <idrac-ip> -u root -p calvin bootseq
racadm -r <idrac-ip> -u root -p calvin set Boot.Once PXE
```

---

## System Information Commands

### Get System Information

**Get System Overview**
```bash
racadm -r <idrac-ip> -u root -p calvin get System
```

**Get Service Tag**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.ServiceTag
```

**Get Model Information**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Model
```

**Get BIOS Version**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.BIOSVersion
```

**Get iDRAC Version**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.IDRACVersion
```

### Processor Information

**Get Processor Information**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Processor
```

**Get CPU Details**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Processor.CPU1
```

**Get CPU Temperature**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Temperature.CPU1
```

### Memory Information

**Get Memory Information**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Memory
```

**Get DIMM Details**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Memory.DIMM.Socket.A1
```

**Get Memory Health**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Memory.Health
```

### Storage Information

**Get Storage Controllers**
```bash
racadm -r <idrac-ip> -u root -p calvin get Storage
```

**Get RAID Controller Info**
```bash
racadm -r <idrac-ip> -u root -p calvin get Storage.RAID.Integrated.1-1
```

**Get Virtual Disks**
```bash
racadm -r <idrac-ip> -u root -p calvin get Storage.RAID.Integrated.1-1.VirtualDisk
```

**Get Physical Disks**
```bash
racadm -r <idrac-ip> -u root -p calvin get Storage.RAID.Integrated.1-1.PhysicalDisk
```

### Network Information

**Get Network Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin get NIC
```

**Get iDRAC IP**
```bash
racadm -r <idrac-ip> -u root -p calvin get NIC.IPv4Address
```

**Get MAC Address**
```bash
racadm -r <idrac-ip> -u root -p calvin get NIC.MACAddress
```

---

## Configuration Commands

### BIOS Configuration

**Get BIOS Settings**
```bash
racadm -r <idrac-ip> -u root -p calvin get BIOS
```

**Get Specific BIOS Setting**
```bash
racadm -r <idrac-ip> -u root -p calvin get BIOS.ProcSettings.LogicalProc
```

**Set BIOS Setting**
```bash
racadm -r <idrac-ip> -u root -p calvin set BIOS.ProcSettings.LogicalProc Enable
```

**Enable Hyper-Threading**
```bash
racadm -r <idrac-ip> -u root -p calvin set BIOS.ProcSettings.LogicalProc Enable
```

**Set Boot Mode**
```bash
racadm -r <idrac-ip> -u root -p calvin set BIOS.BootSettings.BootMode Uefi
```

**Save BIOS Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin jobqueue create BIOS.Setup.1-1
```

### iDRAC Configuration

**Get iDRAC Settings**
```bash
racadm -r <idrac-ip> -u root -p calvin get idrac
```

**Get iDRAC Network Settings**
```bash
racadm -r <idrac-ip> -u root -p calvin get idrac.Network
```

**Set iDRAC IP Address**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.Address 192.168.1.100
```

**Set iDRAC Subnet Mask**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.Netmask 255.255.255.0
```

**Set iDRAC Gateway**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.Gateway 192.168.1.1
```

**Enable iDRAC DHCP**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.DHCPEnable 1
```

### User Management

**Get User List**
```bash
racadm -r <idrac-ip> -u root -p calvin get idrac.Users
```

**Create User**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.2.UserName newuser
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.2.Password newpassword
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.2.Enable 1
```

**Delete User**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.2.UserName ""
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.2.Enable 0
```

**Set User Permissions**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.2.Privilege 0x000001ff
```

### Time and NTP Configuration

**Get Time Settings**
```bash
racadm -r <idrac-ip> -u root -p calvin get idrac.Time
```

**Set iDRAC Time**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.Time.TimeZone America/New_York
```

**Configure NTP**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.NTPConfigGroup.NTP1 192.168.1.10
racadm -r <idrac-ip> -u root -p calvin set idrac.NTPConfigGroup.NTPEnable 1
```

---

## Firmware Update Commands

### Firmware Information

**Get Firmware Versions**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Firmware
```

**Get BIOS Version**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.BIOSVersion
```

**Get iDRAC Firmware Version**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.IDRACVersion
```

### Firmware Updates

**Update iDRAC Firmware**
```bash
racadm -r <idrac-ip> -u root -p calvin update -f <firmware-file.exe>
```

**Update BIOS**
```bash
racadm -r <idrac-ip> -u root -p calvin update -f <bios-firmware.exe> -l BIOS
```

**Schedule Firmware Update**
```bash
racadm -r <idrac-ip> -u root -p calvin jobqueue create BIOS.Setup.1-1 -s <start-time>
```

**Check Update Status**
```bash
racadm -r <idrac-ip> -u root -p calvin jobqueue view
```

---

## Logging and Monitoring Commands

### System Event Log (SEL)

**Get SEL Entries**
```bash
racadm -r <idrac-ip> -u root -p calvin getsel
```

**Get SEL with Details**
```bash
racadm -r <idrac-ip> -u root -p calvin getsel -d
```

**Clear SEL**
```bash
racadm -r <idrac-ip> -u root -p calvin clrsel
```

**Export SEL to File**
```bash
racadm -r <idrac-ip> -u root -p calvin getsel -f sel_output.txt
```

### Lifecycle Log

**Get Lifecycle Log**
```bash
racadm -r <idrac-ip> -u root -p calvin getlclog
```

**Get LC Log Statistics**
```bash
racadm -r <idrac-ip> -u root -p calvin getlclog -s
```

### Temperature Monitoring

**Get Temperature Readings**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Temperature
```

**Get CPU Temperature**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Temperature.CPU1
```

**Get Ambient Temperature**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Temperature.InletTemp
```

### Fan Monitoring

**Get Fan Status**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Fan
```

**Get Fan RPM**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Fan.Fan1
```

### Power Monitoring

**Get Power Consumption**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Power.Consumption
```

**Get Power Supply Status**
```bash
racadm -r <idrac-ip> -u root -p calvin get System.Power.Supply
```

---

## Virtual Media Commands

### Virtual Media Management

**Get Virtual Media Status**
```bash
racadm -r <idrac-ip> -u root -p calvin get vmdisplay
```

**Mount Virtual Media**
```bash
racadm -r <idrac-ip> -u root -p calvin remoteimage -c -u <username> -p <password> -l <iso-url>
```

**Unmount Virtual Media**
```bash
racadm -r <idrac-ip> -u root -p calvin remoteimage -d
```

### Console Redirection

**Start Console Redirection**
```bash
racadm -r <idrac-ip> -u root -p calvin console -d
```

**Stop Console Redirection**
```bash
racadm -r <idrac-ip> -u root -p calvin console -k
```

---

## Configuration Import/Export

### Export Configuration

**Export All Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin get -f config.txt
```

**Export BIOS Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin get BIOS -f bios_config.txt
```

**Export iDRAC Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin get idrac -f idrac_config.txt
```

### Import Configuration

**Import Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin set -f config.txt
```

**Import BIOS Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin set BIOS -f bios_config.txt
```

**Import iDRAC Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac -f idrac_config.txt
```

---

## Job Queue Management

### Job Queue Operations

**View Job Queue**
```bash
racadm -r <idrac-ip> -u root -p calvin jobqueue view
```

**Create Job**
```bash
racadm -r <idrac-ip> -u root -p calvin jobqueue create BIOS.Setup.1-1
```

**Delete Job**
```bash
racadm -r <idrac-ip> -u root -p calvin jobqueue delete <job-id>
```

**Clear Job Queue**
```bash
racadm -r <idrac-ip> -u root -p calvin jobqueue delete --all
```

### Job Scheduling

**Schedule BIOS Update**
```bash
racadm -r <idrac-ip> -u root -p calvin jobqueue create BIOS.Setup.1-1 -s "2024-01-15T02:00:00"
```

**Schedule Reboot**
```bash
racadm -r <idrac-ip> -u root -p calvin jobqueue create System.Embedded.1 -s "2024-01-15T03:00:00"
```

---

## Certificate Management

### SSL Certificate Management

**Get Certificate Information**
```bash
racadm -r <idrac-ip> -u root -p calvin get idrac.Security.Certificates
```

**Generate CSR**
```bash
racadm -r <idrac-ip> -u root -p calvin sslcsr -g -f csr.txt
```

**Import SSL Certificate**
```bash
racadm -r <idrac-ip> -u root -p calvin sslcertupload -t 1 -f certificate.crt
```

**Delete Certificate**
```bash
racadm -r <idrac-ip> -u root -p calvin sslcertdelete -t 1
```

---

## Network Configuration

### Network Settings

**Get Network Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin get idrac.Network
```

**Set Static IP**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.Address 192.168.1.100
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.Netmask 255.255.255.0
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.Gateway 192.168.1.1
```

**Enable DHCP**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.DHCPEnable 1
```

**Disable DHCP**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.DHCPEnable 0
```

### DNS Configuration

**Set DNS Servers**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.Network.DNS1 192.168.1.10
racadm -r <idrac-ip> -u root -p calvin set idrac.Network.DNS2 192.168.1.11
```

**Get DNS Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin get idrac.Network.DNS
```

---

## Advanced Commands

### RAID Configuration

**Get RAID Configuration**
```bash
racadm -r <idrac-ip> -u root -p calvin get Storage.RAID.Integrated.1-1
```

**Create Virtual Disk**
```bash
racadm -r <idrac-ip> -u root -p calvin storage createvd -rl 1 -pdisklist Disk.Bay.0:Enclosure.Internal.0-1:RAID.Integrated.1-1,Disk.Bay.1:Enclosure.Internal.0-1:RAID.Integrated.1-1
```

**Delete Virtual Disk**
```bash
racadm -r <idrac-ip> -u root -p calvin storage deletevd VirtualDisk.0:RAID.Integrated.1-1
```

**Get Physical Disk Information**
```bash
racadm -r <idrac-ip> -u root -p calvin storage getpdisk
```

### Sensor Monitoring

**Get All Sensors**
```bash
racadm -r <idrac-ip> -u root -p calvin sensor
```

**Get Sensor Details**
```bash
racadm -r <idrac-ip> -u root -p calvin sensor -d
```

**Monitor Specific Sensor**
```bash
racadm -r <idrac-ip> -u root -p calvin sensor -s CPU1_Temp
```

### Diagnostic Commands

**Run Diagnostics**
```bash
racadm -r <idrac-ip> -u root -p calvin diagnostics run
```

**Get Diagnostic Results**
```bash
racadm -r <idrac-ip> -u root -p calvin diagnostics results
```

**Get System Inventory**
```bash
racadm -r <idrac-ip> -u root -p calvin inventory
```

---

## Scripting and Automation

### Batch Operations

**Execute Multiple Commands**
```bash
#!/bin/bash
# power_on_and_check.sh
racadm -r $IDRAC_IP -u $USER -p $PASS serveraction powerup
sleep 30
racadm -r $IDRAC_IP -u $USER -p $PASS get System.Power
```

**Loop Through Multiple Servers**
```bash
#!/bin/bash
servers=("server1" "server2" "server3")
for server in "${servers[@]}"; do
    racadm -r $server -u root -p calvin get System.Model
done
```

### Error Handling

**Check Command Exit Status**
```bash
#!/bin/bash
racadm -r $IDRAC_IP -u $USER -p $PASS serveraction powerup
if [ $? -eq 0 ]; then
    echo "Server powered on successfully"
else
    echo "Failed to power on server"
fi
```

**Validate Configuration**
```bash
#!/bin/bash
racadm -r $IDRAC_IP -u $USER -p $PASS get System.Power | grep "PowerState=On"
if [ $? -eq 0 ]; then
    echo "Server is powered on"
else
    echo "Server is powered off"
fi
```

---

## Troubleshooting

### Common Issues

**Connection Refused**
```bash
# Check network connectivity
ping <idrac-ip>

# Check iDRAC service status
racadm -r <idrac-ip> -u root -p calvin get idrac.ServiceStatus
```

**Authentication Failed**
```bash
# Verify credentials
racadm -r <idrac-ip> -u root -p calvin get idrac.Users.1.UserName

# Check if account is locked
racadm -r <idrac-ip> -u root -p calvin get idrac.Users.1.Enable
```

**Command Not Supported**
```bash
# Check iDRAC firmware version
racadm -r <idrac-ip> -u root -p calvin get System.IDRACVersion

# Update iDRAC firmware if needed
racadm -r <idrac-ip> -u root -p calvin update -f <firmware-file.exe>
```

### Debug Mode

**Enable Debug Logging**
```bash
racadm -r <idrac-ip> -u root -p calvin set idrac.Debug.Enable 1
```

**View Debug Logs**
```bash
racadm -r <idrac-ip> -u root -p calvin get idrac.Debug.Log
```

---

## Best Practices

1. **Use SSH Keys** - More secure than password authentication
2. **Enable SSL/TLS** - Always use encrypted connections
3. **Schedule Maintenance** - Use job queue for non-critical updates
4. **Backup Configuration** - Export configuration before making changes
5. **Monitor Logs** - Regularly check SEL and lifecycle logs
6. **Test Commands** - Validate commands on non-production servers first
7. **Use Configuration Files** - For complex configurations, use import/export
8. **Document Changes** - Keep track of configuration modifications

---

## Reference Links

- **Dell racadm Guide:** https://www.dell.com/support/manuals/en-us/poweredge-r740/idrac9_4.00.00.00_pub/racadm
- **iDRAC User Guide:** Check Dell support site for your iDRAC version
- **Firmware Updates:** https://www.dell.com/support/home/en-us/drivers
