# ============================================
# Script  : log_writer.py
# Purpose : Write and read security log entries
# Author  : Anel Graph
# Skill   : File handling — core SOC/automation skill
# ============================================

import datetime  # For timestamps
import os        # To check if file exists

# --- Config ---
LOG_FILE = "system_events.log"

# --- Function 1: Write a log entry ---
def write_log(event_type, message):
    """
    Writes a timestamped log entry to the log file.
    Format: [YYYY-MM-DD HH:MM:SS] | EVENT_TYPE | message
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] | {event_type:<10} | {message}\n"

    with open(LOG_FILE, "a") as f:  # "a" = append mode, never overwrites
        f.write(log_entry)

    print(f"  Logged: {log_entry.strip()}")

# --- Function 2: Read and display all logs ---
def read_logs():
    """
    Reads all entries from the log file and displays them.
    """
    if not os.path.exists(LOG_FILE):
        print("No log file found yet.")
        return

    print("\n" + "=" * 55)
    print("         SYSTEM EVENT LOG — FULL REPORT")
    print("=" * 55)

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    if not lines:
        print("Log file is empty.")
    else:
        for line in lines:
            print(line.strip())

    print("=" * 55)
    print(f"Total entries: {len(lines)}")
    print("=" * 55 + "\n")

# --- Main: Simulate security events ---
print("\nStarting log simulation...\n")

write_log("INFO",    "System startup complete")
write_log("WARNING", "Failed login attempt — user: admin")
write_log("WARNING", "Failed login attempt — user: admin")
write_log("WARNING", "Failed login attempt — user: admin")
write_log("CRITICAL","Account locked after 3 failed attempts")
write_log("INFO",    "Security scan completed — no threats found")
write_log("ALERT",   "Port scan detected — source IP: 192.168.1.45")
# Read back everything written
read_logs()
