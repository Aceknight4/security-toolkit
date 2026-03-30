# ============================================
# Script  : realtime_monitor.py
# Purpose : Watch a log file live and alert
#           the moment a threat appears
# Author  : Anel Graph
# Skill   : Real-time monitoring — SOC core skill
# ============================================

import time   # For time.sleep() — pause between checks
import os     # To check file exists
import re     # For pattern matching

LOG_FILE = "system_events.log"
BRUTE_THRESHOLD = 3  # Warnings before brute-force alert

# Track failed attempts per user across the session
failed_attempts = {}  # {username: count}

# -----------------------------------------------
# Part 2: Analyse a single log line for threats
# -----------------------------------------------
def analyse_line(line):
    """
    Receives one log line.
    Checks if it matches any known threat pattern.
    Prints an alert if it does.
    """
    line = line.strip()

    # Skip empty lines
    if not line:
        return

    # Print the new line so we can see activity
    print(f"  [NEW] {line}")

    # --- Check for failed login (WARNING) ---
    if "| WARNING" in line and "Failed login" in line:
        match = re.search(r"user:\s+(\S+)", line)
        if match:
            username = match.group(1)
            # Add 1 to this user's failed attempt counter
            failed_attempts[username] = failed_attempts.get(username, 0) + 1
            count = failed_attempts[username]

            if count >= BRUTE_THRESHOLD:
                print(f"\n  *** ALERT: BRUTE FORCE DETECTED ***")
                print(f"  User '{username}' has {count} failed attempts")
                print(f"  Action: Block this account immediately\n")

    # --- Check for port scan (ALERT) ---
    elif "| ALERT" in line and "Port scan" in line:
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
        ip = match.group(1) if match else "unknown"
        print(f"\n  *** ALERT: PORT SCAN DETECTED ***")
        print(f"  Source IP: {ip}")
        print(f"  Action: Check firewall rules immediately\n")

    # --- Check for critical event ---
    elif "| CRITICAL" in line:
        parts = line.split("|")
        message = parts[2].strip() if len(parts) >= 3 else "unknown"
        print(f"\n  *** CRITICAL EVENT DETECTED ***")
        print(f"  Event: {message}")
        print(f"  Action: Investigate immediately\n")

# -----------------------------------------------
# Part 3: The real-time monitor loop
# -----------------------------------------------
def start_monitor(filepath):
    """
    Opens the log file and watches it forever.
    Only reads NEW lines added after the script starts.
    """
    if not os.path.exists(filepath):
        print(f"Error: Log file '{filepath}' not found.")
        print("Run log_writer.py first to create it.")
        return

    print(f"Watching: {filepath}")
    print("Waiting for new events... (Press Ctrl+C to stop)\n")

    with open(filepath, "r") as f:
        # Jump to the END of the file
        # This skips all existing old entries
        # We only care about NEW lines from this point
        f.seek(0, 2)  # 0 = move 0 bytes, 2 = from the end

        # Forever loop
        while True:
            line = f.readline()  # Try to read a new line

            if line:
                # A new line appeared — analyse it
                analyse_line(line)
            else:
                # No new line yet — wait 1 second and try again
                time.sleep(1)

# -----------------------------------------------
# Part 4: Start everything
# -----------------------------------------------
print("\n" + "=" * 50)
print("   REAL-TIME SECURITY MONITOR — ACTIVE")
print("=" * 50)

try:
    start_monitor(LOG_FILE)
except KeyboardInterrupt:
    # This runs when you press Ctrl+C to stop
    print("\n\nMonitor stopped by user.")
    print("Session summary:")
    if failed_attempts:
        for user, count in failed_attempts.items():
            print(f"  {user}: {count} failed attempts tracked")
    else:
        print("  No threats detected this session.")
    print("=" * 50)
