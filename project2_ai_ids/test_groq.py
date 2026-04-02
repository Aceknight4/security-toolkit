# ============================================
# Script  : test_groq.py
# Purpose : Verify Groq API works correctly
# Author  : Anel Graph
# ============================================

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from modules.utils import set_api_key_instructions

from groq import Groq

# --- Get API key from environment ---
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("\n  ERROR: GROQ_API_KEY not set.")
    set_api_key_instructions("GROQ")
    sys.exit(1)

print("\n  Connecting to Groq API...")
print("  Sending test security log line...\n")

# --- Create client ---
client = Groq(api_key=api_key)

# --- Test log line ---
test_log = "[2026-04-02 03:00:00] | WARNING | Failed login attempt — user: admin"

# --- Send to AI ---
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a SOC analyst. Analyse security log lines. "
                "For each log line respond with exactly 3 lines:\n"
                "THREAT: yes or no\n"
                "TYPE: the threat category or 'none'\n"
                "REASON: one sentence explanation"
            )
        },
        {
            "role": "user",
            "content": f"Analyse this log line:\n{test_log}"
        }
    ],
    temperature=0.1,
    max_tokens=100
)

# --- Extract response ---
ai_response = response.choices[0].message.content

print("  AI Analysis:")
print("  " + "-" * 40)
for line in ai_response.strip().split("\n"):
    print(f"  {line}")
print("  " + "-" * 40)
print("\n  Groq API connection successful. ✅\n")
