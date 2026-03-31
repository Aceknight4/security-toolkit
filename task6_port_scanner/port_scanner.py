# ============================================
# Script  : port_scanner.py
# Purpose : Scan a target for open network ports
# Author  : Anel Graph
# Skill   : Network reconnaissance — core security skill
# WARNING : Only scan systems you own or have
#           explicit permission to scan
# ============================================

import socket    # For making network connections
import datetime  # For timestamps on the report
import sys       # For reading command-line arguments

# -----------------------------------------------
# Part 2: Scan a single port
# -----------------------------------------------
def scan_port(target_ip, port):
    """
    Tries to connect to one port on the target.
    Returns True if open, False if closed.

    How it works:
    1. Create a socket (the "phone")
    2. Set a 1-second timeout (don't wait forever)
    3. Try to connect to target_ip on this port
    4. If connection works → port is open → return True
    5. If connection fails → port is closed → return False
    6. Always close the socket when done (clean up)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET  = use IPv4 addresses (standard internet addresses)
    # SOCK_STREAM = use TCP (reliable, connection-based protocol)

    s.settimeout(1)  # Give up after 1 second of no response

    try:
        s.connect((target_ip, port))
        return True   # Connection succeeded — port is OPEN
    except:
        return False  # Connection failed — port is CLOSED
    finally:
        s.close()     # Always clean up the socket
        # "finally" runs whether the try succeeded or failed

# -----------------------------------------------
# Part 3: Run a full scan across a port range
# -----------------------------------------------
def run_scanner(target, start_port, end_port):
    """
    Scans all ports from start_port to end_port.
    Prints open ports as it finds them.
    Prints a summary report at the end.
    """

    # Resolve hostname to IP address
    # Example: "localhost" → "127.0.0.1"
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Error: Cannot resolve '{target}' to an IP address.")
        print("Check the hostname and try again.")
        return

    # Print scan header
    print("\n" + "=" * 52)
    print("         NETWORK PORT SCANNER — REPORT")
    print("=" * 52)
    print(f"  Target   : {target} ({target_ip})")
    print(f"  Ports    : {start_port} → {end_port}")
    print(f"  Started  : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 52)
    print("  Scanning...\n")

    open_ports = []   # List to collect all open ports found

    # Loop through every port in the range
    for port in range(start_port, end_port + 1):

        # Show progress every 100 ports so we know it's working
        if port % 100 == 0:
            print(f"  Checking port {port}...")

        result = scan_port(target_ip, port)

        if result:
            # Port is open — record it and print immediately
            open_ports.append(port)

            # Try to identify what service normally runs on this port
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"

            print(f"  [OPEN]  Port {port:<6} — {service}")

    # Print final summary
    print("\n" + "=" * 52)
    print(f"  Scan complete.")
    print(f"  Open ports found : {len(open_ports)}")

    if open_ports:
        print(f"  Open port list   : {open_ports}")
    else:
        print("  No open ports detected in this range.")

    print(f"  Finished : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 52 + "\n")

# -----------------------------------------------
# Part 4: Main — get target and run the scan
# -----------------------------------------------
print("\n" + "=" * 52)
print("        PYTHON PORT SCANNER — by Anel Graph")
print("=" * 52)

# Scan localhost (your own machine) — always safe
# localhost = 127.0.0.1 = your own computer
TARGET     = "localhost"
START_PORT = 1
END_PORT   = 1024   # Ports 1–1024 are "well-known" ports

print(f"\n  Target set to : {TARGET}")
print(f"  Port range    : {START_PORT} to {END_PORT}")
print(f"\n  Note: Only scan systems you own or have")
print(f"  permission to scan.\n")

run_scanner(TARGET, START_PORT, END_PORT)
