#!/usr/bin/env python3
"""
TeachScript Test Suite

Runs all TeachScript examples and verifies they execute correctly.
"""

import sys
import os
import subprocess
from pathlib import Path


EXAMPLES_DIR = Path(__file__).parent / "teachscript_examples"
RUNNER = Path(__file__).parent / "run_teachscript.py"

# Examples that don't require user input
NON_INTERACTIVE_EXAMPLES = [
    "01_hello_world.teach",
    "02_variables.teach",
    "03_conditionals.teach",
    "04_loops.teach",
    "05_functions.teach",
    "06_lists_strings.teach",
    "08_prime_numbers.teach",
]

# Interactive examples (skip in automated tests)
INTERACTIVE_EXAMPLES = [
    "07_calculator.teach",
    "09_guessing_game.teach",
]


def run_example(filename):
    """Run a single TeachScript example and return the result."""
    filepath = EXAMPLES_DIR / filename

    if not filepath.exists():
        return False, f"File not found: {filepath}"

    try:
        result = subprocess.run(
            [sys.executable, str(RUNNER), str(filepath)],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Execution timeout"
    except Exception as e:
        return False, str(e)


def main():
    """Run all tests."""
    print("=" * 70)
    print("TeachScript Test Suite")
    print("Honey Badger Language Construction Set")
    print("=" * 70)
    print()

    passed = 0
    failed = 0

    for filename in NON_INTERACTIVE_EXAMPLES:
        print(f"Testing: {filename}")
        print("-" * 70)

        success, output = run_example(filename)

        if success:
            print(f"✓ PASS")
            print()
            print("Output:")
            print(output)
            passed += 1
        else:
            print(f"✗ FAIL")
            print()
            print("Error:")
            print(output)
            failed += 1

        print()

    # Show interactive examples
    print("=" * 70)
    print("Interactive Examples (not auto-tested):")
    print("=" * 70)
    for filename in INTERACTIVE_EXAMPLES:
        print(f"  - {filename}")
    print()
    print("Run these manually with:")
    print(f"  python3 run_teachscript.py teachscript_examples/<filename>")
    print()

    # Summary
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")
    print()

    if failed == 0:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
