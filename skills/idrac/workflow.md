# iDRAC Workflows

## 1. Initial Server Setup

**Use when:** A new Dell server needs iDRAC network, user, and time configuration.

**Prerequisites:**
- Physical installation complete
- Network connectivity to iDRAC
- Administrative credentials

**Steps:**
1. Test connectivity: `ping <idrac-ip>` and `racadm -r <idrac-ip> -u <user> -p <pass> get System.Model`.
2. Configure static network:
   - `racadm set idrac.IPv4.Address <ip>`
   - `racadm set idrac.IPv4.Netmask <mask>`
   - `racadm set idrac.IPv4.Gateway <gw>`
   - `racadm set idrac.IPv4.DHCPEnable 0`
3. Set DNS and NTP:
   - `racadm set idrac.Network.DNS1 <dns>`
   - `racadm set idrac.NTPConfigGroup.NTP1 <ntp>`
   - `racadm set idrac.NTPConfigGroup.NTPEnable 1`
4. Set time zone: `racadm set idrac.Time.TimeZone <zone>`.
5. Create admin and read-only users, set privileges, and enable them.
6. Generate or upload SSL certificate.
7. Run initial health check and generate a baseline TSR.

**Verification:**
- Network reachable
- Static IP configured
- DNS/NTP set
- Users created
- System health check passed
- Baseline TSR archived

## 2. Firmware Update

**Use when:** Updating iDRAC, BIOS, NIC, or other component firmware.

**Steps:**
1. Back up current configuration: `racadm get -f pre_update_config.txt`.
2. Check current firmware: `racadm get System.Firmware`.
3. Verify system health and that the job queue is empty.
4. Upload firmware via Redfish `/UpdateService/Actions/UpdateService.SimpleUpdate` or `racadm update -f <file> -l <component>`.
5. Monitor the job queue until `Completed`.
6. Post-update verification: `racadm get System.Firmware`, `getsel`, `techsupreport`.

**Rollback:** Restore `pre_update_config.txt` and apply previous firmware if needed.

## 3. Troubleshooting Hardware Issues

**Use when:** A server has symptoms of hardware failure.

**Steps:**
1. Generate TSR: `racadm techsupreport export -f <filename>.zip`.
2. Review system logs: `getsel -d`, `getlclog -d`.
3. Check component health: `get System.Processor`, `get System.Memory`, `get Storage`, `get System.Power.Supply`, `get System.Temperature`.
4. Run diagnostics: `racadm diagnostics run` and `racadm diagnostics results`.
5. Identify failed components (`Status=Disabled` or `Health!=OK`).
6. Apply fixes (reset component, reconfigure RAID, replace hardware).
7. Re-run diagnostics and generate a post-fix TSR.

## 4. Automated Health Monitoring

**Use when:** Setting up ongoing server health checks.

**Steps:**
1. Use `scripts/idrac_redfish_client.py` or a Redfish script to poll:
   - `/redfish/v1/Systems/System.Embedded.1`
   - `/redfish/v1/Systems/System.Embedded.1/Thermal`
   - `/redfish/v1/Systems/System.Embedded.1/Power`
   - `/redfish/v1/Systems/System.Embedded.1/LogServices/SEL/Entries`
2. Filter for `Critical` and `Warning` log entries.
3. Export metrics to Prometheus/Grafana or send email alerts.
4. Schedule daily TSR collection with retention (e.g., last 30 days).

## 5. Disaster Recovery Preparation

**Steps:**
1. Back up configurations:
   - `racadm get -f backup_config.txt`
   - `racadm get BIOS -f bios_backup.txt`
   - `racadm get Storage -f storage_backup.txt`
   - `racadm sslcertexport -f ssl_backup.cer`
2. Generate recovery TSR.
3. Document network configuration and VLANs.
4. Create a recovery script using `set -f` and `sslcertupload`.
5. Test on non-production hardware.
6. Encrypt and store backups offsite.
