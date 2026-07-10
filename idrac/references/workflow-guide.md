# iDRAC Workflow Guides

This guide provides step-by-step workflows for common iDRAC operations and TSR analysis tasks.

## Workflow 1: Initial Server Setup and Configuration

### Use Case
Set up a new Dell server with proper iDRAC configuration, network settings, and initial health check.

### Prerequisites
- Server physical installation complete
- Network connectivity available
- iDRAC access credentials
- Administrative access to network equipment

### Steps

#### 1.1 Initial Connection Test
```bash
# Test network connectivity
ping <idrac-ip>

# Test iDRAC access via racadm
racadm -r <idrac-ip> -u root -p calvin get System.Model

# Test Redfish API access
curl -k -u root:calvin https://<idrac-ip>/redfish/v1/Systems
```

#### 1.2 Configure Network Settings
```bash
# Set static IP address
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.Address 192.168.1.100
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.Netmask 255.255.255.0
racadm -r <idrac-ip> -u root -p calvin set idrac.IPv4.Gateway 192.168.1.1

# Configure DNS
racadm -r <idrac-ip> -u root -p calvin set idrac.Network.DNS1 192.168.1.10
racadm -r <idrac-ip> -u root -p calvin set idrac.Network.DNS2 192.168.1.11

# Configure NTP
racadm -r <idrac-ip> -u root -p calvin set idrac.NTPConfigGroup.NTP1 192.168.1.10
racadm -r <idrac-ip> -u root -p calvin set idrac.NTPConfigGroup.NTPEnable 1
```

#### 1.3 Configure Time Zone
```bash
# Set time zone
racadm -r <idrac-ip> -u root -p calvin set idrac.Time.TimeZone America/New_York
```

#### 1.4 Create User Accounts
```bash
# Create admin user
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.2.UserName admin
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.2.Password secure_password
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.2.Enable 1
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.2.Privilege 0x000001ff

# Create read-only user
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.3.UserName readonly
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.3.Password readonly_password
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.3.Enable 1
racadm -r <idrac-ip> -u root -p calvin set idrac.Users.3.Privilege 0x00000001
```

#### 1.5 Configure SSL Certificate
```bash
# Generate CSR
racadm -r <idrac-ip> -u root -p calvin sslcsr -g -f csr.txt

# Submit CSR to CA and obtain certificate
# Import signed certificate
racadm -r <idrac-ip> -u root -p calvin sslcertupload -t 1 -f signed_certificate.crt
```

#### 1.6 Initial Health Check
```bash
# Get system information
racadm -r <idrac-ip> -u root -p calvin get System

# Check component health
racadm -r <idrac-ip> -u root -p calvin get System.Processor
racadm -r <idrac-ip> -u root -p calvin get System.Memory
racadm -r <idrac-ip> -u root -p calvin get Storage

# Check system logs
racadm -r <idrac-ip> -u root -p calvin getsel
racadm -r <idrac-ip> -u root -p calvin getlclog
```

#### 1.7 Generate Baseline TSR
```bash
# Generate initial TSR report
racadm -r <idrac-ip> -u root -p calvin techsupreport export -f baseline_tsr.zip
```

### Verification Checklist
- [ ] Network connectivity confirmed
- [ ] Static IP configured and accessible
- [ ] DNS and NTP configured
- [ ] User accounts created with appropriate privileges
- [ ] SSL certificate installed
- [ ] System health check passed
- [ ] Baseline TSR generated and archived

---

## Workflow 2: Firmware Update Process

### Use Case
Update server firmware (BIOS, iDRAC, NIC, etc.) using best practices to minimize downtime and risk.

### Prerequisites
- Valid backup of current configuration
- Firmware files downloaded from Dell support site
- Maintenance window scheduled
- Update procedure documented

### Steps

#### 2.1 Pre-Update Checks
```bash
# Check current firmware versions
racadm -r <idrac-ip> -u root -p calvin get System.Firmware

# Check system health
racadm -r <idrac-ip> -u root -p calvin get System.Power
racadm -r <idrac-ip> -u root -p calvin get System.Temperature

# Check for running jobs
racadm -r <idrac-ip> -u root -p calvin jobqueue view

# Export current configuration
racadm -r <idrac-ip> -u root -p calvin get -f pre_update_config.txt
```

