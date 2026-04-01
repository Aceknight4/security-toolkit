import socket
import datetime

def scan_port(target_ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((target_ip, port))
        return True
    except:
        return False
    finally:
        s.close()

def run_scanner(target, start_port, end_port):
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Error: Cannot resolve '{target}'.")
        return
    print("\n" + "=" * 52)
    print("         NETWORK PORT SCANNER — REPORT")
    print("=" * 52)
    print(f"  Target   : {target} ({target_ip})")
    print(f"  Ports    : {start_port} to {end_port}")
    print(f"  Started  : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 52)
    print("  Scanning...\n")
    open_ports = []
    for port in range(start_port, end_port + 1):
        if port % 100 == 0:
            print(f"  Checking port {port}...")
        if scan_port(target_ip, port):
            open_ports.append(port)
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            print(f"  [OPEN]  Port {port:<6} — {service}")
    print("\n" + "=" * 52)
    print(f"  Scan complete.")
    print(f"  Open ports found : {len(open_ports)}")
    if open_ports:
        print(f"  Open port list   : {open_ports}")
    else:
        print("  No open ports detected in this range.")
    print(f"  Finished : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 52 + "\n")

if __name__ == "__main__":
    run_scanner("localhost", 1, 1024)