# ============================================
# Script  : password_checker.py
# Purpose : Analyse password strength and give
#           actionable improvement advice
# Author  : Anel Graph
# Skill   : Security logic — sellable on Upwork
# ============================================

import re  # For pattern detection inside strings

# -----------------------------------------------
# Part 1: Analyse a single password
# -----------------------------------------------
def check_password(password):
    """
    Runs 5 security checks on the password.
    Returns a dictionary with full results.

    A dictionary is like a labelled box:
    results["score"] gives you the score
    results["rating"] gives you the rating
    etc.
    """
    results = {
        "password"  : password,
        "score"     : 0,
        "rating"    : "",
        "checks"    : {},   # Stores pass/fail for each check
        "advice"    : []    # Stores improvement tips
    }

    # ---- Check 1: Length ----
    # Shorter passwords are cracked faster
    # 8+ is minimum, 12+ is recommended, 16+ is excellent
    length = len(password)
    if length >= 16:
        results["score"] += 2      # Bonus point for extra length
        results["checks"]["length"] = f"Excellent ({length} chars)"
    elif length >= 12:
        results["score"] += 1
        results["checks"]["length"] = f"Good ({length} chars)"
    else:
        results["checks"]["length"] = f"Too short ({length} chars)"
        results["advice"].append("Use at least 12 characters")

    # ---- Check 2: Uppercase letters ----
    # re.search returns None if pattern not found
    if re.search(r"[A-Z]", password):
        results["score"] += 1
        results["checks"]["uppercase"] = "Present"
    else:
        results["checks"]["uppercase"] = "Missing"
        results["advice"].append("Add uppercase letters (A-Z)")

    # ---- Check 3: Lowercase letters ----
    if re.search(r"[a-z]", password):
        results["score"] += 1
        results["checks"]["lowercase"] = "Present"
    else:
        results["checks"]["lowercase"] = "Missing"
        results["advice"].append("Add lowercase letters (a-z)")

    # ---- Check 4: Numbers ----
    if re.search(r"[0-9]", password):
        results["score"] += 1
        results["checks"]["numbers"] = "Present"
    else:
        results["checks"]["numbers"] = "Missing"
        results["advice"].append("Add numbers (0-9)")

    # ---- Check 5: Special characters ----
    # These dramatically increase brute force difficulty
    if re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password):
        results["score"] += 1
        results["checks"]["special_chars"] = "Present"
    else:
        results["checks"]["special_chars"] = "Missing"
        results["advice"].append("Add special characters (!@#$%...)")

    # ---- Map score to rating ----
    # Score ranges from 0 to 6 (length can give 2 points)
    score = results["score"]
    if score >= 6:
        results["rating"] = "VERY STRONG"
    elif score == 5:
        results["rating"] = "STRONG"
    elif score == 4:
        results["rating"] = "MODERATE"
    elif score == 3:
        results["rating"] = "WEAK"
    else:
        results["rating"] = "VERY WEAK"

    return results

# -----------------------------------------------
# Part 2: Print a clean report
# -----------------------------------------------
def print_report(results):
    """
    Takes the results dictionary from check_password()
    and prints a formatted security report.
    """
    password = results["password"]
    score    = results["score"]
    rating   = results["rating"]

    # Mask the password for display — show first 2 chars only
    # Never print full passwords in logs or reports
    masked = password[:2] + "*" * (len(password) - 2)

    print("\n" + "-" * 48)
    print(f"  Password  : {masked}")
    print(f"  Score     : {score}/6")
    print(f"  Rating    : {rating}")
    print(f"\n  Checks:")

    # Print each check result
    for check, result in results["checks"].items():
        # Visual indicator — tick or cross
        icon = "+" if "Missing" not in result and "short" not in result else "!"
        print(f"    [{icon}] {check:<16} {result}")

    # Print advice if any
    if results["advice"]:
        print(f"\n  How to improve:")
        for tip in results["advice"]:
            print(f"    → {tip}")
    else:
        print(f"\n  No improvements needed — excellent password!")

    print("-" * 48)

# -----------------------------------------------
# Part 3: Main — test passwords
# -----------------------------------------------
print("\n" + "=" * 48)
print("     PASSWORD STRENGTH CHECKER")
print("     by Anel Graph — Security Toolkit")
print("=" * 48)

# --- Test a range of passwords automatically ---
# These show the full range from terrible to excellent
test_passwords = [
    "password",           # Classic terrible password
    "Password1",          # Looks okay but common pattern
    "P@ssw0rd!",          # Better but still predictable
    "MyDog$Name7Is!Rex",  # Getting strong
    "kX9!mP#qL2@vR5$nW",  # Excellent — random and long
]

print("\n  Running automatic tests...\n")

for pwd in test_passwords:
    report = check_password(pwd)
    print_report(report)

# --- Let the user test their own password ---
print("\n" + "=" * 48)
print("  Test your own password")
print("=" * 48)

user_password = input("\n  Enter a password to check: ")
report = check_password(user_password)
print_report(report)

print("\n  Tip: Never use a real password in a test script.")
print("  Use a similar pattern with different characters.\n")