#### 2.2 Schedule Maintenance Window
```bash
# Schedule iDRAC firmware update
racadm -r <idrac-ip> -u root -p calvin update -f idrac_firmware.exe -s "2024-01-15T02:00:00"

# Schedule BIOS update
racadm -r <idrac-ip> -u root -p calvin jobqueue create BIOS.Setup.1-1 -s "2024-01-15T02:30:00"
```

#### 2.3 Monitor Update Progress
```bash
# Monitor job queue
watch -n 10 'racadm -r <idrac-ip> -u root -p calvin jobqueue view'

# Check update status
racadm -r <idrac-ip> -u root -p calvin jobqueue view <job-id>
```

#### 2.4 Post-Update Verification
```bash
# Verify firmware versions
racadm -r <idrac-ip> -u root -p calvin get System.Firmware

# Check system health
racadm -r <idrac-ip> -u root -p calvin get System

# Check system logs for update-related entries
racadm -r <idrac-ip> -u root -p calvin getsel

# Generate post-update TSR
racadm -r <idrac-ip> -u root -p calvin techsupreport export -f post_update_tsr.zip
```

#### 2.5 Rollback Procedure (if needed)
```bash
# If update fails, restore previous configuration
racadm -r <idrac-ip> -u root -p calvin set -f pre_update_config.txt

# Revert firmware if necessary
# (Requires specific firmware rollback procedure per Dell documentation)
```

### Verification Checklist
- [ ] Pre-update health check passed
- [ ] Configuration backed up
- [ ] Maintenance window confirmed
- [ ] Updates scheduled
- [ ] Update progress monitored
- [ ] Post-update verification completed
- [ ] System health confirmed
- [ ] Post-update TSR generated

---

## Workflow 3: Troubleshooting Hardware Issues

### Use Case
Diagnose and resolve hardware issues using iDRAC tools and TSR analysis.

### Prerequisites
- Server experiencing issues
- iDRAC access available
- TSR report generated

### Steps

#### 3.1 Generate TSR Report
```bash
# Generate comprehensive TSR
racadm -r <idrac-ip> -u root -p calvin techsupreport export -f troubleshooting_tsr.zip
```

#### 3.2 Analyze System Logs
```bash
# Check System Event Log for errors
racadm -r <idrac-ip> -u root -p calvin getsel -d

# Check Lifecycle Controller logs
racadm -r <idrac-ip> -u root -p calvin getlclog -d

# Filter for critical errors
racadm -r <idrac-ip> -u root -p calvin getsel | grep -i critical
```

#### 3.3 Check Component Health
```bash
# Check processor health
racadm -r <idrac-ip> -u root -p calvin get System.Processor

# Check memory health
racadm -r <idrac-ip> -u root -p calvin get System.Memory

# Check storage health
racadm -r <idrac-ip> -u root -p calvin get Storage.RAID.Integrated.1-1

# Check power supply status
racadm -r <idrac-ip> -u root -p calvin get System.Power.Supply

# Check temperature readings
racadm -r <idrac-ip> -u root -p calvin get System.Temperature
```

#### 3.4 Run Diagnostics
```bash
# Run system diagnostics
racadm -r <idrac-ip> -u root -p calvin diagnostics run

# Get diagnostic results
racadm -r <idrac-ip> -u root -p calvin diagnostics results
```

#### 3.5 Identify Failed Components
```bash
# Check for disabled components
racadm -r <idrac-ip> -u root -p calvin get System | grep -i "Status=Disabled"

# Check for components with health issues
racadm -r <idrac-ip> -u root -p calvin get System | grep -i "Health!=OK"
```

#### 3.6 Implement Fixes
```bash
# Example: Reset failed component
racadm -r <idrac-ip> -u root -p calvin set System.Processor.CPU1.Reset 1

# Example: Clear memory errors
racadm -r <idrac-ip> -u root -p calvin set System.Memory.DIMM.Socket.A1.Reset 1

# Example: Reconfigure storage
racadm -r <idrac-ip> -u root -p calvin storage deletevd VirtualDisk.0:RAID.Integrated.1-1
racadm -r <idrac-ip> -u root -p calvin storage createvd -rl 1 -pdisklist <disk_list>
```

