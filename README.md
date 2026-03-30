# 🛡️ Python Security Toolkit

A collection of Python automation scripts built as part of my 
cybersecurity and automation training.

---

## 📁 Projects

### 1. Professional Profile (`task1_profile/`)
Displays a formatted personal profile using Python variables,
lists, and the datetime module.

**Concepts:** variables, f-strings, lists, datetime

---

### 2. Security Log Writer (`task2_log_writer/`)
Simulates a real security tool by writing timestamped log entries
to a persistent file. Supports INFO, WARNING, CRITICAL, and ALERT
severity levels — exactly as production logging tools do.

**Concepts:** file handling, append mode, functions, timestamps

---

### 3. Automated Threat Detector (`task3_threat_detector/`)
Parses a security log file and automatically detects threats:
- Brute-force attacks (repeated failed logins)
- Port scans (via IP extraction)
- Critical system events

Uses regex pattern matching and threshold-based alerting —
the same core logic behind tools like Splunk and Wazuh.

**Concepts:** regex, file parsing, dictionaries, SIEM logic

---

## 🚀 How to Run
```bash
# Clone this repository
git clone https://github.com/👉YOUR_USERNAME/security-toolkit.git
cd security-toolkit

# Run any script
python3 task1_profile/my_info.py
python3 task2_log_writer/log_writer.py
python3 task3_threat_detector/threat_detector.py
```

---

## 🎯 Goal

Training toward remote roles in:
- SOC Analysis
- Security Automation
- Cloud Security Engineering

**Author:** Anel Graph  
**Status:** Training in progress 🚀
