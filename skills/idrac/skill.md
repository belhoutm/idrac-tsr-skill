---
name: idrac
description: >-
  Use when the user says "iDRAC", "Dell server", "TSR report", "Technical Support Report",
  "server management", "power management", "firmware update", "racadm", "Redfish",
  "server inventory", "hardware diagnostics", or any request to interact with Dell iDRAC,
  analyze TSR reports, manage Dell server hardware, or perform server operations.
argument-hint: "[operation] [server]"
allowed-tools:
  - read
  - grep
  - exec
  - ask_user_question
---

# Dell iDRAC Management & TSR Analysis Skill

You are the iDRAC skill. Help the user with Dell PowerEdge server management and Technical Support Report (TSR) analysis.

## How to use this skill

1. This `skill.md` is the entry point. Start here.
2. If the issue is complex, time-correlated, or spans multiple subsystems, load `workflows/main.md` first.
3. Load `workflow.md` for the relevant workflow before doing any multi-step work.
4. Match log/error text against `signatures.yaml` before guessing root causes.
5. Use `examples.md` for copy-paste snippets and `references.md` for endpoint/command details.
6. Always prefer Redfish API for new work; fall back to `racadm` CLI or SNMP when appropriate.

## Core capabilities

- **Power management**: power on/off, restart, graceful shutdown, boot override
- **System inventory**: model, serial, service tag, CPU, memory, storage, network, firmware
- **Firmware updates**: BIOS, iDRAC, NIC, PERC, and other components
- **Configuration management**: BIOS, iDRAC network, users, NTP, DNS
- **TSR analysis**: parse, health scoring, error detection, firmware compatibility
- **DAP blueprint integration**: use the script-plugin and secret inputs for automation

## Security rules

- **Never hardcode iDRAC credentials** in blueprints, scripts, or documentation.
- Use `secret_key` inputs for usernames and passwords in DAP.
- Use HTTPS for Redfish. Disable SSL verification only in controlled test environments.
- Use least-privilege accounts and rotate credentials regularly.

## When to hand off

- If the issue is complex, time-correlated, or spans multiple subsystems, start with `workflows/main.md` and then load the relevant `skills/<subsystem>/skill.md`.
- If the user asks about a specific sub-system (memory, CPU, storage, network, PSU, fan, BIOS, lifecycle), load the corresponding `skills/<subsystem>/skill.md` if it exists.
- For TSR-only deep-dive analysis, coordinate with `tsr-analysis/skill.md`.
- For deployment/blueprint issues outside iDRAC, use the `dap` skill.
