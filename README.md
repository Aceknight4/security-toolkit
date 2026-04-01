# 🛡️ Python Security Toolkit

A unified, menu-driven security toolkit built entirely in Python.
Designed to demonstrate core SOC analyst and automation skills
through practical, working tools.

Run everything from a single entry point:

    python3 toolkit.py

---

## 🔧 Tools Included

| Tool | Description | Key Concepts |
|---|---|---|
| Log Writer | Generates timestamped security events | File I/O, severity levels |
| Threat Detector | Parses logs and flags threats | Regex, SIEM logic |
| Real-Time Monitor | Watches log file live | File tailing, while True |
| Port Scanner | Scans a target for open ports | Sockets, TCP, recon |
| Password Checker | Scores password strength | Regex, scoring, entropy |

---

## 📁 Project Structure

    security-toolkit/
    ├── toolkit.py
    ├── modules/
    │   ├── log_writer.py
    │   ├── threat_detector.py
    │   ├── port_scanner.py
    │   └── password_checker.py
    └── task5_realtime_monitor/
        └── realtime_monitor.py

---

## 🚀 Quick Start

    git clone https://github.com/Aceknight4/security-toolkit.git
    cd security-toolkit
    python3 toolkit.py

Requirements: Python 3.8+ — standard library only, no pip installs needed.

---

## 🎯 Skills Demonstrated

**Python**
- File handling — read, write, append
- Regex pattern matching with the re module
- Socket programming and TCP connections
- Dictionary counters and threshold logic
- Real-time file tailing with while True loops
- Modular code design with imports

**Cybersecurity**
- SIEM detection logic — brute force, port scan, critical events
- Security log format — timestamped, severity-levelled entries
- Network reconnaissance — port scanning and service identification
- Password entropy analysis — character class scoring

**Tools & Workflow**
- Git version control and GitHub portfolio management
- Linux terminal — Kali Linux environment

---

## 🌍 Real-World Relevance

| This toolkit mirrors... | Real tools like... |
|---|---|
| Log writer | Syslog, Windows Event Log |
| Threat detector | Splunk, IBM QRadar |
| Real-time monitor | Fail2Ban, OSSEC |
| Port scanner | Nmap |
| Password checker | zxcvbn, HaveIBeenPwned API |

---

## 👤 Author

**Anel Graph**
Training toward remote roles in SOC Analysis, Security Automation,
and Cloud Security Engineering.

GitHub: https://github.com/Aceknight4
Status: Training in progress 🚀
```


