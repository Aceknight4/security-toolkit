<div align="center">

# 🔧 Python Security Toolkit
### SOC Automation Scripts — Log Analysis, Threat Detection, Port Scanning & More

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SOC](https://img.shields.io/badge/SOC-Automation-1B2A4A?style=for-the-badge)](https://github.com/Aceknight4)
[![SIEM Logic](https://img.shields.io/badge/SIEM-Logic-2563EB?style=for-the-badge)](https://github.com/Aceknight4)

> A growing collection of Python security automation scripts that mirror real SOC analyst workflows — built as the foundation for [SentinelLite](https://github.com/Aceknight4/SentinelLite).

</div>

---

## 📌 Why This Project Exists

Before building SentinelLite, I needed to master the core Python building blocks that power every SOC tool — log parsing, regex threat detection, port scanning, and real-time monitoring. This toolkit is that foundation, built script by script.

Each tool here maps to a real-world SOC function:

| Script | Real-World Equivalent |
|--------|----------------------|
| Log Writer | SIEM event ingestion |
| Threat Detector | SIEM alert rules (Splunk, Wazuh) |
| Port Scanner | Nmap / asset discovery |
| Real-time Monitor | SOC dashboard / live feed |
| Password Checker | PAM / password policy enforcement |

---

## 📁 Project Structure

```
security-toolkit/
├── task1_profile/          # Python fundamentals — profile display
├── task2_log_writer/       # Security log writer with severity levels
├── task3_threat_detector/  # Log parser + regex-based threat detection
├── task5_realtime_monitor/ # Live network/process monitoring
├── task6_port_scanner/     # Python TCP port scanner
├── task7_password_checker/ # Password strength analyzer
└── README.md
```

---

## 🛠️ Scripts Overview

### 📄 Task 1 — Professional Profile (`task1_profile/`)
Displays a formatted personal security profile using Python variables, lists, f-strings, and datetime.  
**Concepts:** variables, data types, f-strings, lists, datetime module

---

### 📋 Task 2 — Security Log Writer (`task2_log_writer/`)
Simulates a production security logging tool. Writes timestamped entries to a persistent log file with severity levels matching real SIEM tools.

**Severity levels:** `INFO` | `WARNING` | `CRITICAL` | `ALERT`

```python
# Example output:
[2025-08-14 10:23:41] [CRITICAL] Failed login attempt from 192.168.1.105 (attempt 5/5)
[2025-08-14 10:23:45] [ALERT] Brute force threshold exceeded — IP flagged
```

**Concepts:** file I/O, append mode, functions, timestamps, severity classification

---

### 🔍 Task 3 — Automated Threat Detector (`task3_threat_detector/`)
Parses a security log file and automatically detects:
- **Brute-force attacks** — repeated failed login attempts above threshold
- **Port scans** — multiple port hits from same source IP
- **Critical system events** — keyword-based pattern matching

Uses regex pattern matching and threshold-based alerting — the same core logic behind Splunk and Wazuh detection rules.

```python
# Example output:
[THREAT DETECTED] Brute Force: 192.168.1.105 — 8 failed attempts in 60s
[THREAT DETECTED] Port Scan: 10.0.0.22 — 45 ports probed
```

**Concepts:** regex, file parsing, dictionaries, threshold logic, SIEM correlation

---

### 📡 Task 5 — Real-Time Monitor (`task5_realtime_monitor/`)
Monitors live system processes or network activity and flags anomalies in real time. Refreshes at set intervals like a basic SOC dashboard feed.

**Concepts:** subprocess, psutil, real-time loops, anomaly detection

---

### 🔌 Task 6 — Port Scanner (`task6_port_scanner/`)
A Python TCP port scanner that identifies open ports on a target host. Supports custom port ranges and outputs results in a clean, readable format.

```bash
python3 task6_port_scanner/scanner.py --target 192.168.1.1 --ports 1-1024
```

**Concepts:** socket programming, TCP handshake, threading, network fundamentals

---

### 🔑 Task 7 — Password Strength Checker (`task7_password_checker/`)
Analyzes password strength against security policy rules — checks length, complexity, common patterns, and dictionary words. Returns a score and improvement suggestions.

**Concepts:** string analysis, regex, policy enforcement, security awareness

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/Aceknight4/security-toolkit.git
cd security-toolkit

# Run any script (no dependencies needed for most)
python3 task2_log_writer/log_writer.py
python3 task3_threat_detector/threat_detector.py
python3 task6_port_scanner/scanner.py --target 127.0.0.1 --ports 1-100
```

---

## 🔗 Related Projects

- [SentinelLite](https://github.com/Aceknight4/SentinelLite) — Full SOC automation system built on these foundations + Suricata + ML

---

## 👤 Author

**Seppo Anel Graph Mbake**  
SOC Analyst | Blue Team Engineer | ISO 27001 Certified  
📧 [annelgraph46@gmail.com](mailto:annelgraph46@gmail.com)  
🔗 [LinkedIn](https://linkedin.com/in/seppo-anel-graph-mbake-03b736206)
