# ============================================
# Script  : ai_ids.py
# Purpose : AI-Powered Intrusion Detection System
#           Uses Groq/Llama to analyse log lines
#           in real time and detect threats
# Author  : Anel Graph
# Project : Portfolio Project 2
# ============================================

import os
import sys
import time
import datetime
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from modules.utils import clear_screen, check_python_version, set_api_key_instructions

from groq import Groq

check_python_version()

# -----------------------------------------------
# Config
# -----------------------------------------------
LOG_FILE        = "ai_ids_events.log"
REFRESH_SECONDS = 3
MODEL           = "llama-3.3-70b-versatile"
MAX_TOKENS      = 120
WIDTH           = 58

# -----------------------------------------------
# Storage — kept in memory during session
# -----------------------------------------------
session_alerts  = []   # All AI-confirmed threats this session
total_analysed  = 0    # Total lines sent to AI

# -----------------------------------------------
# Part 1: Setup Groq client
# -----------------------------------------------
def get_client():
    """
    Creates and returns a Groq client.
    Exits cleanly if API key is missing.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\n  ERROR: GROQ_API_KEY not set.")
        set_api_key_instructions("GROQ")
        sys.exit(1)
    return Groq(api_key=api_key)

# -----------------------------------------------
# Part 2: Ask AI to analyse one log line
# -----------------------------------------------
def analyse_with_ai(client, log_line):
    """
    Sends one log line to Groq/Llama for analysis.
    Returns a dictionary with:
      threat  : "yes" or "no"
      type    : threat category or "none"
      reason  : one sentence explanation
      raw     : full AI response text
    """
    # The system prompt tells the AI exactly how to behave
    # Specific instructions = consistent, parseable output
    system_prompt = (
        "You are an expert SOC analyst. "
        "Analyse security log lines for threats. "
        "Always respond with EXACTLY these 3 lines and nothing else:\n"
        "THREAT: yes or no\n"
        "TYPE: threat category or none\n"
        "REASON: one sentence max"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": f"Analyse:\n{log_line}"}
            ],
            temperature=0.1,
            max_tokens=MAX_TOKENS
        )

        raw = response.choices[0].message.content.strip()

        # Parse the 3-line response into a dictionary
        result = {"threat": "no", "type": "none", "reason": "n/a", "raw": raw}

        for line in raw.split("\n"):
            line = line.strip()
            if line.upper().startswith("THREAT:"):
                result["threat"] = line.split(":", 1)[1].strip().lower()
            elif line.upper().startswith("TYPE:"):
                result["type"] = line.split(":", 1)[1].strip()
            elif line.upper().startswith("REASON:"):
                result["reason"] = line.split(":", 1)[1].strip()

        return result

    except Exception as e:
        # If API call fails, return safe default
        return {
            "threat": "unknown",
            "type":   "api_error",
            "reason": str(e)[:80],
            "raw":    ""
        }

# -----------------------------------------------
# Part 3: Write a log entry (same as before)
# -----------------------------------------------
def write_log(event_type, message):
    """Writes a timestamped entry to the log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] | {event_type:<10} | {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)

# -----------------------------------------------
# Part 4: Dashboard border helper
# -----------------------------------------------
def row(content=""):
    total = WIDTH - 2
    text  = " " + str(content)
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
# Part 5: Draw the AI-IDS dashboard
# -----------------------------------------------
def draw_dashboard(recent_alerts, total_lines):
    """Renders the live AI-IDS dashboard."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    divider("top")
    row(" AI-POWERED INTRUSION DETECTION SYSTEM")
    row(f" Last updated : {now}")
    row(f" Model        : Llama 3.3 (via Groq)")
    divider("mid")

    row(" SESSION STATS")
    row(f" Lines analysed by AI : {total_lines}")
    row(f" Threats confirmed    : {len(session_alerts)}")
    divider("mid")

    row(" RECENT AI ALERTS")
    if not session_alerts:
        row(" [OK] No threats detected yet")
    else:
        # Show last 5 alerts, most recent first
        for alert in session_alerts[-5:][::-1]:
            time_str = alert["time"]
            atype    = alert["type"][:20]
            row(f" [!] {time_str} — {atype}")
            reason   = alert["reason"][:WIDTH - 8]
            row(f"     {reason}")

    divider("mid")
    row(" WAITING FOR NEW LOG EVENTS...")
    row(f" Add events to: {LOG_FILE}")
    divider("bot")

# -----------------------------------------------
# Part 6: Real-time monitor loop with AI analysis
# -----------------------------------------------
def run_ai_ids(client):
    """
    Watches the log file in real time.
    Every new line is sent to the AI for analysis.
    Confirmed threats are stored and displayed.
    """
    global total_analysed

    # Create log file if it doesn't exist
    if not os.path.exists(LOG_FILE):
        write_log("INFO", "AI-IDS session started")
        print(f"\n  Created log file: {LOG_FILE}")

    print(f"\n  Watching : {LOG_FILE}")
    print(f"  AI Model : {MODEL}")
    print(f"  Press Ctrl+C to stop\n")
    time.sleep(2)

    with open(LOG_FILE, "r") as f:
        # Jump to end — only analyse NEW lines
        f.seek(0, 2)

        while True:
            line = f.readline()

            if line and line.strip():
                total_analysed += 1
                log_line = line.strip()

                # Show what we're analysing
                clear_screen()
                draw_dashboard(session_alerts, total_analysed)
                print(f"\n  Analysing: {log_line[:60]}...")
                print(f"  Sending to AI...")

                # Ask AI to analyse this line
                result = analyse_with_ai(client, log_line)

                # If AI says it's a threat — store it
                if result["threat"] == "yes":
                    alert = {
                        "time"   : datetime.datetime.now().strftime("%H:%M:%S"),
                        "line"   : log_line,
                        "type"   : result["type"],
                        "reason" : result["reason"]
                    }
                    session_alerts.append(alert)

                    # Print immediate alert
                    print(f"\n  *** AI THREAT DETECTED ***")
                    print(f"  Type   : {result['type']}")
                    print(f"  Reason : {result['reason']}")
                    print()

                else:
                    print(f"\n  AI: No threat — {result['reason'][:60]}")

                time.sleep(1)

                # Redraw clean dashboard
                clear_screen()
                draw_dashboard(session_alerts, total_analysed)
                print(f"\n  Monitoring... Ctrl+C to stop")

            else:
                # No new lines — wait and check again
                time.sleep(REFRESH_SECONDS)

# -----------------------------------------------
# Part 7: Main
# -----------------------------------------------
print("\n" + "=" * WIDTH)
print("  AI-POWERED INTRUSION DETECTION SYSTEM")
print("  by Anel Graph — Portfolio Project 2")
print("=" * WIDTH)

client = get_client()
print("\n  Groq API connected. ✅")
print("  AI model loaded. ✅")

try:
    run_ai_ids(client)

except KeyboardInterrupt:
    clear_screen()
    print("\n" + "=" * WIDTH)
    print("  AI-IDS SESSION ENDED")
    print("=" * WIDTH)
    print(f"  Lines analysed : {total_analysed}")
    print(f"  Threats found  : {len(session_alerts)}")

    if session_alerts:
        print(f"\n  Threat summary:")
        for i, alert in enumerate(session_alerts, 1):
            print(f"  [{i}] {alert['time']} — {alert['type']}")
            print(f"      {alert['reason']}")

    print(f"\n  Session ended : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * WIDTH)
    print("\n  Stay secure, Anel. 🛡️\n")
