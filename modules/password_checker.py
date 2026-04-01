import re

def check_password(password):
    results = {
        "password": password,
        "score":    0,
        "rating":   "",
        "checks":   {},
        "advice":   []
    }
    length = len(password)
    if length >= 16:
        results["score"] += 2
        results["checks"]["length"] = f"Excellent ({length} chars)"
    elif length >= 12:
        results["score"] += 1
        results["checks"]["length"] = f"Good ({length} chars)"
    else:
        results["checks"]["length"] = f"Too short ({length} chars)"
        results["advice"].append("Use at least 12 characters")
    if re.search(r"[A-Z]", password):
        results["score"] += 1
        results["checks"]["uppercase"] = "Present"
    else:
        results["checks"]["uppercase"] = "Missing"
        results["advice"].append("Add uppercase letters (A-Z)")
    if re.search(r"[a-z]", password):
        results["score"] += 1
        results["checks"]["lowercase"] = "Present"
    else:
        results["checks"]["lowercase"] = "Missing"
        results["advice"].append("Add lowercase letters (a-z)")
    if re.search(r"[0-9]", password):
        results["score"] += 1
        results["checks"]["numbers"] = "Present"
    else:
        results["checks"]["numbers"] = "Missing"
        results["advice"].append("Add numbers (0-9)")
    if re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password):
        results["score"] += 1
        results["checks"]["special_chars"] = "Present"
    else:
        results["checks"]["special_chars"] = "Missing"
        results["advice"].append("Add special characters (!@#$%...)")
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

def print_report(results):
    password = results["password"]
    score    = results["score"]
    rating   = results["rating"]
    masked   = password[:2] + "*" * (len(password) - 2)
    print("\n" + "-" * 48)
    print(f"  Password  : {masked}")
    print(f"  Score     : {score}/6")
    print(f"  Rating    : {rating}")
    print(f"\n  Checks:")
    for check, result in results["checks"].items():
        icon = "+" if "Missing" not in result and "short" not in result else "!"
        print(f"    [{icon}] {check:<16} {result}")
    if results["advice"]:
        print(f"\n  How to improve:")
        for tip in results["advice"]:
            print(f"    → {tip}")
    else:
        print(f"\n  No improvements needed — excellent password!")
    print("-" * 48)

if __name__ == "__main__":
    test_passwords = [
        "password",
        "Password1",
        "P@ssw0rd!",
        "MyDog$Name7Is!Rex",
        "kX9!mP#qL2@vR5$nW",
    ]
    for pwd in test_passwords:
        print_report(check_password(pwd))