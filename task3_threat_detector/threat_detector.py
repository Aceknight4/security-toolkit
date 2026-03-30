# ============================================
# Script  : threat_detector.py
# Purpose : Parse logs and detect threats automatically
# Author  : Anel Graph
# Skill   : Log analysis — core SOC analyst task
# ============================================

import re  # Regular expressions — for pattern matching in text

LOG_FILE = "system_events.log"
BRUTE_FORCE_THRESHOLD = 3  # How many warnings = a threat

# --- Storage ---
warnings   = []   # All WARNING lines collected
alerts     = []   # All ALERT lines collected
criticals  = []   # All CRITICAL lines collected
threats    = []   # Confirmed threats we detected

# --- Step 1: Read and parse the log file ---
def parse_log(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if "| WARNING" in line:
            warnings.append(line)
        elif "| ALERT" in line:
            alerts.append(line)
        elif "| CRITICAL" in line:
            criticals.append(line)

    print(f"Parsed {len(lines)} log entries.")
    print(f"  WARNING  : {len(warnings)}")
    print(f"  ALERT    : {len(alerts)}")
    print(f"  CRITICAL : {len(criticals)}\n")

# --- Step 2: Detect brute-force patterns ---
def detect_brute_force():
    # Extract usernames from WARNING lines using regex
    user_attempts = {}  # {username: count}

    for line in warnings:
        # Match pattern: "user: someusername"
        match = re.search(r"user:\s+(\S+)", line)
        if match:
            username = match.group(1)
            user_attempts[username] = user_attempts.get(username, 0) + 1

    # Flag users who exceeded the threshold
    for user, count in user_attempts.items():
        if count >= BRUTE_FORCE_THRESHOLD:
            threat = f"BRUTE FORCE DETECTED — user '{user}' had {count} failed login attempts"
            threats.append(threat)

# --- Step 3: Detect port scans ---
def detect_port_scans():
    for line in alerts:
        if "Port scan detected" in line:
            # Extract IP address using regex
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
            ip = match.group(1) if match else "unknown"
            threat = f"PORT SCAN DETECTED — source IP: {ip}"
            threats.append(threat)

# --- Step 4: Detect critical events ---
def detect_critical_events():
    """
    Any CRITICAL log entry means something damaging already occurred.
    We report every single one as a confirmed threat.
    """
    for line in criticals:
        # Extract the message part after the last "|"
        # Example line: [2026-03-30] | CRITICAL   | Account locked after 3 failed attempts
        parts = line.split("|")  # Split the line by "|" into a list
        if len(parts) >= 3:
            message = parts[2].strip()  # Take the 3rd piece — the message
            threat = f"CRITICAL EVENT — {message}"
            threats.append(threat)

# --- Step 5: Print threat report ---
def print_report():
    print("=" * 55)
    print("         AUTOMATED THREAT DETECTION REPORT")
    print("=" * 55)

    if not threats:
        print("  No threats detected. System clean.")
    else:
        print(f"  {len(threats)} THREAT(S) FOUND:\n")
        for i, threat in enumerate(threats, 1):
            print(f"  [{i}] {threat}")

    print("\n" + "=" * 55)
    print(f"  Warnings reviewed : {len(warnings)}")
    print(f"  Alerts reviewed   : {len(alerts)}")
    print(f"  Criticals logged  : {len(criticals)}")
    print(f"  Threats confirmed : {len(threats)}")
    print("=" * 55)

# --- Run everything ---
print("\nRunning threat detector...\n")
parse_log(LOG_FILE)
detect_brute_force()
detect_port_scans()
detect_critical_events() 
print_report()
