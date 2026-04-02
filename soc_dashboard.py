# ============================================
# Script  : soc_dashboard.py
# Purpose : Live-updating SOC terminal dashboard
# Author  : Anel Graph
# Skill   : Capstone — brings all tools together
# ============================================

import os
import re
import time
import datetime

LOG_FILE = "security_events.log"
REFRESH_SECONDS = 5
BRUTE_THRESHOLD = 3
WIDTH = 56

def row(content=""):
    total = WIDTH - 2
    text = " " + content
    padded = text + " " * (total - len(text))
    print("║" + padded + "║")

def divider(style="mid"):
    if style == "top":
        print("╔" + "═" * (WIDTH - 2) + "╗")
    elif style == "mid":
        print("╠" + "═" * (WIDTH - 2) + "╣")
    elif style == "bot":
        print("╚" + "═" * (WIDTH - 2) + "╝")

def parse_log():
    counts = {"INFO": 0, "WARNING": 0, "CRITICAL": 0, "ALERT": 0}
    all_lines = []
    user_attempts = {}
    threats = []

    if not os.path.exists(LOG_FILE):
        return counts, [], ["No log file found — run Log Writer first"]

    with open(LOG_FILE, "r") as f:
        all_lines = [l.strip() for l in f.readlines() if l.strip()]

    for lt in all_lines:
        if "| INFO" in lt:
            counts["INFO"] += 1
        elif "| WARNING" in lt:
            counts["WARNING"] += 1
        elif "| CRITICAL" in lt:
            counts["CRITICAL"] += 1
        elif "| ALERT" in lt:
            counts["ALERT"] += 1

    for lt in all_lines:
        if "| WARNING" in lt and "login" in lt:
            match = re.search(r"user:\s+(\S+)", lt)
            if match:
                u = match.group(1)
                user_attempts[u] = user_attempts.get(u, 0) + 1

    for user, count in user_attempts.items():
        if count >= BRUTE_THRESHOLD:
            threats.append(f"BRUTE FORCE: '{user}' — {count} attempts")

    seen_ips = []
    for lt in all_lines:
        if "| ALERT" in lt and "scan" in lt:
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)", lt)
            ip = match.group(1) if match else "unknown"
            if ip not in seen_ips:
                seen_ips.append(ip)
                threats.append(f"PORT SCAN: source IP {ip}")

    seen_crits = []
    for lt in all_lines:
        if "| CRITICAL" in lt:
            parts = lt.split("|")
            if len(parts) >= 3:
                msg = parts[2].strip()[:38]
                if msg not in seen_crits:
                    seen_crits.append(msg)
                    threats.append(f"CRITICAL: {msg}")

    recent = all_lines[-5:]
    recent.reverse()
    return counts, recent, threats

def draw(counts, recent, threats):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = sum(counts.values())

    divider("top")
    row(" SOC DASHBOARD — LIVE VIEW")
    row(f" Last updated : {now}")
    divider("mid")

    row(" EVENT SUMMARY")
    row(f" INFO     : {counts['INFO']:<6} WARNING  : {counts['WARNING']}")
    row(f" CRITICAL : {counts['CRITICAL']:<6} ALERT    : {counts['ALERT']}")
    row(f" TOTAL    : {total}")
    divider("mid")

    row(" THREAT STATUS")
    if not threats:
        row(" [OK] No active threats detected")
    else:
        for t in threats[:5]:
            row(f" [!] {t[:WIDTH-8]}")
    divider("mid")

    row(" RECENT EVENTS (last 5)")
    if not recent:
        row(" No events logged yet")
    else:
        for event in recent:
            parts = event.split("|")
            if len(parts) >= 3:
                etype = parts[1].strip()[:8]
                msg = parts[2].strip()[:WIDTH-16]
                row(f" [{etype}] {msg}")
    divider("bot")

print("\n  Starting SOC Dashboard...")
print(f"  Log file : {LOG_FILE}")
print(f"  Refresh  : every {REFRESH_SECONDS} seconds")
print("  Press Ctrl+C to exit\n")
time.sleep(2)

try:
    while True:
        os.system("clear")
        counts, recent, threats = parse_log()
        draw(counts, recent, threats)
        print(f"\n  Refreshing in {REFRESH_SECONDS}s... Ctrl+C to stop")
        time.sleep(REFRESH_SECONDS)

except KeyboardInterrupt:
    os.system("clear")
    print("\n" + "=" * 56)
    print("  SOC DASHBOARD — SESSION ENDED")
    print("=" * 56)
    print(f"  Final event count : {sum(counts.values())}")
    print(f"  Active threats    : {len(threats)}")
    print(f"  Session ended     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 56)
    print("\n  Stay secure, Anel. 🛡️\n")