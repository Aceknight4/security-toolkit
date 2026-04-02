# ============================================
# Module  : utils.py
# Purpose : Cross-platform compatibility layer
# Author  : Anel Graph
# Works on: Linux, macOS, Windows
# ============================================

import os
import platform
import sys

# Detect OS once at import time
# platform.system() returns "Linux", "Darwin" (macOS), or "Windows"
CURRENT_OS = platform.system()
IS_WINDOWS  = CURRENT_OS == "Windows"
IS_MAC      = CURRENT_OS == "Darwin"
IS_LINUX    = CURRENT_OS == "Linux"

def clear_screen():
    """
    Clears the terminal screen on any OS.
    Linux/Mac → 'clear'
    Windows   → 'cls'
    """
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")

def get_log_path(filename="security_events.log"):
    """
    Returns the correct path to the log file
    regardless of which OS is running.

    os.path.join() automatically uses the right
    slash direction:
      Linux/Mac → security-toolkit/security_events.log
      Windows   → security-toolkit\\security_events.log
    """
    # Get the directory where this utils.py file lives
    # then go one level up to security-toolkit/
    base_dir = os.path.dirname(  # directory of utils.py = modules/
        os.path.dirname(          # one level up = security-toolkit/
            os.path.abspath(__file__)
        )
    )
    return os.path.join(base_dir, filename)

def get_home_path(*parts):
    """
    Builds a path from the home directory.
    Works on all OS.

    Example:
      get_home_path("security-toolkit", "logs")
      Linux  → /home/aceknight/security-toolkit/logs
      Mac    → /Users/anel/security-toolkit/logs
      Windows→ C:\\Users\\Anel\\security-toolkit\\logs
    """
    return os.path.join(os.path.expanduser("~"), *parts)

def set_api_key_instructions(service="GROQ"):
    """
    Prints the correct instructions for setting
    an environment variable on the current OS.
    """
    key_name = f"{service}_API_KEY"
    print(f"\n  To set your {service} API key:")

    if IS_WINDOWS:
        print(f"  CMD        : set {key_name}=your_key_here")
        print(f"  PowerShell : $env:{key_name}='your_key_here'")
    else:
        print(f"  Terminal   : export {key_name}='your_key_here'")
        print(f"  Permanent  : echo 'export {key_name}=your_key' >> ~/.bashrc")

def check_python_version():
    """
    Verifies Python 3.8+ is being used.
    Exits with a helpful message if not.
    """
    major = sys.version_info.major
    minor = sys.version_info.minor

    if major < 3 or (major == 3 and minor < 8):
        print(f"  ERROR: Python 3.8+ required.")
        print(f"  You have: Python {major}.{minor}")
        print(f"  Please upgrade Python and try again.")
        sys.exit(1)

def print_os_info():
    """
    Prints current OS and Python version.
    Useful for debugging and portfolio demos.
    """
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"  OS      : {CURRENT_OS}")
    print(f"  Python  : {py_version}")
    print(f"  Platform: {platform.platform()}")
