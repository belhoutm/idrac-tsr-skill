# Quick Start Guide - iDRAC-TSR-Skill

## Getting Started Quickly

### 1. Verify Project Structure

```bash
cd /home/belhout/iDRAC-TSR-Skill
ls -la
```

Expected output:
```
drwxr-xr-x  idrac/
drwxr-xr-x  tsr-analysis/
-rw-r--r--  README.md
-rw-r--r--  QUICKSTART.md
```

### 2. Choose Your Skill

**For Active Server Management** → Use `idrac` skill
**For Log Analysis** → Use `tsr-analysis` skill

### 3. Basic Usage Examples

#### Using idrac Skill

**Power on a server:**
```
"@idrac power on server 192.168.1.100"
```

**Get system inventory:**
```
"@idrac get hardware inventory for server 192.168.1.100"
```

**Update firmware:**
```
"@idrac update firmware on server 192.168.1.100"
```

#### Using tsr-analysis Skill

**Analyze a TSR report:**
```
"@tsr analyze TSR<ServiceTag>_timestamp.zip"
```

**Check for hardware failures:**
```
"@tsr check for I2C communication failures in the TSR"
```

**Compare system configurations:**
```
"@tsr compare TSR reports between system1 and system2"
```

### 4. Common Workflows

#### Workflow 1: Server Issue Investigation

```bash
# Step 1: Collect TSR (using idrac)
# SECURITY: Replace with your actual credentials
# Never commit real credentials to Git
racadm -r 192.168.1.100 -u <YOUR_USERNAME> -p <YOUR_PASSWORD> techsupportreport

# Step 2: Analyze TSR (using tsr-analysis)
# Invoke: "@tsr analyze the collected TSR report"

# Step 3: Apply fixes (using idrac)
# Invoke: "@idrac apply the recommended configuration changes"
```

#### Workflow 2: Hardware Health Check

```bash
# Step 1: Monitor server (using idrac)
# Invoke: "@idrac check server health for 192.168.1.100"

# Step 2: If issues found, collect and analyze TSR
# Invoke: "@tsr analyze the TSR report for hardware issues"

# Step 3: Resolve issues (using idrac)
# Invoke: "@idrac update firmware or replace components"
```

### 5. Quick Reference

| Task | Skill | Example Command |
|------|-------|-----------------|
| Power on server | idrac | "@idrac power on server 192.168.1.100" |
| Get inventory | idrac | "@idrac get system inventory" |
| Update firmware | idrac | "@idrac update BIOS firmware" |
| Analyze TSR | tsr-analysis | "@tsr analyze TSR report" |
| Find hardware failures | tsr-analysis | "@tsr check for I2C failures" |
| Compare systems | tsr-analysis | "@tsr compare TSR reports" |

### 6. Prerequisites Checklist

Before using the skills, ensure you have:

- [ ] Network access to iDRAC interfaces
- [ ] Valid iDRAC credentials (username/password)
- [ ] Python 3.8+ installed
- [ ] Required Python packages: `redfish`, `argparse`
- [ ] Appropriate permissions for server management
- [ ] TSR report files (for tsr-analysis skill)

### 7. Security Setup

**Never hardcode credentials!** Use secure methods:

```bash
# Environment variables (recommended for testing)
export IDRAC_USERNAME="root"
export IDRAC_PASSWORD="calvin"
export IDRAC_HOST="192.168.1.100"

# Or use DAP secret management (for production)
# Configure secret_key inputs in your blueprints
```

### 8. Testing Your Setup

**Test iDRAC connectivity:**
```bash
# SECURITY: Replace with your actual credentials
# Never commit real credentials to Git
# Using racadm
racadm -r 192.168.1.100 -u <YOUR_USERNAME> -p <YOUR_PASSWORD> get system.hostname

# Using Python/Redfish
# SECURITY: Replace with your actual credentials
# Never commit real credentials to Git
python3 -c "from redfish import RedfishClient; client = RedfishClient('192.168.1.100', '<YOUR_USERNAME>', '<YOUR_PASSWORD>'); client.login(); print('Connected!')"
```

**Test TSR analysis:**
```bash
# Ensure you have a TSR file
ls -la TSR*.zip

# Test extraction
unzip -l TSR<ServiceTag>_timestamp.zip
```

### 9. Getting Help

For detailed information:
- **idrac skill**: See `idrac/SKILL.md`
- **tsr-analysis skill**: See `tsr-analysis/SKILL.md`
- **Full documentation**: See `README.md`

### 10. Next Steps

1. **Read the full README.md** for comprehensive documentation
2. **Explore individual skill documentation** for detailed reference
3. **Review examples** in the `examples/` directories
4. **Test with non-production servers** first
5. **Implement proper credential management** before production use

## Troubleshooting Quick Fixes

**Issue**: "Cannot connect to iDRAC"
- **Fix**: Check network connectivity, verify IP address, test credentials

**Issue**: "TSR analysis fails"
- **Fix**: Verify TSR file is not corrupted, check disk space, ensure valid format

**Issue**: "Permission denied"
- **Fix**: Verify user has sufficient privileges, check iDRAC user role

**Issue**: "Python module not found"
- **Fix**: Install dependencies: `pip install redfish argparse`

## Need More Help?

- Check individual skill documentation
- Review Dell official documentation
- Enable debug mode for detailed logging
- Contact Dell support for hardware-specific issues