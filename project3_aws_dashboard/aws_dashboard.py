# ============================================
# Script  : aws_dashboard.py
# Purpose : Live AWS Security Dashboard
#           Reads CloudTrail logs from S3
#           Detects threats and displays live
# Author  : Anel Graph
# Stack   : Python, boto3, AWS S3, CloudTrail
# ============================================

import boto3
import json
import gzip
import os
import re
import time
import datetime
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from modules.utils import clear_screen, check_python_version

check_python_version()

# --- Config ---
BUCKET_NAME    = "anel-security-logs-185188589088"
REGION         = "eu-north-1"
REFRESH_SECONDS = 30
WIDTH          = 58

# --- AWS clients ---
s3 = boto3.client('s3', region_name=REGION)

# -----------------------------------------------
# Part 1: Dashboard border helper
# -----------------------------------------------
def row(content=""):
    total = WIDTH - 2
    text  = " " + content
    padded = text + " " * (total - len(text))
    print("║" + padded + "║")

def divider(style="mid"):
    if style == "top":
        print("╔" + "═" * (WIDTH - 2) + "╗")
    elif style == "mid":
        print("╠" + "═" * (WIDTH - 2) + "╣")
    elif style == "bot":
        print("╚" + "═" * (WIDTH - 2) + "╝")

# -----------------------------------------------
# Part 2: Fetch CloudTrail log files from S3
# -----------------------------------------------
def get_log_files(max_files=5):
    """
    Lists the most recent CloudTrail log files
    in the S3 bucket and returns their keys.
    CloudTrail stores logs as gzipped JSON files.
    """
    try:
        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix="cloudtrail/",
            MaxKeys=50
        )

        if 'Contents' not in response:
            return []

        # Sort by last modified — most recent first
        objects = sorted(
            response['Contents'],
            key=lambda x: x['LastModified'],
            reverse=True
        )

        # Return only .json.gz files (CloudTrail format)
        log_files = [
            obj['Key'] for obj in objects
            if obj['Key'].endswith('.json.gz')
        ]

        return log_files[:max_files]

    except Exception as e:
        return []

# -----------------------------------------------
# Part 3: Parse a single CloudTrail log file
# -----------------------------------------------
def parse_log_file(key):
    """
    Downloads one CloudTrail log file from S3,
    decompresses it (gzip), and parses the JSON.
    Returns a list of CloudTrail event records.

    CloudTrail log structure:
    {
        "Records": [
            {
                "eventTime": "2026-04-07T...",
                "eventName": "GetObject",
                "userIdentity": {...},
                "sourceIPAddress": "1.2.3.4",
                "errorCode": "AccessDenied"  ← threats often here
            }
        ]
    }
    """
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        compressed = response['Body'].read()
        decompressed = gzip.decompress(compressed)
        log_data = json.loads(decompressed)
        return log_data.get('Records', [])
    except Exception:
        return []

# -----------------------------------------------
# Part 4: Analyse events for threats
# -----------------------------------------------
def analyse_events(all_events):
    """
    Scans CloudTrail events for suspicious patterns.
    Returns counts and detected threats.
    """
    counts = {
        "total"          : len(all_events),
        "errors"         : 0,
        "access_denied"  : 0,
        "root_usage"     : 0,
        "console_logins" : 0,
    }
    threats  = []
    recent   = []

    for event in all_events:
        event_name   = event.get('eventName', 'Unknown')
        event_time   = event.get('eventTime', '')
        source_ip    = event.get('sourceIPAddress', 'unknown')
        error_code   = event.get('errorCode', '')
        user_identity = event.get('userIdentity', {})
        user_type    = user_identity.get('type', '')
        username     = user_identity.get('userName', user_type)

        # Track recent events
        recent.append({
            "time"   : event_time[:19] if event_time else 'unknown',
            "event"  : event_name[:30],
            "user"   : username[:20],
            "ip"     : source_ip[:15]
        })

        # Count errors
        if error_code:
            counts["errors"] += 1

        # Detect AccessDenied — someone tried something they shouldn't
        if error_code == "AccessDenied":
            counts["access_denied"] += 1
            threat = f"ACCESS DENIED: {username} → {event_name}"
            if threat not in threats:
                threats.append(threat)

        # Detect root account usage — always suspicious
        if user_type == "Root":
            counts["root_usage"] += 1
            threats.append(f"ROOT USAGE DETECTED: {event_name} from {source_ip}")

        # Detect console logins
        if event_name == "ConsoleLogin":
            counts["console_logins"] += 1

    return counts, threats, recent[-5:]

# -----------------------------------------------
# Part 5: Draw the dashboard
# -----------------------------------------------
def draw_dashboard(counts, threats, recent, log_count, last_key):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    divider("top")
    row(" AWS SECURITY DASHBOARD — LIVE VIEW")
    row(f" Last updated  : {now}")
    row(f" Region        : {REGION}")
    row(f" Log files read: {log_count}")
    divider("mid")

    row(" EVENT SUMMARY")
    row(f" Total events    : {counts['total']}")
    row(f" Errors          : {counts['errors']}")
    row(f" Access denied   : {counts['access_denied']}")
    row(f" Root usage      : {counts['root_usage']}")
    row(f" Console logins  : {counts['console_logins']}")
    divider("mid")

    row(" THREAT STATUS")
    if not threats:
        row(" [OK] No threats detected")
    else:
        for t in threats[:4]:
            row(f" [!] {t[:WIDTH-8]}")
    divider("mid")

    row(" RECENT EVENTS (last 5)")
    if not recent:
        row(" No events yet — CloudTrail logs appear")
        row(" within 15 minutes of AWS activity")
    else:
        for e in recent:
            row(f" {e['time']} | {e['event'][:20]}")
    divider("bot")

# -----------------------------------------------
# Part 6: Main loop
# -----------------------------------------------
print("\n  Starting AWS Security Dashboard...")
print(f"  Bucket  : {BUCKET_NAME}")
print(f"  Region  : {REGION}")
print(f"  Refresh : every {REFRESH_SECONDS} seconds")
print("  Press Ctrl+C to stop\n")
time.sleep(2)

try:
    while True:
        clear_screen()

        # Fetch latest log files from S3
        log_files = get_log_files(max_files=5)

        # Parse all log files and combine events
        all_events = []
        for key in log_files:
            events = parse_log_file(key)
            all_events.extend(events)

        # Analyse for threats
        counts, threats, recent = analyse_events(all_events)
        last_key = log_files[0] if log_files else "none yet"

        # Draw dashboard
        draw_dashboard(counts, threats, recent, len(log_files), last_key)

        if not log_files:
            print("\n  No log files yet — CloudTrail takes ~15 minutes")
            print("  to deliver first logs. Dashboard will auto-update.")

        print(f"\n  Refreshing in {REFRESH_SECONDS}s... Ctrl+C to stop")
        time.sleep(REFRESH_SECONDS)

except KeyboardInterrupt:
    clear_screen()
    print("\n" + "=" * 58)
    print("  AWS SECURITY DASHBOARD — SESSION ENDED")
    print("=" * 58)
    print(f"  Log files analysed : {len(log_files)}")
    print(f"  Total events       : {counts.get('total', 0)}")
    print(f"  Threats detected   : {len(threats)}")
    print(f"  Session ended      : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 58)
    print("\n  Stay secure, Anel. 🛡️\n")
