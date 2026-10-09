# Skill Trigger Guide

## Quick Reference

### @ Trigger Notation

Both skills in this project support quick `@` trigger notation for immediate invocation:

- **@idrac** - Invoke the idrac skill for server management
- **@tsr** - Invoke the tsr-analysis skill for log analysis

## Usage Examples

### @idrac Examples

**Power Management:**
```
"@idrac power on server 192.168.1.100"
"@idrac power off server 192.168.1.100"
"@idrac restart server 192.168.1.100"
```

**System Information:**
```
"@idrac get system inventory"
"@idrac get firmware versions"
"@idrac check server health"
```

**Configuration:**
```
"@idrac set BIOS attribute"
"@idrac configure network settings"
"@idrac update firmware"
```

**TSR Collection:**
```
"@idrac collect TSR report"
"@idrac generate technical support report"
```

### @tsr Examples

**Basic Analysis:**
```
"@tsr analyze TSR<ServiceTag>_timestamp.zip"
"@tsr analyze the TSR report"
```

**Hardware Diagnosis:**
```
"@tsr check for hardware failures"
"@tsr identify I2C communication failures"
"@tsr check for voltage regulator issues"
```

**Deployment Analysis:**
```
"@tsr analyze deployment failure"
"@tsr investigate ESXi reimage failure"
"@tsr review deployment timeline"
```

### @security-audit Examples

**Pre-commit Scan:**
```
"@security-audit scan staged files for secrets"
"@security-audit check for credentials before commit"
```

**Credential Detection:**
```
"@security-audit find hardcoded passwords"
"@security-audit scan for API keys"
```

**Comparison:**
```
"@tsr compare TSR reports between system1 and system2"
"@tsr compare working vs failing server configurations"
```

**Specific Error Searches:**
```
"@tsr search for I2C_Master_Write_Read failures"
"@tsr check for power supply events"
"@tsr review lifecycle events"
```

## Traditional Invocation Methods

The @ notation is optional. You can still use traditional invocation methods:

### Traditional idrac Invocation
```
"Use the idrac skill to power on server 192.168.1.100"
"Use idrac for server management"
"Analyze TSR report using idrac capabilities"
```

### Traditional tsr-analysis Invocation
```
"Use tsr-analysis to analyze the TSR report"
"Use the tsr-analysis skill"
"Analyze Technical Support Report for hardware issues"
```

## Combined Usage

You can combine @ notation with detailed instructions:

```
"@idrac power on server 192.168.1.100 and verify the system state"
"@tsr analyze TSRABC123.zip and focus on I2C communication failures"
"@idrac collect TSR report and then @tsr analyze it for hardware issues"
```

## Best Practices

1. **Use @ notation for quick tasks**: Simple, straightforward operations
2. **Use traditional phrases for complex tasks**: When you need detailed context
3. **Be specific with @ notation**: Include relevant details in your command
4. **Chain commands**: Use both skills in sequence for complete workflows

## Workflow Examples

### Server Issue Investigation
```
"@idrac collect TSR report from server 192.168.1.100"
"@tsr analyze the collected TSR for hardware failures"
"@idrac apply the recommended fixes"
```

### Health Monitoring
```
"@idrac check server health for all servers in cluster"
"@tsr analyze TSR reports for any servers showing issues"
"@idrac update firmware on affected servers"
```

### Deployment Troubleshooting
```
"@idrac monitor deployment progress"
"@tsr analyze TSR report if deployment fails"
"@idrac apply configuration corrections"
```

## Trigger Word Summary

| Trigger | Skill | Purpose |
|---------|-------|---------|
| @idrac | idrac | Active server management and operations |
| @tsr | tsr-analysis | TSR log analysis and diagnostics |
| @security-audit | security-audit | Credential and secret scanning |
| iDRAC | idrac | Traditional iDRAC skill invocation |
| TSR analysis | tsr-analysis | Traditional TSR analysis invocation |
| security audit | security-audit | Traditional security audit invocation |
| Dell server | idrac | Server management tasks |
| Technical Support Report | idrac / tsr-analysis | Can invoke either skill based on context |

## Advantages of @ Notation

1. **Faster typing**: Shorter commands
2. **Clear intent**: Immediately obvious which skill you want
3. **Less ambiguity**: No confusion about which skill to use
4. **Better for workflows**: Easy to chain commands
5. **Modern syntax**: Familiar to users of other tools

## Migration Guide

If you're used to the traditional invocation methods, here's how to migrate:

**Old way:**
```
"Use the idrac skill to power on server 192.168.1.100"
```

**New way:**
```
"@idrac power on server 192.168.1.100"
```

**Old way:**
```
"Use tsr-analysis to analyze the TSR report"
```

**New way:**
```
"@tsr analyze the TSR report"
```

Both methods continue to work, so you can migrate gradually or use whichever feels more natural for each situation.

## Troubleshooting

**@ notation not working?**
- Ensure you're using the correct skill names: @idrac and @tsr
- Check that the skill files are properly configured
- Try traditional invocation as a fallback

**Wrong skill being invoked?**
- Be more specific in your command
- Use the full skill name: @tsr-analysis instead of @tsr
- Provide more context about what you want to accomplish

**Want to use both skills in one command?**
- Chain the commands: "@idrac collect TSR, then @tsr analyze it"
- Use separate commands for each step
- Reference the specific skill you want for each part of the task