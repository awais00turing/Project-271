#!/usr/bin/env python3
"""
Script to run Pylint on the project.
"""
import sys
import subprocess

def run_pylint():
    """Run Pylint on the app directory."""
    print("Running Pylint...")
    result = subprocess.run(
        ["pylint", "app"],
        capture_output=True,
        text=True,
        check=False
    )
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_pylint())