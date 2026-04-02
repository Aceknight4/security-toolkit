# ============================================
# Script  : toolkit.py
# Purpose : Unified entry point for the
#           Python Security Toolkit
# Author  : Anel Graph
# Usage   : python3 toolkit.py
# ============================================

import os
import sys
from modules.utils import clear_screen, check_python_version, print_os_info
check_python_version()

# Add the current directory to Python's search path
# This lets us import from the modules/ folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all modules
from modules import log_writer
from modules import threat_detector
from modules import port_scanner
from modules import password_checker

# -----------------------------------------------
# Menu display function
# -----------------------------------------------
def show_menu():
    """Prints the main toolkit menu."""
    print("\n" + "=" * 52)
    print("       PYTHON SECURITY TOOLKIT v1.0")
    print("       by Anel Graph")
    print("=" * 52)
    print("  [1]  Generate security log events")
    print("  [2]  Run static threat detector")
    print("  [3]  Start real-time log monitor")
    print("  [4]  Run network port scanner")
    print("  [5]  Check password strength")
    print("  [0]  Exit toolkit")
    print("=" * 52)

    menu_actions = {
        "1": run_log_writer,
        "2": run_threat_detector,
        "3": lambda: print("\n  Run: python3 task5_realtime_monitor/realtime_monitor.py"),
        "4": run_port_scanner,
        "5": run_password_checker,
        "6": lambda: print_os_info(),        # ← add this
    }
# -----------------------------------------------
# Wrapper functions — one per tool
# -----------------------------------------------
def run_log_writer():
    print("\n[ LOG WRITER — Starting ]\n")
    log_writer.write_log("INFO",     "Toolkit session started")
    log_writer.write_log("WARNING",  "Simulated failed login — user: testuser")
    log_writer.write_log("WARNING",  "Simulated failed login — user: testuser")
    log_writer.write_log("CRITICAL", "Simulated account lockout")
    log_writer.write_log("ALERT",    "Simulated port scan — source IP: 10.0.0.1")
    log_writer.read_logs()

def run_threat_detector():
    print("\n[ THREAT DETECTOR — Starting ]\n")
    # Check log file exists first
    if not os.path.exists(log_writer.LOG_FILE):
        print("  No log file found. Run the Log Writer first (option 1).")
        return
    threat_detector.parse_log(log_writer.LOG_FILE)
    threat_detector.detect_brute_force()
    threat_detector.detect_port_scans()
    threat_detector.detect_critical_events()
    threat_detector.print_report()

def run_port_scanner():
    print("\n[ PORT SCANNER — Starting ]\n")
    target = input("  Enter target hostname or IP (default: localhost): ").strip()
    if not target:
        target = "localhost"

    try:
        start = int(input("  Start port (default: 1): ").strip() or "1")
        end   = int(input("  End port   (default: 1024): ").strip() or "1024")
    except ValueError:
        print("  Invalid port number. Using defaults.")
        start, end = 1, 1024

    port_scanner.run_scanner(target, start, end)

def run_password_checker():
    print("\n[ PASSWORD CHECKER — Starting ]\n")
    while True:
        pwd = input("  Enter password to check (or 'done' to exit): ").strip()
        if pwd.lower() == "done":
            break
        if pwd:
            report = password_checker.check_password(pwd)
            password_checker.print_report(report)

# -----------------------------------------------
# Main loop
# -----------------------------------------------
# Map menu choices to functions
menu_actions = {
    "1": run_log_writer,
    "2": run_threat_detector,
    "3": lambda: print("\n  Start realtime_monitor.py directly in its own terminal.\n  Run: python3 task5_realtime_monitor/realtime_monitor.py"),
    "4": run_port_scanner,
    "5": run_password_checker,
}

print("\n  Welcome to your Python Security Toolkit.")
print("  All tools available from one place.\n")

while True:
    show_menu()
    choice = input("\n  Enter your choice: ").strip()

    if choice == "0":
        print("\n  Toolkit closed. Stay secure, Anel. 👋\n")
        break
    elif choice in menu_actions:
        menu_actions[choice]()   # Call the matching function
    else:
        print("\n  Invalid choice. Enter a number from the menu.")
