# Main Troubleshooting Workflow

This is the default orchestration workflow for complex, time-correlated Dell server issues.
Use it whenever the user provides a timestamp, a TSR/ZIP file, or a symptom that may span multiple subsystems (iDRAC, storage, memory, network, power, etc.).

## Trigger

- User provides a timestamp or a relative time range (e.g., "around 14:30", "last night").
- User asks for root cause analysis of a server crash, hardware failure, or deployment failure.
- User supplies a TSR or lifecycle log dump.
- Multiple subsystems may be involved.

## Steps

### 1. Parse the time scope

1. Identify the user-specified timestamp.
2. Establish a window around it. Default: ±30 minutes.
3. Convert all timestamps to the timezone used in the log source (usually UTC from iDRAC).

### 2. Load the relevant skill(s)

For each suspected subsystem, load its `skill.md` entry point:

- `skills/idrac/skill.md` for iDRAC, power, firmware, inventory, lifecycle logs
- `tsr-analysis/skill.md` for deep TSR package analysis
- `security-audit/skill.md` for credential or secret detection
- `skills/memory/skill.md` if memory errors are suspected
- `skills/cpu/skill.md` if CPU/processor errors are suspected
- `skills/storage/skill.md` if RAID, disk, or storage errors are suspected
- `skills/network/skill.md` if network or NIC errors are suspected
- `skills/power/skill.md` if PSU or power events are suspected

If the subsystem is unclear, start with `skills/idrac/skill.md` because it hosts the lifecycle log gateway and can route to other skills.

### 3. Analyze Lifecycle Controller logs

1. Locate `lclog*.xml` or lifecycle logs in the TSR or via iDRAC Redfish:
   - `GET /redfish/v1/Managers/iDRAC.Embedded.1/Oem/Dell/LCLogs`
   - `GET /redfish/v1/Systems/System.Embedded.1/LogServices/LifecycleLog/Entries`
2. Filter entries to the selected time window.
3. Identify alerts, severity levels, and affected components.
4. Extract `MessageId`, `MessageArgs`, and `Severity` for deterministic matching.

### 4. Identify alerts and affected subsystems

1. Match messages against `skills/<subsystem>/signatures.yaml`.
2. Group findings by subsystem.
3. Count occurrences and severity.
4. Note any cascading events (e.g., power event → fan error → thermal shutdown).

### 5. Invoke the appropriate skill(s)

For each affected subsystem:

1. Load its `skill.md`.
2. Let the skill read its own `workflow.md`, `signatures.yaml`, `examples.md`, and `references.md`.
3. Collect subsystem-specific findings, evidence, and confidence.

### 6. Correlate findings across skills

1. Build a timeline that merges events from all subsystems.
2. Identify cause-consequence chains:
   - Power supply failure → voltage regulator error → CPU memory errors
   - Thermal event → fan failure → system shutdown
   - Firmware update → job exception → component not responding
3. Mark primary events (root cause) and secondary events (symptoms).

### 7. Check for additional artifacts

Based on findings, request or extract more evidence:

- **Environmental / thermal events:** Ask the user to extract `tsr/hardware/platformdata/thermaldata.zip` manually. Dell protects this archive with a password, so it cannot be extracted automatically.
- **Debug logs:** If `tsr/dbglog/logs/dumplogs.zip` exists, invoke `workflows/debug_logs.md` (create if missing) for deeper firmware/iDRAC dump analysis.
- **Crash dumps / core dumps:** Look for `tsr/dbglog/logs/dumps/` or `iDRACDebug.txt`.
- **Power data:** Look for `tsr/hardware/platformdata/powerdata.xml` or `power.xml`.

### 8. Produce a consolidated report

The report should contain:

| Section | Content |
|---------|---------|
| Summary | What happened, when, and which server/service tag |
| Evidence | Key log lines, timestamps, and source files |
| Affected Subsystems | List of subsystems involved and their findings |
| Timeline | Chronological event chain with confidence levels |
| Probable Root Cause | Primary cause with supporting evidence |
| Confidence | High / Medium / Low with caveats |
| Recommended Actions | Immediate, short-term, and long-term remediation |
| Missing Data | Artifacts that could improve confidence (e.g., password-protected thermal zip) |

## Handoff rules

- If a finding maps to exactly one subsystem, hand off to that subsystem skill and let it drive.
- If multiple subsystems are involved, stay in this main workflow and coordinate.
- If the user only has a TSR and no timestamp, use the TSR generation timestamp as the anchor and ask for confirmation.
- If the user wants automated remediation, switch to `skills/idrac/workflow.md` for iDRAC operations.
