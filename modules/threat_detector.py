import re
import os

LOG_FILE = "security_events.log"
BRUTE_FORCE_THRESHOLD = 3

warnings  = []
alerts    = []
criticals = []
threats   = []

def parse_log(filepath):
    global warnings, alerts, criticals, threats
    warnings, alerts, criticals, threats = [], [], [], []
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

def detect_brute_force():
    user_attempts = {}
    for line in warnings:
        match = re.search(r"user:\s+(\S+)", line)
        if match:
            username = match.group(1)
            user_attempts[username] = user_attempts.get(username, 0) + 1
    for user, count in user_attempts.items():
        if count >= BRUTE_FORCE_THRESHOLD:
            threats.append(f"BRUTE FORCE DETECTED — user '{user}' had {count} failed login attempts")

def detect_port_scans():
    for line in alerts:
        if "Port scan detected" in line:
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
            ip = match.group(1) if match else "unknown"
            threats.append(f"PORT SCAN DETECTED — source IP: {ip}")

def detect_critical_events():
    for line in criticals:
        parts = line.split("|")
        if len(parts) >= 3:
            message = parts[2].strip()
            threats.append(f"CRITICAL EVENT — {message}")

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
    print(f"  Warnings reviewed  : {len(warnings)}")
    print(f"  Alerts reviewed    : {len(alerts)}")
    print(f"  Criticals reviewed : {len(criticals)}")
    print(f"  Threats confirmed  : {len(threats)}")
    print("=" * 55)

if __name__ == "__main__":
    print("\nRunning threat detector...\n")
    parse_log(LOG_FILE)
    detect_brute_force()
    detect_port_scans()
    detect_critical_events()
    print_report()