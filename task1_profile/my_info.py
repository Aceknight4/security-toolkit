# ============================================
# Script: my_info.py
# Purpose: Display my professional profile
# Author: 👉 Your Name
# ============================================

import datetime  # Built-in Python module

# --- Your Info (edit these) ---
name = "👉 Anel Graph"
goal = "👉 Become an expert Remote Automation Specialist & SOC Analyst"
skills_learning = ["Python","Machine Learning", "Cybersecurity", "Cloud", "AI Automation"]
start_date = "2025-01-01"  # When you started learning

# --- Auto-calculated ---
today = datetime.date.today()
start = datetime.date.fromisoformat(start_date)
days_learning = (today - start).days

# --- Display Output ---
print("=" * 45)
print("       MY PROFESSIONAL PROFILE")
print("=" * 45)
print(f"Name        : {name}")
print(f"Goal        : {goal}")
print(f"Skills      : {', '.join(skills_learning)}")
print(f"Days Active : {days_learning} days into my journey")
print(f"Date Today  : {today}")
print("=" * 45)
print("Status: TRAINING IN PROGRESS 🚀")
print("=" * 45)
