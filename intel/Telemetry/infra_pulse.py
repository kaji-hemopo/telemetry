#!/usr/bin/env python3
"""
infra_pulse.py — Ito Workspace Infrastructure Health Check
Run by: cron b59d1431-e95f-4d6a-a6c3-c8850a96f793
Last run: %LAST_RUN%
"""
import os
import sys
from datetime import datetime, timezone, timedelta

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG = os.path.join(WORKSPACE, "heartbeat_logs", "infra_pulse_log.md")
JST = timezone(timedelta(hours=+9))

def jst_now():
    return datetime.now(JST)

def check(name, condition, detail=""):
    status = "OK" if condition else "FAIL"
    detail_str = f" — {detail}" if detail else ""
    return f"- **{name}:** {'✅' if condition else '🔴'} {status}{detail_str}"

def run():
    ts = jst_now().strftime("%Y-%m-%d %H:%M UTC")
    findings = []
    ok_count = warn_count = fail_count = 0

    # 1. Critical directories exist
    critical_dirs = ["scripts", "kaji", "memory", "heartbeat_logs"]
    for d in critical_dirs:
        path = os.path.join(WORKSPACE, d)
        exists = os.path.isdir(path)
        findings.append(check(f"Dir: {d}", exists, "found" if exists else "MISSING"))
        if exists: ok_count += 1
        else: fail_count += 1

    # 2. Key files exist
    key_files = {
        "MEMORY.md": os.path.join(WORKSPACE, "MEMORY.md"),
        "IDENTITY.md": os.path.join(WORKSPACE, "IDENTITY.md"),
        "SOUL.md": os.path.join(WORKSPACE, "SOUL.md"),
        "HEARTBEAT.md": os.path.join(WORKSPACE, "HEARTBEAT.md"),
    }
    for name, path in key_files.items():
        exists = os.path.isfile(path)
        findings.append(check(f"File: {name}", exists, "found" if exists else "MISSING"))
        if exists: ok_count += 1
        else: fail_count += 1

    # 3. Cron session alive check (workspace processes)
    pid_file = os.path.join(WORKSPACE, ".cron_pid")
    if os.path.isfile(pid_file):
        findings.append(check("Cron PID file", True, "present"))
        ok_count += 1
    else:
        findings.append(check("Cron PID file", False, "not found (may not apply)"))
        warn_count += 1

    # 4. Scripts/Tier1_Scripts health
    scripts_dir = os.path.join(WORKSPACE, "scripts", "Tier1_Scripts")
    if os.path.isdir(scripts_dir):
        scripts = os.listdir(scripts_dir)
        findings.append(check("Tier1 Scripts", len(scripts) > 0, f"{len(scripts)} scripts"))
        ok_count += 1
    else:
        findings.append(check("Tier1 Scripts", False, "MISSING"))
        fail_count += 1

    # Determine overall status
    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    report = f"""# Infra Pulse Log

**Timestamp:** {ts}  
**Status:** {overall}

## Summary
- **OK:** {ok_count}
- **Warn:** {warn_count}
- **Fail:** {fail_count}

## Findings
{chr(10).join(findings)}

## Notes
Ito workspace heartbeat active. Cron session: b59d1431-e95f-4d6a-a6c3-c8850a96f793
"""

    with open(LOG, "w") as f:
        f.write(report)

    print(f"[infra_pulse] {overall} — OK:{ok_count} WARN:{warn_count} FAIL:{fail_count}")
    return 0 if overall != "FAIL" else 1

if __name__ == "__main__":
    sys.exit(run())