#### 3.7 Verify Resolution
```bash
# Re-run diagnostics
racadm -r <idrac-ip> -u root -p calvin diagnostics run

# Check component health
racadm -r <idrac-ip> -u root -p calvin get System

# Generate post-fix TSR
racadm -r <idrac-ip> -u root -p calvin techsupreport export -f post_fix_tsr.zip
```

### Verification Checklist
- [ ] TSR report generated
- [ ] System logs analyzed
- [ ] Component health checked
- [ ] Diagnostics run
- [ ] Failed components identified
- [ ] Fixes implemented
- [ ] Resolution verified
- [ ] Post-fix TSR generated

---

## Workflow 4: Automated Server Health Monitoring

### Use Case
Implement automated health monitoring for Dell servers using iDRAC and TSR analysis.

### Prerequisites
- Python environment with necessary libraries
- Network access to iDRAC interfaces
- Monitoring system (Prometheus, Grafana, etc.)

### Steps

#### 4.1 Setup Monitoring Script
```python
#!/usr/bin/env python3
import requests
import json
from datetime import datetime

class IDRACHealthMonitor:
    def __init__(self, idrac_ip, username, password):
        self.idrac_ip = idrac_ip
        self.username = username
        self.password = password
        self.base_url = f"https://{idrac_ip}/redfish/v1"
    
    def get_system_health(self):
        """Get overall system health"""
        response = requests.get(
            f"{self.base_url}/Systems/System.Embedded.1",
            auth=(self.username, self.password),
            verify=False
        )
        return response.json()
    
    def get_temperature_data(self):
        """Get temperature readings"""
        response = requests.get(
            f"{self.base_url}/Systems/System.Embedded.1/Thermal",
            auth=(self.username, self.password),
            verify=False
        )
        return response.json()
    
    def get_power_consumption(self):
        """Get power consumption data"""
        response = requests.get(
            f"{self.base_url}/Systems/System.Embedded.1/Power",
            auth=(self.username, self.password),
            verify=False
        )
        return response.json()
    
    def check_for_alerts(self):
        """Check system logs for alerts"""
        response = requests.get(
            f"{self.base_url}/Systems/System.Embedded.1/LogServices/SEL/Entries",
            auth=(self.username, self.password),
            verify=False
        )
        logs = response.json()
        
        alerts = []
        for entry in logs['Members']:
            if entry['Severity'] in ['Critical', 'Warning']:
                alerts.append({
                    'timestamp': entry['Created'],
                    'severity': entry['Severity'],
                    'message': entry['Message']
                })
        
        return alerts
    
    def generate_health_report(self):
        """Generate comprehensive health report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_health': self.get_system_health(),
            'temperature': self.get_temperature_data(),
            'power': self.get_power_consumption(),
            'alerts': self.check_for_alerts()
        }
        return report

# Usage
monitor = IDRACHealthMonitor('idrac-ip', 'username', 'password')
report = monitor.generate_health_report()
print(json.dumps(report, indent=2))
```

#### 4.2 Schedule Regular TSR Generation
```bash
# Add to crontab for daily TSR generation
0 2 * * * /usr/local/bin/generate_tsr.sh
```

```bash
#!/bin/bash
# generate_tsr.sh
IDRAC_IP=$1
USERNAME=$2
PASSWORD=$3
OUTPUT_DIR="/var/lib/tsr_reports"
DATE=$(date +%Y%m%d)

# Generate TSR
racadm -r $IDRAC_IP -u $USERNAME -p $PASSWORD techsupreport export -f $OUTPUT_DIR/tsr_$DATE.zip

# Keep last 30 days
find $OUTPUT_DIR -name "tsr_*.zip" -mtime +30 -delete
```

#### 4.3 Setup Automated Analysis
```python
#!/usr/bin/env python3
import schedule
import time
from tsr_analyzer import TSRHealthAnalyzer

def analyze_tsr_reports():
    """Analyze latest TSR reports"""
    analyzer = TSRHealthAnalyzer('/var/lib/tsr_reports/latest.zip')
    health = analyzer.assess_health()
    
    if health['health_score'] < 80:
        send_alert(health)
    
    export_metrics_to_prometheus(health)

schedule.every().day.at("03:00").do(analyze_tsr_reports)

while True:
    schedule.run_pending()
    time.sleep(60)
```

