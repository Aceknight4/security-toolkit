import datetime
import os

LOG_FILE = "security_events.log"

def write_log(event_type, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] | {event_type:<10} | {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(f"  Logged: {log_entry.strip()}")

def read_logs():
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

if __name__ == "__main__":
    print("\nStarting log simulation...\n")
    write_log("INFO",     "System startup complete")
    write_log("WARNING",  "Failed login attempt — user: admin")
    write_log("CRITICAL", "Account locked after 3 failed attempts")
    write_log("ALERT",    "Port scan detected — source IP: 192.168.1.45")
    read_logs()