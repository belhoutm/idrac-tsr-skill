# Project iDRAC Rule

This project provides Dell iDRAC server management and TSR analysis skills.

When the user mentions iDRAC, Dell server, Technical Support Report, TSR, racadm, Redfish, power management, firmware update, server inventory, or hardware diagnostics, route the request to the relevant `skill.md`.

Do this before answering:
1. If the issue is complex, time-correlated, or spans multiple subsystems, start with `workflows/main.md`.
2. Read the appropriate `skills/<subsystem>/skill.md` (e.g., `skills/idrac/skill.md`) for the skill overview and security rules.
3. Load the corresponding `workflow.md` for the relevant workflow.
4. Check `signatures.yaml` for error signatures.
5. Use `examples.md` for snippets and `references.md` for command details.

Never hardcode iDRAC credentials. Use `secret_key` inputs for DAP blueprints and environment variables for CLI scripts.