#### 4.4 Configure Alerting
```python
def send_alert(health_report):
    """Send alert based on health report"""
    if health_report['overall_health'] == 'Critical':
        # Send critical alert
        send_email(
            to='admin@company.com',
            subject='CRITICAL: Server Health Alert',
            body=json.dumps(health_report, indent=2)
        )
        # Send to monitoring system
        send_to_prometheus_alertmanager(health_report)
```

### Verification Checklist
- [ ] Monitoring script configured
- [ ] Credentials secured
- [ ] TSR generation scheduled
- [ ] Analysis automation setup
- [ ] Alerting configured
- [ ] Metrics exported to monitoring system
- [ ] Alert thresholds defined

---

## Workflow 5: Disaster Recovery Preparation

### Use Case
Prepare servers for disaster recovery by backing up configurations and creating recovery procedures.

### Prerequisites
- Administrative access to all servers
- Backup storage location
- Recovery procedures documented

### Steps

#### 5.1 Configuration Backup
```bash
# Backup complete iDRAC configuration
racadm -r <idrac-ip> -u root -p calvin get -f backup_config.txt

# Backup BIOS configuration
racadm -r <idrac-ip> -u root -p calvin get BIOS -f bios_backup.txt

# Backup RAID configuration
racadm -r <idrac-ip> -u root -p calvin get Storage -f storage_backup.txt

# Export SSL certificates
racadm -r <idrac-ip> -u root -p calvin sslcertexport -f ssl_backup.cer
```

#### 5.2 Generate Recovery TSR
```bash
# Generate comprehensive TSR for recovery
racadm -r <idrac-ip> -u root -p calvin techsupreport export -f recovery_tsr.zip
```

#### 5.3 Document Network Configuration
```bash
# Export network configuration
racadm -r <idrac-ip> -u root -p calvin get idrac.Network > network_config.txt

# Document VLAN settings
racadm -r <idrac-ip> -u root -p calvin get NIC.VLAN > vlan_config.txt
```

#### 5.4 Create Recovery Script
```bash
#!/bin/bash
# recover_server.sh
IDRAC_IP=$1
BACKUP_DIR=$2

# Restore iDRAC configuration
racadm -r $IDRAC_IP -u root -p calvin set -f $BACKUP_DIR/backup_config.txt

# Restore BIOS configuration
racadm -r $IDRAC_IP -u root -p calvin set BIOS -f $BACKUP_DIR/bios_backup.txt

# Restore SSL certificate
racadm -r $IDRAC_IP -u root -p calvin sslcertupload -t 1 -f $BACKUP_DIR/ssl_backup.cer

# Verify configuration
racadm -r $IDRAC_IP -u root -p calvin get System
```

#### 5.5 Test Recovery Procedure
```bash
# Test on non-production server first
./recover_server.sh test-server-ip /path/to/backups

# Verify all settings restored correctly
```

#### 5.6 Store Backup Offsite
```bash
# Encrypt and transfer to offsite storage
gpg -c backup_config.txt
scp backup_config.txt.gpg offsite-server:/backups/
```

### Verification Checklist
- [ ] All configurations backed up
- [ ] Recovery TSR generated
- [ ] Network configuration documented
- [ ] Recovery script created
- [ ] Recovery procedure tested
- [ ] Backups stored offsite
- [ ] Backup encryption configured
- [ ] Recovery documentation updated

---

## Best Practices

### General
- Always test procedures on non-production servers first
- Maintain detailed documentation of all procedures
- Use version control for configuration files
- Implement proper credential management
- Schedule regular backup verification

### Security
- Use strong passwords and change regularly
- Enable SSL/TLS for all connections
- Implement principle of least privilege
- Regularly audit user access
- Monitor for unauthorized access attempts

### Automation
- Automate repetitive tasks
- Implement monitoring and alerting
- Use configuration management tools
- Maintain audit trails
- Test automation regularly

### Documentation
- Document all procedures and configurations
- Maintain change logs
- Keep contact information updated
- Document escalation procedures
- Regularly review and update documentation
